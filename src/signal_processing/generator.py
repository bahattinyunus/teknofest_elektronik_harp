import numpy as np

class SignalGenerator:
    """
    Simulates RF signal generation for testing purposes.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def generate_cw(self, frequency, duration, amplitude=1.0):
        """
        Generates a Continuous Wave (CW) sinusoidal signal.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        return t, amplitude * np.sin(2 * np.pi * frequency * t)

    def generate_noise(self, duration, noise_level=0.1):
        """
        Generates Gaussian white noise.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        return t, np.random.normal(0, noise_level, len(t))

    def add_signals(self, signal1, signal2):
        """
        Adds two signals together (must be same length).
        """
        if len(signal1) != len(signal2):
            raise ValueError("Signals must be of the same length to add.")
        return signal1 + signal2
