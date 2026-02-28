import sys
import os
import numpy as np

# Add root to path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor, DirectionFinder
from src.signal_processing.lpi_detector import LPIDetector
from src.jamming_logic.jammers import NoiseJammer, SpoofingJammer, FrequencyHoppingJammer
from src.ai_engine.classifier import SignalClassifier
from src.ai_engine.autonomy_manager import AutonomyManager

def test_eh_system():
    print("--- TEKNOFEST 2026 EH System Verification ---")
    
    # 1. Test Parameter Extraction
    print("\n[1] Testing Parameter Extraction...")
    extractor = ParameterExtractor(sample_rate=1e6)
    # Generate 5 pulses
    t = np.linspace(0, 0.01, 10000)
    signal = np.zeros_like(t)
    for i in range(5):
        start = i * 2000 + 500
        end = start + 500
        signal[start:end] = 1.0
    
    params = extractor.estimate_parameters(signal)
    print(f"Extracted Params: {params}")

    # 2. Test Direction Finding
    print("\n[2] Testing Direction Finding...")
    df = DirectionFinder()
    # Signal stronger in North and East
    strengths = [0.9, 0.7, 0.1, 0.2] # N, E, S, W
    angle = df.estimate_doa(strengths)
    print(f"Estimated DOA Angle: {angle:.2f}°")

    # 3. Test Autonomy & Jamming
    print("\n[3] Testing Autonomy Manager...")
    classifier = SignalClassifier()
    autonomy = AutonomyManager(classifier, {})
    
    # Mock spectrum for a "CW" signal (low bandwidth)
    freqs = np.linspace(0, 500000, 1000)
    mags = np.zeros_like(freqs)
    mags[500] = 1.0 # One sharp peak
    
    strategy = autonomy.process_detection(freqs, mags)
    print(f"Autonomy Strategy: {strategy}")

    # 5. Test LPI Detection
    print("\n[5] Testing LPI Detector (FMCW Chirp)...")
    lpi_detector = LPIDetector(sample_rate=1e6)
    # Generate a chirp signal
    t_lpi = np.linspace(0, 0.001, 1000)
    # Linear FMCW chirp
    chirp_signal = np.cos(2 * np.pi * (100e3 * t_lpi + 50e6 * t_lpi**2))
    lpi_results = lpi_detector.detect_all(chirp_signal)
    print(f"LPI Detection Results: {lpi_results['final_verdict']} ({lpi_results['confidence']})")

    print("\nVerification Complete.")

if __name__ == "__main__":
    test_eh_system()
