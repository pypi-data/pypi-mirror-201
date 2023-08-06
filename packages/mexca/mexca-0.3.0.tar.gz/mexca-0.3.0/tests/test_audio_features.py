"""Test audio feature calculation classes and methods.
"""

import librosa
import pytest
import numpy as np
from mexca.audio.features import (
    AudioSignal,
    BaseFrames,
    BaseSignal,
    FormantFrames,
    FormantAmplitudeFrames,
    PitchFrames,
    PitchHarmonicsFrames,
    PitchPulseFrames,
    SpecFrames,
    JitterFrames,
    ShimmerFrames,
    HnrFrames
)


@pytest.fixture
def audio_file():
    return librosa.ex("trumpet")


class TestBaseSignal:
    n_samples = 10

    @pytest.fixture
    def sig_obj(self):
        return BaseSignal(np.random.uniform(-1, 1, self.n_samples), self.n_samples)

    def test_idx(self, sig_obj):
        idx = sig_obj.idx
        assert np.all(idx == np.arange(self.n_samples))

    def test_ts(self, sig_obj):
        ts = sig_obj.ts
        assert np.all(ts == sig_obj.idx / sig_obj.sr)


class TestAudioSignal(TestBaseSignal):
    def test_from_file(self, audio_file):
        sig_obj = AudioSignal.from_file(audio_file)
        assert isinstance(sig_obj, (AudioSignal, BaseSignal))


class TestBaseFrames:
    frame_len = 1024
    hop_len = frame_len // 4

    @pytest.fixture
    def sig_obj(self, audio_file):
        return AudioSignal.from_file(audio_file)

    @pytest.fixture
    def sig_frames_obj(self, sig_obj):
        return BaseFrames.from_signal(
            sig_obj, frame_len=self.frame_len, hop_len=self.hop_len
        )

    @pytest.fixture
    def frames_scope(self, sig_frames_obj):
        return sig_frames_obj

    def test_idx(self, sig_obj, frames_scope):
        idx = frames_scope.idx
        assert np.all(idx == np.arange((sig_obj.sig.shape[0] + 1) // self.hop_len + 1))

    def test_ts(self, frames_scope):
        ts = frames_scope.ts
        assert np.all(
            ts
            == librosa.frames_to_time(
                frames_scope.idx, sr=frames_scope.sr, hop_length=frames_scope.hop_len
            )
        )


class TestPitchFrames(TestBaseFrames):
    @pytest.fixture
    def pitch_frames_obj(self, sig_obj):
        return PitchFrames.from_signal(
            sig_obj, frame_len=self.frame_len, hop_len=self.hop_len
        )

    @pytest.fixture
    def frames_scope(self, pitch_frames_obj):
        return pitch_frames_obj

    def test_pitch_pyin(self, pitch_frames_obj):
        pitch_f0 = pitch_frames_obj.frames
        assert pitch_f0.shape == pitch_frames_obj.ts.shape == pitch_frames_obj.idx.shape
        assert np.all(np.logical_or(pitch_f0 > 0, np.isnan(pitch_f0)))


class TestSpecFrames(TestBaseFrames):
    @pytest.fixture
    def spec_frames_obj(self, sig_obj):
        return SpecFrames.from_signal(
            sig_obj, frame_len=self.frame_len, hop_len=self.hop_len
        )

    @pytest.fixture
    def frames_scope(self, spec_frames_obj):
        return spec_frames_obj

    def test_spec(self, spec_frames_obj):
        spec = spec_frames_obj.frames
        assert spec.shape[:1] == spec_frames_obj.ts.shape == spec_frames_obj.idx.shape
        assert np.all(
            np.iscomplex(spec[:, 1:-1])
        )  # First and last columns are not complex


class TestFormantFrames(TestBaseFrames):
    @pytest.fixture
    def formant_frames_obj(self, sig_frames_obj):
        return FormantFrames.from_frames(sig_frames_obj)

    @pytest.fixture
    def frames_scope(self, formant_frames_obj):
        return formant_frames_obj

    def test_formants(self, formant_frames_obj):
        formants = formant_frames_obj.frames
        assert isinstance(formants, list)
        assert (
            len(formants)
            == formant_frames_obj.ts.shape[0]
            == formant_frames_obj.idx.shape[0]
        )
        assert np.all(np.array([np.all(np.array(f) > 0) for f in formants]))

    def test_calc_formants(self, sig_frames_obj, formant_frames_obj):
        coefs = librosa.lpc(sig_frames_obj.frames, order=10)
        formants = formant_frames_obj._calc_formants(
            coefs[0, :],
            sig_frames_obj.sr,
            formant_frames_obj.lower,
            formant_frames_obj.upper,
        )
        assert isinstance(formants, list)
        assert np.all(np.array(formants))


class TestPitchHarmonicsFrames(TestPitchFrames, TestSpecFrames):
    n_harmonics = 100

    @pytest.fixture
    def harmonics_frames_obj(self, spec_frames_obj, pitch_frames_obj):
        return PitchHarmonicsFrames.from_spec_and_pitch_frames(
            spec_frames_obj, pitch_frames_obj, self.n_harmonics
        )

    @pytest.fixture
    def frames_scope(self, harmonics_frames_obj):
        return harmonics_frames_obj

    def test_harmonics(self, harmonics_frames_obj):
        harmonics = harmonics_frames_obj.frames
        assert (
            harmonics.shape[0]
            == harmonics_frames_obj.ts.shape[0]
            == harmonics_frames_obj.idx.shape[0]
        )
        assert np.all(np.logical_or(harmonics >= 0, np.isnan(harmonics)))


class TestFormantAmplitudeFrames(TestFormantFrames, TestPitchHarmonicsFrames):
    @pytest.fixture
    def formant_amp_frames_obj(
        self, formant_frames_obj, harmonics_frames_obj, pitch_frames_obj
    ):
        return FormantAmplitudeFrames.from_formant_harmonics_and_pitch_frames(
            formant_frames_obj, harmonics_frames_obj, pitch_frames_obj
        )

    @pytest.fixture
    def frames_scope(self, formant_amp_frames_obj):
        return formant_amp_frames_obj

    def test_formant_amplitude(self, formant_amp_frames_obj, formant_frames_obj):
        amp = formant_amp_frames_obj.frames
        assert isinstance(amp, np.ndarray)
        assert (
            amp.shape[0]
            == formant_amp_frames_obj.ts.shape[0]
            == formant_amp_frames_obj.idx.shape[0]
        )
        assert amp.shape[1] == formant_frames_obj.max_formants


class TestPitchPulseFrames(TestPitchFrames):
    @pytest.fixture
    def pulses_frames_obj(self, sig_obj, pitch_frames_obj):
        return PitchPulseFrames.from_signal_and_pitch_frames(sig_obj, pitch_frames_obj)

    @pytest.fixture
    def frames_scope(self, pulses_frames_obj):
        return pulses_frames_obj

    def test_pulses(self, pulses_frames_obj):
        pulses = pulses_frames_obj.frames
        assert isinstance(pulses, list)
        assert (
            len(pulses)
            == pulses_frames_obj.ts.shape[0]
            == pulses_frames_obj.idx.shape[0]
        )
        assert np.all(
            np.array(
                [
                    isinstance(puls, tuple) and np.all(np.array(puls[:2]) >= 0)
                    for frame in pulses
                    for puls in frame
                    if len(frame) > 0
                ]
            )
        )

    def test_get_next_pulse(self, pulses_frames_obj):
        frame = np.random.uniform(-1, 1, self.frame_len)
        ts = np.linspace(0, 1, num=self.frame_len)
        t0 = 0.005 + np.random.uniform(0, 0.0005, self.frame_len)
        start = 0.5 - 0.0025
        stop = 0.5 + 0.0025
        pulses = []
        pulses_frames_obj._get_next_pulse(frame, ts, t0, start, stop, True, pulses)
        pulses_frames_obj._get_next_pulse(frame, ts, t0, start, stop, False, pulses)
        assert len(pulses) > 0
        assert np.all(
            np.array([isinstance(puls, tuple) and puls[0] > 0 for puls in pulses])
        )


class TestJitterFrames(TestPitchPulseFrames):
    @pytest.fixture
    def jitter_frames_obj(self, pulses_frames_obj):
        return JitterFrames.from_pitch_pulse_frames(pulses_frames_obj)

    @pytest.fixture
    def frames_scope(self, jitter_frames_obj):
        return jitter_frames_obj

    def test_jitter(self, jitter_frames_obj):
        jitter = jitter_frames_obj.frames
        assert jitter.shape == jitter_frames_obj.ts.shape == jitter_frames_obj.idx.shape
        assert np.all(np.logical_or(jitter > 0, np.isnan(jitter)))

    def test_calc_jitter_frame(self, pulses_frames_obj, jitter_frames_obj):
        jitter_frame = jitter_frames_obj._calc_jitter_frame(
            pulses_frames_obj.frames[1],
            rel=True,
            lower=0.0001,
            upper=0.02,
            max_period_ratio=1.3,
        )
        assert isinstance(jitter_frame, float)
        assert jitter_frame > 0 or np.isnan(jitter_frame)


class TestShimmerFrames(TestPitchPulseFrames):
    @pytest.fixture
    def shimmer_frames_obj(self, pulses_frames_obj):
        return ShimmerFrames.from_pitch_pulse_frames(pulses_frames_obj)

    @pytest.fixture
    def frames_scope(self, shimmer_frames_obj):
        return shimmer_frames_obj

    def test_shimmer(self, shimmer_frames_obj):
        shimmer = shimmer_frames_obj.frames
        assert (
            shimmer.shape == shimmer_frames_obj.ts.shape == shimmer_frames_obj.idx.shape
        )
        assert np.all(np.logical_or(shimmer > 0, np.isnan(shimmer)))

    def test_calc_shimmer_frame(self, pulses_frames_obj, shimmer_frames_obj):
        shimmer_frame = shimmer_frames_obj._calc_shimmer_frame(
            pulses_frames_obj.frames[1],
            rel=True,
            lower=0.0001,
            upper=0.02,
            max_period_ratio=1.3,
            max_amp_factor=1.6,
        )
        assert isinstance(shimmer_frame, float)
        assert shimmer_frame > 0 or np.isnan(shimmer_frame)

    def test_get_amplitude(self, pulses_frames_obj, shimmer_frames_obj):
        _, mask = shimmer_frames_obj._calc_period_length(
            pulses_frames_obj.frames[1], 0.0001, 0.02
        )
        amps = shimmer_frames_obj._get_amplitude(pulses_frames_obj.frames[1], mask)
        assert isinstance(amps, list)


class TestHnrFrames(TestBaseFrames):
    @pytest.fixture
    def hnr_frames_obj(self, sig_frames_obj):
        return HnrFrames.from_frames(sig_frames_obj)
    
    @pytest.fixture
    def frames_scope(self, hnr_frames_obj):
        return hnr_frames_obj
    

    def test_hnr(self, hnr_frames_obj):
        hnr = hnr_frames_obj.frames
        assert hnr.shape == hnr_frames_obj.ts.shape == hnr_frames_obj.idx.shape
        assert np.all(np.logical_or(10 ** (hnr / 10) > 0, np.isnan(hnr)))


    def test_find_max_peak(self, hnr_frames_obj):
        sig = (1 + 0.3 * np.sin(2 * np.pi * 140 * np.linspace(0, 1, self.frame_len)))
        autocor = librosa.autocorrelate(sig)
        max_peak = hnr_frames_obj._find_max_peak(autocor, 44100, 75.0)
        assert max_peak == autocor.max()


    def test_find_max_peak_all_below_threshold(self, hnr_frames_obj):
        sig = (1 + 0.3 * np.sin(2 * np.pi * 0 * np.linspace(0, 1, self.frame_len)))
        autocor = librosa.autocorrelate(sig)
        max_peak = hnr_frames_obj._find_max_peak(autocor, 44100, 75.0)
        assert np.isnan(max_peak)
