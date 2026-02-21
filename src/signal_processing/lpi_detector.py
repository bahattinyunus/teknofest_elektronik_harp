import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import spectrogram

class LPIDetector:
    """
    Low Probability of Intercept (LPI) Radar Signal Detector.

    LPI radars are specifically designed to avoid conventional ESM receivers.
    They use techniques like FMCW (Frequency Modulated Continuous Wave),
    spread spectrum, and ultra-low peak power. This module applies
    time-frequency analysis to detect them.
    """

    def __init__(self, sample_rate=1e6, window_size=256):
        self.sample_rate = sample_rate
        self.window_size = window_size

    # ---------------------------------------------------------------
    # Method 1: Energy Detection (Radiometric)
    # ---------------------------------------------------------------
    def energy_detection(self, signal, threshold_db=-15.0):
        """
        Compares average signal energy against the noise floor.
        Returns True if a signal above threshold is detected.
        """
        power = np.mean(np.abs(signal) ** 2)
        power_db = 10 * np.log10(power + 1e-12)
        detected = power_db > threshold_db
        return {
            "method": "energy",
            "power_db": round(power_db, 2),
            "threshold_db": threshold_db,
            "detected": detected
        }

    # ---------------------------------------------------------------
    # Method 2: Singular Value Decomposition (SVD)
    # ---------------------------------------------------------------
    def svd_detection(self, signal, singular_ratio_thresh=10.0):
        """
        Constructs a Hankel matrix from the signal and decompose it with SVD.
        A large ratio between the first and second singular values indicates
        a coherent (LPI) signal embedded in noise.
        """
        N = len(signal)
        L = self.window_size
        K = N - L + 1
        if K <= 0:
            return {"method": "svd", "detected": False, "ratio": 0.0}

        # Build Hankel-like matrix
        H = np.array([signal[i:i+L] for i in range(K)])
        _, s, _ = np.linalg.svd(H, full_matrices=False)

        ratio = s[0] / (s[1] + 1e-9)
        detected = ratio > singular_ratio_thresh

        return {
            "method": "svd",
            "singular_ratio": round(float(ratio), 2),
            "threshold": singular_ratio_thresh,
            "detected": detected
        }

    # ---------------------------------------------------------------
    # Method 3: STFT (Short-Time Fourier Transform) Chirp Detection
    # ---------------------------------------------------------------
    def stft_chirp_detection(self, signal, chirp_bandwidth_thresh=50e3):
        """
        Analyses the time-frequency representation using STFT.
        Detects diagonal ridges (chirp signatures) in the spectrogram.
        """
        f, t, Sxx = spectrogram(signal, fs=self.sample_rate,
                                 nperseg=self.window_size, noverlap=self.window_size // 2)

        # Find peak frequency at each time step
        peak_freqs = f[np.argmax(Sxx, axis=0)]

        # Measure sweep bandwidth: range of peak frequencies
        bandwidth = np.max(peak_freqs) - np.min(peak_freqs)
        detected = bandwidth > chirp_bandwidth_thresh

        return {
            "method": "stft_chirp",
            "bandwidth_hz": round(float(bandwidth), 0),
            "threshold_hz": chirp_bandwidth_thresh,
            "detected": detected
        }

    def detect_all(self, signal):
        """
        Runs all three detection methods and returns a combined verdict.
        """
        e = self.energy_detection(signal)
        s = self.svd_detection(signal)
        c = self.stft_chirp_detection(signal)

        votes = sum([e["detected"], s["detected"], c["detected"]])
        return {
            "energy": e,
            "svd": s,
            "stft_chirp": c,
            "final_verdict": "DETECTED" if votes >= 2 else "CLEAR",
            "confidence": f"{votes}/3 methods triggered"
        }
