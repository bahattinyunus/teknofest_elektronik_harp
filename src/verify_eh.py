import sys
import os
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor, DirectionFinder
from jamming_logic.jammers import NoiseJammer, SpoofingJammer, FrequencyHoppingJammer
from ai_engine.classifier import SignalClassifier
from ai_engine.autonomy_manager import AutonomyManager

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

    # 4. Test ET Signal Generation
    print("\n[4] Testing Spoofing Jammer...")
    spoof = SpoofingJammer()
    _, spoof_signal = spoof.generate_jamming_signal(0.001)
    print(f"Spoofing Signal Min/Max: {np.min(spoof_signal):.2f} / {np.max(spoof_signal):.2f}")

    print("\nVerification Complete.")

if __name__ == "__main__":
    test_eh_system()
