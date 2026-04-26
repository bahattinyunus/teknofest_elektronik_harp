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

    def calculate_rms_power(self, signal):
        """Calculates RMS power of the time-domain signal."""
        return np.sqrt(np.mean(np.square(np.abs(signal))))

    def compute_stft(self, signal, nperseg=256, noverlap=128):
        """
        Computes Short-Time Fourier Transform (STFT).
        Useful for LPI (FMCW) detection where frequency changes over time.
        """
        from scipy.signal import stft
        f, t, Zxx = stft(signal, fs=self.sample_rate, nperseg=nperseg, noverlap=noverlap)
        return f, t, np.abs(Zxx)

    def detect_peaks(self, frequencies, magnitudes, threshold=0.5):
        """
        Detects peaks in the frequency domain above a certain threshold.
        Returns a list of (frequency, magnitude) tuples.
        """
        peaks = []
        for f, m in zip(frequencies, magnitudes):
            if m > threshold:
                peaks.append((f, m))
        return peaks

class ParameterExtractor:
    """
    Extracts tactical parameters like PRI, PW, and Duty Cycle from pulses.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def estimate_parameters(self, time_domain_signal):
        """
        Estimates PRI (Pulse Repetition Interval), PW (Pulse Width), Center Frequency, 
        and Signal Type (Analog vs Digital).
        """
        # Simple threshold-based pulse detection
        threshold = np.max(np.abs(time_domain_signal)) * 0.4
        pulses = np.abs(time_domain_signal) > threshold
        
        # Find rising and falling edges
        diff = np.diff(pulses.astype(int))
        rising_edges = np.where(diff == 1)[0]
        falling_edges = np.where(diff == -1)[0]
        
        if len(rising_edges) < 1 or len(falling_edges) < 1:
            return {"PRI": None, "PW": None, "CenterFreq": None, "DutyCycle": None}
            
        # Ensure we have pairs of edges
        min_len = min(len(rising_edges), len(falling_edges))
        pws = (falling_edges[:min_len] - rising_edges[:min_len]) / self.sample_rate
        
        # Estimate Center Frequency from the first pulse (simplified)
        center_freq = 0
        if len(rising_edges) > 0:
            pulse_segment = time_domain_signal[rising_edges[0]:falling_edges[0]]
            if len(pulse_segment) > 8:
                # Use FFT on the pulse to find its dominant frequency
                N = len(pulse_segment)
                yf = fft(pulse_segment)
                xf = fftfreq(N, 1 / self.sample_rate)
                idx = np.argmax(np.abs(yf[:N//2]))
                center_freq = np.abs(xf[idx])

        pris = np.diff(rising_edges) / self.sample_rate if len(rising_edges) > 1 else [0]
        
        # Analog vs Digital Detection (Kurtosis-based)
        envelope = np.abs(time_domain_signal)
        mean_env = np.mean(envelope) + 1e-12
        std_env = np.std(envelope)
        kurtosis = np.mean(((envelope - mean_env) / (std_env + 1e-12))**4)
        signal_type = "Analog" if kurtosis > 3.5 else "Digital"

        # Multiplexing & ECCM Detection (TERCİHEN requirements)
        multiplexing = self.detect_multiplexing(time_domain_signal)
        eccm = self.detect_dsss(time_domain_signal)

        return {
            "PRI": np.mean(pris) if len(pris) > 0 else 0,
            "PW": np.mean(pws) if len(pws) > 0 else 0,
            "Bandwidth": 1.0 / np.mean(pws) if len(pws) > 0 and np.mean(pws) > 0 else 0,
            "CenterFreq": center_freq,
            "DutyCycle": (np.mean(pws) / np.mean(pris)) * 100 if len(pris) > 0 and np.mean(pris) > 0 else 0,
            "SignalType": signal_type,
            "Multiplexing": multiplexing,
            "ECCM": eccm,
            "Power_RMS": np.sqrt(np.mean(envelope**2))
        }

    def detect_multiplexing(self, signal):
        """
        Heuristic detection for TDMA, FDMA, CDMA, OFDM.
        """
        N = len(signal)
        yf = np.abs(fft(signal))
        # OFDM: Flat spectrum with sharp edges
        # CDMA: Direct Sequence like noise-like wide spectrum
        # TDMA: Burst energy in time domain
        # FDMA: Multichannel spectral peaks
        
        # Check for multiple peaks (FDMA)
        peaks = np.where(yf[0:N//2] > np.max(yf) * 0.6)[0]
        if len(peaks) > 3:
            return "FDMA"
            
        # Check for OFDM (Flatness over bandwidth)
        # Using Spectral Flatness Ratio
        spectral_flatness = np.exp(np.mean(np.log(yf + 1e-12))) / (np.mean(yf) + 1e-12)
        if spectral_flatness > 0.7:
            return "OFDM"
            
        return "None"

    def detect_dsss(self, signal):
        """
        Detects Direct Sequence Spread Spectrum (DSSS) by looking for 
        low Peak-to-Average Power Ratio (PAPR) characteristics typical of 
        spread spectrum signals.
        """
        envelope = np.abs(signal)
        if len(envelope) == 0: return "None"
        
        # Calculate Peak-to-Average Power Ratio (PAPR)
        papr = np.max(envelope**2) / (np.mean(envelope**2) + 1e-12)
        
        # DSSS and other spread spectrum signals typically have lower PAPR 
        # compared to pulsed or intermittent signals.
        return "DSSS" if papr < 15.0 else "None"

class AnalogDemodulator:
    """
    Simulates Demodulation of Analog Voice (AM/FM).
    Required for "Sinyal Dinleme" task (Section 5.1.3).
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def demodulate(self, signal, mode="FM", carrier_freq=120e3):
        """
        Performs basic AM/FM demodulation.
        Returns 'audio' signal (envelope or frequency deviation).
        """
        if mode == "AM":
            # Envelope detector
            return np.abs(signal)
        else: # FM
            # Differentiator + Envelope
            diff_sig = np.diff(signal)
            return np.abs(diff_sig)

class SigMFExporter:
    """
    Exports captured signals in a format compatible with the SigMF standard.
    (Section 5.1.3: Sinyal Kayıt ve Veri Formatı)
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def export(self, signal, filename_prefix="capture"):
        import json
        import os
        import time

        os.makedirs("captures", exist_ok=True)
        timestamp = int(time.time())
        
        # Meta file (.sigmf-meta)
        metadata = {
            "global": {
                "core:datatype": "cf32_le",
                "core:sample_rate": self.sample_rate,
                "core:version": "0.1.0",
                "core:description": "Almasta-AI Tactical Capture"
            },
            "captures": [
                {
                    "core:sample_start": 0,
                    "core:frequency": 150000.0, # Center frequency placeholder
                    "core:datetime": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                }
            ],
            "annotations": []
        }

        meta_path = f"captures/{filename_prefix}_{timestamp}.sigmf-meta"
        data_path = f"captures/{filename_prefix}_{timestamp}.sigmf-data"

        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=4)

        # Data file (.sigmf-data)
        # Convert to complex32 (IQ) and save as binary
        iq_signal = signal.astype(np.complex64)
        iq_signal.tofile(data_path)

        return meta_path, data_path

class DirectionFinder:
    """
    Simulates Direction of Arrival (DoA) estimation for a 12-antenna circular array.
    """
    def __init__(self, num_antennas=12, radius=0.15):
        self.num_antennas = num_antennas
        self.radius = radius # Array radius in meters
        # Approximate spacing between adjacent elements for phase calcs
        self.antenna_spacing = 2 * radius * np.sin(np.pi / num_antennas)
        # Define antenna positions in degrees (360 / 12 = 30 degree increments)
        self.antenna_angles = np.linspace(0, 360, num_antennas, endpoint=False)

    def estimate_doa_amplitude(self, signal_strengths):
        """
        Estimates the angle of arrival based on relative signal strengths from 12 Vivaldi antennas.
        Uses a centroid/weighted average approach across the 3 strongest adjacent antennas.
        """
        if len(signal_strengths) != self.num_antennas:
            return 0.0
            
        # Find the peak antenna
        peak_idx = np.argmax(signal_strengths)
        
        # Consider the peak and its neighbors for interpolation
        idx_minus = (peak_idx - 1) % self.num_antennas
        idx_plus  = (peak_idx + 1) % self.num_antennas
        
        weights = np.array([signal_strengths[idx_minus], signal_strengths[peak_idx], signal_strengths[idx_plus]])
        angles  = np.array([self.antenna_angles[idx_minus], self.antenna_angles[peak_idx], self.antenna_angles[idx_plus]])
        
        # Handle 350-10 degree wrap-around
        if angles[0] > angles[2]: # Wrap around case
            if angles[1] < 180: # Peak is near 0
                angles[0] -= 360
            else: # Peak is near 360
                angles[2] += 360
        
        # Weighted average AoA
        norm_weights = weights / (np.sum(weights) + 1e-12)
        aoa = np.sum(angles * norm_weights)
        
        return (aoa + 360) % 360

    def estimate_doa_phase(self, phase_differences, wavelength):
        """
        Simulates Phase Interferometry DOA estimation for 2 antennas.
        phase_differences: phase difference in radians.
        wavelength: signal wavelength in meters.
        """
        # Phase diff = (2 * pi * d * sin(theta)) / lambda
        # sin(theta) = (Phase diff * lambda) / (2 * pi * d)
        val = (phase_differences * wavelength) / (2 * np.pi * self.antenna_spacing)
        
        # Clamp value to [-1, 1] to avoid mathematical errors
        val = max(-1.0, min(1.0, val))
        
        angle = np.degrees(np.arcsin(val))
        return angle
