"""
Unit test suite for Mergen-AI Electronic Warfare System.
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
from simulation.scenario_manager import ScenarioManager

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
        angle = df.estimate_doa_amplitude([1.0, 0.0, 0.0, 0.0])
        # Strong North signal -> angle should be near 0 or 360
        norm = angle % 360
        assert norm < 20 or norm > 340

    def test_east_bearing(self):
        df = DirectionFinder()
        angle = df.estimate_doa_amplitude([0.0, 1.0, 0.0, 0.0])
        assert 80 < angle < 100

    def test_phase_doa(self):
        df = DirectionFinder(antenna_spacing=0.5)
        angle = df.estimate_doa_phase(0.0, wavelength=1.0)
        assert abs(angle) < 1.0  # 0 phase diff -> 0 degrees

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
        _, noise = gen.generate_noise(0.01, noise_level=0.01)
        det = LPIDetector(SR)
        result = det.detect_all(noise)
        assert result["final_verdict"] == "CLEAR"

    def test_svd_detection(self):
        # SVD is good for low-rank signals (like CW in noise)
        gen = SignalGenerator(SR)
        _, sig = gen.generate_cw(100e3, 0.01, amplitude=1.0)
        det = LPIDetector(SR)
        res = det.svd_detection(sig)
        assert res["detected"] == True


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
        features = {"peak_freq": 0, "peak_mag": 0.05, "bandwidth": 0, "spectral_flatness": 0}
        label, conf = clf.predict(features)
        assert label == "Noise"
        assert conf > 0.8

    def test_classify_cw(self):
        clf = SignalClassifier()
        features = {"peak_freq": 100e3, "peak_mag": 0.9, "bandwidth": 1000, "spectral_flatness": 0.1}
        label, conf = clf.predict(features)
        assert label == "CW"
        assert conf > 0.7

    def test_classify_pulsed_radar(self):
        clf = SignalClassifier()
        features = {"peak_freq": 150e3, "peak_mag": 0.8, "bandwidth": 20000, "spectral_flatness": 0.2}
        pulse_params = {"PRI": 0.002, "PW": 0.0001, "CenterFreq": 150e3}
        label, conf = clf.predict(features, pulse_params=pulse_params)
        assert label == "Pulsed_Radar"

    def test_dl_classifier(self):
        clf = SignalClassifier(use_dl=True)
        # Assuming PyTorch is installed, this shouldn't crash.
        features = {"peak_freq": 150e3, "peak_mag": 0.8, "bandwidth": 20000, "spectral_flatness": 0.2}
        # Provide some dummy magnitudes representing an FFT
        mags = np.random.rand(1024)
        label, conf = clf.predict(features, pulse_params=None, magnitudes=mags)
        assert label is not None
        assert conf >= 0.0

class TestAutonomyManager:
    def test_strategy_selection(self):
        clf = SignalClassifier()
        lpi = LPIDetector(SR)
        mgr = AutonomyManager(clf, lpi, {})
        freqs = np.linspace(0, 500e3, 1000)
        mags = np.zeros(1000)
        mags[200] = 0.9
        strategy = mgr.process_detection(freqs, mags)
        assert isinstance(strategy, str)

    def test_lpi_priority_strategy(self):
        clf = SignalClassifier()
        lpi = LPIDetector(SR)
        mgr = AutonomyManager(clf, lpi, {})
        gen = SignalGenerator(SR)
        _, sig = gen.generate_chirp(100e3, 200e3, 0.01)
        freqs, mags = np.zeros(100), np.zeros(100)
        strategy = mgr.process_detection(freqs, mags, raw_signal=sig)
        assert strategy == "SmartJamming_LPI"

    def test_risk_assessment(self):
        clf = SignalClassifier()
        lpi = LPIDetector(SR)
        mgr = AutonomyManager(clf, lpi, {})
        result = mgr.risk_assessment()
        assert "risk_score" in result
        assert "threat_level" in result


# ============================================================
# Scenario Manager Tests
# ============================================================
class TestScenarioManager:
    def test_pulse_stream(self):
        sm = ScenarioManager(SR)
        t, sig = sm.generate_pulse_stream(150e3, 2e-3, 100e-6, 0.01)
        assert len(sig) > 0
        assert np.max(np.abs(sig)) > 0.1

    def test_fhss_signal(self):
        sm = ScenarioManager(SR)
        freqs = [100e3, 200e3, 300e3]
        t, sig = sm.generate_fhss_signal(freqs, dwell_time=0.002, n_hops=3)
        assert len(sig) > 0

    def test_scenario_lookup(self):
        sm = ScenarioManager(SR)
        _, sig = sm.get_scenario_signal("Long Range Search", duration=0.01)
        assert len(sig) > 0


# ============================================================
# FHSS Jammer Tests
# ============================================================
class TestFHSSJammer:
    def test_hop_learning(self):
        j = FrequencyHoppingJammer(SR)
        freqs = np.linspace(0, 500e3, 1000)
        mags = np.zeros(1000)
        mags[300] = 0.8  # Peak at 150 kHz
        detected, freq = j.detect_and_learn_hop(freqs, mags)
        assert detected is True
        assert freq > 0

    def test_hop_prediction(self):
        j = FrequencyHoppingJammer(SR)
        j.detected_hops = [100e3, 150e3, 200e3]
        predicted = j.predict_next_hop()
        assert abs(predicted - 250e3) < 10e3  # Should predict ~250 kHz
