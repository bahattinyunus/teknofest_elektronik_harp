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
