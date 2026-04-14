import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import spectrogram, hilbert
from scipy.stats import entropy

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
    def svd_detection(self, signal, singular_ratio_thresh=3.0):
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

        # Compare the dominant singular value to the average of the remaining (noise floor)
        noise_floor = np.mean(s[1:]) if len(s) > 1 else 1e-9
        ratio = s[0] / (noise_floor + 1e-9)
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

    # ---------------------------------------------------------------
    # Method 4: Wigner-Ville Distribution (WVD)
    # ---------------------------------------------------------------
    def wvd_detection(self, signal, wvd_threshold=50.0):
        """
        Pseudo Wigner-Ville Distribution (PWVD) based LPI detection.
        Provides ultra-high time-frequency resolution for detecting FMCW
        and Phase-coded LPI radar waveforms.
        """
        N = min(len(signal), 512) # Limit length for computational performance
        sig = signal[:N]
        
        # Compute analytic signal to avoid negative frequency interference
        analytic_signal = hilbert(sig)
        
        wvd_matrix = np.zeros((N, N), dtype=complex)
        
        for t in range(N):
            tau_max = min(t, N - 1 - t)
            tau = np.arange(-tau_max, tau_max + 1)
            # WVD kernel: x(t+tau) * x*(t-tau)
            wvd_matrix[t, tau_max + tau] = analytic_signal[t + tau] * np.conj(analytic_signal[t - tau])
            
        # FFT along the delay axis
        wvd = np.abs(fft(wvd_matrix, axis=1))
        
        # LPI signals compress energy tightly in the time-frequency plane.
        # We look for high peak-to-average concentration.
        peak_energy = np.max(wvd)
        mean_energy = np.mean(wvd) + 1e-9
        concentration_ratio = peak_energy / mean_energy
        
        detected = concentration_ratio > wvd_threshold
        
        return {
            "method": "wvd",
            "concentration_ratio": round(float(concentration_ratio), 2),
            "threshold": wvd_threshold,
            "detected": detected
        }

    # ---------------------------------------------------------------
    # Method 5: Spectral Entropy Detection
    # ---------------------------------------------------------------
    def entropy_detection(self, signal, entropy_threshold=0.85):
        """
        Calculates the normalized spectral entropy of the signal.
        LPI signals (like FMCW) often have structured (lower entropy) 
        distribution compared to pure white noise.
        """
        f, Pxx = np.abs(fft(signal)), np.abs(fft(signal))**2
        psd_norm = Pxx / np.sum(Pxx)
        
        # Shannon entropy
        S = entropy(psd_norm) / np.log(len(signal))
        
        # For LPI, we look for 'ordered' signals (lower entropy) 
        # but structured. Actually, most jamming is high entropy.
        # Radar signals are low entropy compared to noise.
        detected = S < entropy_threshold
        
        return {
            "method": "spectral_entropy",
            "entropy": round(float(S), 3),
            "threshold": entropy_threshold,
            "detected": detected
        }

    def detect_all(self, signal):
        """
        Runs all five detection methods and returns a combined verdict.
        """
        e = self.energy_detection(signal)
        s = self.svd_detection(signal)
        c = self.stft_chirp_detection(signal)
        w = self.wvd_detection(signal)
        en = self.entropy_detection(signal)

        votes = sum([e["detected"], s["detected"], c["detected"], w["detected"], en["detected"]])
        return {
            "energy": e,
            "svd": s,
            "stft_chirp": c,
            "wvd": w,
            "entropy": en,
            "final_verdict": "DETECTED" if votes >= 3 else "CLEAR",
            "confidence": votes / 5.0,
            "confidence_text": f"{votes}/5 methods triggered"
        }
