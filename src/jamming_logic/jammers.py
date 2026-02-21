import numpy as np
from abc import ABC, abstractmethod

class JammerBase(ABC):
    """
    Abstract base class for all Electronic Attack (ET) / Jamming modules.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    @abstractmethod
    def generate_jamming_signal(self, duration):
        pass

class NoiseJammer(JammerBase):
    """
    Implements Barrage or Spot Noise Jamming.
    """
    def generate_jamming_signal(self, duration, noise_level=1.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        # Power is much higher than typical signals to overwhelm the receiver
        return t, np.random.normal(0, noise_level, len(t))

class SmartJammer(JammerBase):
    """
    Implements 'Look-through' Jamming: Only activates when a target signal is detected.
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.active = False

    def generate_jamming_signal(self, duration, target_detected=False, power_boost=2.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        if target_detected:
            self.active = True
            # Smart jamming often uses sweep or pulse noise tailored to the target
            return t, np.random.normal(0, power_boost, len(t))
        else:
            self.active = False
            return t, np.zeros_like(t)

class SpoofingJammer(JammerBase):
    """
    Deceives the receiver by generating fake signal patterns (e.g., false range/velocity).
    """
    def generate_jamming_signal(self, duration, pulse_delay=10e-6):
        """
        Generates a delayed version of a fake pulse to create false range targets.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        # Simulate a fake "echo" or signal
        fake_signal = np.sin(2 * np.pi * 100e3 * t) * np.exp(-((t - pulse_delay)**2) / (2 * (1e-6)**2))
        return t, fake_signal

class FrequencyHoppingJammer(JammerBase):
    """
    Follows and jams signals that jump between different frequencies.
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.hop_sequence = []

    def set_hop_sequence(self, sequence):
        self.hop_sequence = sequence

    def generate_jamming_signal(self, duration, current_hop_index=0):
        """
        Produces noise at the specific frequency where the target is expected to hop.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        if current_hop_index < len(self.hop_sequence):
            freq = self.hop_sequence[current_hop_index]
            # Targeted noise jamming at the hopping frequency
            noise = np.random.normal(0, 1.0, len(t))
            modulated_noise = noise * np.cos(2 * np.pi * freq * t)
            return t, modulated_noise
        return t, np.zeros_like(t)
