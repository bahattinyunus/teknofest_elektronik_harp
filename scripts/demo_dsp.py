import numpy as np
import matplotlib.pyplot as plt
from src.signal_processing.generator import SignalGenerator
from src.signal_processing.analyzer import SpectrumAnalyzer

def main():
    # Parameters
    sample_rate = 1e6 # 1 MHz
    duration = 0.001 # 1 ms
    freq_target = 50e3 # 50 kHz
    
    # Initialize modules
    gen = SignalGenerator(sample_rate)
    sa = SpectrumAnalyzer(sample_rate)
    
    # 1. Generate Signal
    print(f"Generating {freq_target/1e3} kHz CW signal...")
    t, cw_signal = gen.generate_cw(freq_target, duration)
    
    # 2. Add Noise
    print("Adding noise...")
    _, noise = gen.generate_noise(duration, noise_level=0.5)
    mixed_signal = gen.add_signals(cw_signal, noise)
    
    # 3. Analyze Spectrum
    print("Computing FFT...")
    freqs, mags = sa.compute_fft(mixed_signal)
    
    # 4. Detect Peaks
    print("Detecting peaks...")
    peaks = sa.detect_peaks(freqs, mags, threshold=0.4)
    
    print("\n--- Detection Results ---")
    for f, m in peaks:
        print(f"Detected Peak: {f/1e3:.2f} kHz (Magnitude: {m:.2f})")
        
    # Validation
    found = any(abs(f - freq_target) < 1000 for f, m in peaks)
    if found:
        print("\nSUCCESS: Target frequency detected!")
    else:
        print("\nFAILURE: Target frequency NOT detected.")

if __name__ == "__main__":
    main()
