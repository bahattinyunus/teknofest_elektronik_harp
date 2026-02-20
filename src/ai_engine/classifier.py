import numpy as np

class SignalClassifier:
    """
    AI-driven signal classification and parameter extraction.
    Currently uses heuristic features, ready for deep learning model integration.
    """
    def __init__(self):
        self.labels = ["Noise", "CW", "BPSK", "QPSK", "FM"]

    def extract_features(self, freqs, magnitudes):
        """
        Extracts basic features from the power spectrum.
        """
        peak_idx = np.argmax(magnitudes)
        peak_freq = freqs[peak_idx]
        peak_mag = magnitudes[peak_idx]
        
        # Bandwidth estimation (simplified)
        threshold = peak_mag * 0.5
        occupied_indices = np.where(magnitudes > threshold)[0]
        bandwidth = freqs[occupied_indices[-1]] - freqs[occupied_indices[0]] if len(occupied_indices) > 0 else 0
        
        return {
            "peak_freq": peak_freq,
            "peak_mag": peak_mag,
            "bandwidth": bandwidth
        }

    def predict(self, features):
        """
        Simulated classification logic.
        In production, this would be a loaded .pth or .h5 deep learning model.
        """
        # Heuristic rules for demo
        if features["peak_mag"] < 0.2:
            return "Noise"
        
        if features["bandwidth"] < 5000: # Narrow band
            return "CW"
        
        if 5000 <= features["bandwidth"] < 50000:
            return "BPSK"
        
        return "QPSK" # Wide band fallback
