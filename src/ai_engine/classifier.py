import numpy as np
import logging

try:
    from ai_engine.dl_classifier import DummyDLClassifier, TORCH_AVAILABLE
except ImportError:
    try:
        from src.ai_engine.dl_classifier import DummyDLClassifier, TORCH_AVAILABLE
    except ImportError:
        TORCH_AVAILABLE = False

class SignalClassifier:
    """
    AI-driven signal classification using spectrum AND pulse parameter features.
    Currently uses heuristic rule engine, designed for deep learning model plug-in.
    """
    def __init__(self, use_dl=False):
        self.labels = ["Noise", "CW", "BPSK", "QPSK", "Pulsed_Radar", "FHSS", "LPI_Radar", "GNSS", "Analog_Telsiz"]
        
        self.use_dl = use_dl and TORCH_AVAILABLE
        self.dl_model = None
        if self.use_dl:
            self.dl_model = DummyDLClassifier()
            if self.dl_model.model is None:
                self.use_dl = False
                logging.warning("DL model requested but failed to initialize. Falling back to heuristics.")
            else:
                logging.info("DL model successfully initialized in SignalClassifier.")

    def extract_features(self, freqs, magnitudes):
        """
        Extracts basic spectral features from the power spectrum.
        """
        peak_idx = np.argmax(magnitudes)
        peak_freq = freqs[peak_idx]
        peak_mag = magnitudes[peak_idx]

        # Bandwidth estimation: -3 dB occupancy
        threshold = peak_mag * 0.5
        occupied_indices = np.where(magnitudes > threshold)[0]
        bandwidth = freqs[occupied_indices[-1]] - freqs[occupied_indices[0]] if len(occupied_indices) > 1 else 0

        # Spectral flatness (ratio of geometric to arithmetic mean) — detects FHSS
        eps = 1e-12
        spectral_flatness = np.exp(np.mean(np.log(magnitudes + eps))) / (np.mean(magnitudes) + eps)

        return {
            "peak_freq": peak_freq,
            "peak_mag": peak_mag,
            "bandwidth": bandwidth,
            "spectral_flatness": spectral_flatness
        }

    def predict(self, features, pulse_params=None, magnitudes=None):
        """
        Multi-feature classification with confidence score.
        Uses spectral features and optional pulse parameters.
        If use_dl=True and magnitudes provided, delegates to PyTorch CNN.
        Returns (label, confidence).
        """
        if self.use_dl and magnitudes is not None and self.dl_model is not None:
            dl_label, dl_conf = self.dl_model.predict_from_magnitudes(magnitudes)
            if dl_label:
                # Still fallback to heuristics if DL prediction confidence is garbage or noise 
                # (since it's a dummy un-trained model right now)
                
                # We can fuse: If DL says BPSK (conf 0.9), take it. For now, since weights 
                # are random, we will prioritize heuristics if DL confidence is low, 
                # but we prove the inference pipeline works.
                if dl_conf > 0.4:  
                    return dl_label, dl_conf

        pm = features["peak_mag"]
        bw = features["bandwidth"]
        sf = features.get("spectral_flatness", 0)

        # Pull pulse params if provided
        pri = pulse_params.get("PRI", 0) or 0 if pulse_params else 0
        pw  = pulse_params.get("PW", 0) or 0 if pulse_params else 0

        if pm < 0.15:
            return "Noise", 0.95

        # FHSS: flat spectrum + high bandwidth
        if sf > 0.6 and bw > 100e3:
            return "FHSS", 0.80

        # Pulsed radar: has PRI/PW structure
        if pulse_params and pri > 0 and pw > 0:
            duty_cycle = (pw / pri) * 100 if pri > 0 else 0
            if duty_cycle < 15:
                return "Pulsed_Radar", 0.88
            
        # Narrow CW tone
        if bw < 5000:
            return "CW", 0.90

        # BPSK / QPSK by bandwidth
        if bw < 35e3:
            return "BPSK", 0.75
        elif bw < 100e3:
            return "QPSK", 0.70

        # GNSS detection (constant high-bandwidth noise-like but structured)
        if bw > 250e3 and sf < 0.4:
            return "GNSS", 0.75

        # Analog Telsiz (Voice AM/FM)
        if pulse_params and pulse_params.get("SignalType") == "Analog":
            protocol = self.identify_protocol(features["peak_freq"], bw)
            return f"Analog_Telsiz ({protocol})", 0.85

        return "Unknown", 0.50

    def identify_protocol(self, freq, bw):
        """
        Map frequency/bandwidth to common protocols (PMR, Marine, etc.)
        """
        # Very simplified mapping for the simulation
        if 446e3 <= freq <= 446.2e3: return "PMR446"
        if 156e3 <= freq <= 162e3: return "Marine_VHF"
        if 868e3 <= freq <= 870e3: return "LoRa_EU868"
        return "Generic"
