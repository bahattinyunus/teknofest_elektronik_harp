import numpy as np
from scipy.fft import fft, fftfreq

class SpectrumAnalyzer:
    """
    Performs spectral analysis on signals.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def compute_fft(self, signal):
        """
        Computes the Fast Fourier Transform (FFT) of the signal.
        Returns frequencies and magnitude spectrum.
        """
        N = len(signal)
        yf = fft(signal)
        xf = fftfreq(N, 1 / self.sample_rate)
        
        # Return only the positive frequencies
        return xf[:N//2], 2.0/N * np.abs(yf[0:N//2])

    def detect_peaks(self, frequencies, magnitudes, threshold=0.5):
        """
        Detects peaks in the frequency domain above a certain threshold.
        Returns a list of (frequency, magnitude) tuples.
        """
        peaks = []
        # Basic peak detection: check if value is above threshold
        # In a real scenario, this would include windowing and more robust logic
        for f, m in zip(frequencies, magnitudes):
            if m > threshold:
                peaks.append((f, m))
        
        # Filter close peaks (simple approach for now)
        # This is a placeholder for more advanced clustering/grouping
        return peaks
