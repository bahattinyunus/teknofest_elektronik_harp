"""
Unit test suite for Aegis-AI Electronic Warfare System.
Run with: pytest tests/ -v
"""
import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor, DirectionFinder
from signal_processing.generator import SignalGenerator
from signal_processing.tracking import KalmanFilterDOA
from signal_processing.lpi_detector import LPIDetector
from ai_engine.classifier import SignalClassifier
from ai_engine.autonomy_manager import AutonomyManager
from jamming_logic.jammers import NoiseJammer, SpoofingJammer, FrequencyHoppingJammer

SR = 1e6  # Sample rate


# ============================================================
# Signal Processing Tests
# ============================================================
class TestSpectrumAnalyzer:
    def test_fft_output_shape(self):
        gen = SignalGenerator(SR)
        _, sig = gen.generate_cw(100e3, 0.01)
        ana = SpectrumAnalyzer(SR)
        freqs, mags = ana.compute_fft(sig)
        assert len(freqs) == len(mags)
        assert freqs[0] >= 0

    def test_peak_detection(self):
        gen = SignalGenerator(SR)
        _, sig = gen.generate_cw(100e3, 0.01)
        ana = SpectrumAnalyzer(SR)
        freqs, mags = ana.compute_fft(sig)
        peaks = ana.detect_peaks(freqs, mags, threshold=0.1)
        assert len(peaks) > 0

class TestParameterExtractor:
    def test_pri_extraction(self):
        t = np.linspace(0, 0.01, 10000)
        sig = np.zeros_like(t)
        for i in range(5):
            s = i * 2000 + 500
            sig[s:s+100] = 1.0
        ext = ParameterExtractor(SR)
        params = ext.estimate_parameters(sig)
        assert params["PRI"] is not None
        assert params["PW"] is not None

class TestDirectionFinder:
    def test_north_bearing(self):
        df = DirectionFinder()
        angle = df.estimate_doa([1.0, 0.0, 0.0, 0.0])
        # Strong North signal -> angle should be near 0 or 360
        norm = angle % 360
        assert norm < 20 or norm > 340

    def test_east_bearing(self):
        df = DirectionFinder()
        angle = df.estimate_doa([0.0, 1.0, 0.0, 0.0])
        assert 80 < angle < 100

class TestKalmanFilter:
    def test_tracking_convergence(self):
        kf = KalmanFilterDOA()
        target_angle = 45.0
        for _ in range(20):
            noisy = target_angle + np.random.normal(0, 5)
            kf.predict()
            state = kf.update(noisy)
        # After 20 updates, should be close to target
        assert abs(state[0] - target_angle) < 15.0


# ============================================================
# Signal Generator Tests
# ============================================================
class TestSignalGenerator:
    def test_chirp_generation(self):
        gen = SignalGenerator(SR)
        t, sig = gen.generate_chirp(50e3, 200e3, 0.005)
        assert len(t) == len(sig)
        assert np.max(np.abs(sig)) <= 1.01

    def test_bpsk_generation(self):
        gen = SignalGenerator(SR)
        t, sig = gen.generate_bpsk(100e3, 10e3, 0.005)
        assert len(sig) > 0

    def test_qpsk_generation(self):
        gen = SignalGenerator(SR)
        t, sig = gen.generate_qpsk(100e3, 5e3, 0.005)
        assert len(sig) > 0

    def test_pulsed_generation(self):
        gen = SignalGenerator(SR)
        t, sig = gen.generate_pulsed(100e3, 1e-3, 100e-6, 0.01)
        assert np.sum(sig != 0) > 0


# ============================================================
# LPI Detector Tests
# ============================================================
class TestLPIDetector:
    def test_chirp_detected(self):
        gen = SignalGenerator(SR)
        _, chirp = gen.generate_chirp(10e3, 400e3, 0.01)
        det = LPIDetector(SR)
        result = det.detect_all(chirp)
        assert result["stft_chirp"]["detected"] == True

    def test_noise_not_detected(self):
        gen = SignalGenerator(SR)
        _, noise = gen.generate_noise(0.01, noise_level=0.05)
        det = LPIDetector(SR)
        result = det.energy_detection(noise, threshold_db=-10.0)
        assert result["detected"] == False


# ============================================================
# Jamming Tests
# ============================================================
class TestJammers:
    def test_noise_jammer(self):
        j = NoiseJammer(SR)
        t, sig = j.generate_jamming_signal(0.001)
        assert len(sig) > 0

    def test_spoofing_jammer(self):
        j = SpoofingJammer(SR)
        t, sig = j.generate_jamming_signal(0.001)
        assert np.max(np.abs(sig)) > 0

    def test_fh_jammer(self):
        j = FrequencyHoppingJammer(SR)
        j.set_hop_sequence([100e3, 200e3, 300e3])
        t, sig = j.generate_jamming_signal(0.001, current_hop_index=1)
        assert len(sig) > 0


# ============================================================
# AI Engine Tests
# ============================================================
class TestSignalClassifier:
    def test_classify_noise(self):
        clf = SignalClassifier()
        features = {"peak_freq": 0, "peak_mag": 0.05, "bandwidth": 0}
        label = clf.predict(features)
        assert label == "Noise"

    def test_classify_cw(self):
        clf = SignalClassifier()
        features = {"peak_freq": 100e3, "peak_mag": 0.9, "bandwidth": 1000}
        label = clf.predict(features)
        assert label == "CW"

class TestAutonomyManager:
    def test_strategy_selection(self):
        clf = SignalClassifier()
        mgr = AutonomyManager(clf, {})
        freqs = np.linspace(0, 500e3, 1000)
        mags = np.zeros(1000)
        mags[200] = 0.9
        strategy = mgr.process_detection(freqs, mags)
        assert isinstance(strategy, str)
