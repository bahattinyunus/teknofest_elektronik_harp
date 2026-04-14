import numpy as np
from abc import ABC, abstractmethod
from ..signal_processing.drfm import DRFMKernel

class JammerBase(ABC):
    """
    Abstract base class for all Electronic Attack (ET) / Jamming modules.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate
        self.power_dbm = 20.0  # Default output power in dBm

    @abstractmethod
    def generate_jamming_signal(self, duration, **kwargs):
        pass

    def set_power(self, dbm):
        """Sets the jamming power in dBm."""
        self.power_dbm = dbm
    
    def _get_amplitude(self):
        """Converts power in dBm to a normalized amplitude."""
        return 10 ** ((self.power_dbm - 20.0) / 20.0)

class NoiseJammer(JammerBase):
    """
    Implements Spot Noise Jamming (targeted bandwidth).
    """
    def generate_jamming_signal(self, duration, noise_level=1.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude() * noise_level
        return t, np.random.normal(0, amplitude, len(t))

class BarrageJammer(JammerBase):
    """
    Implements wideband Barrage Jamming.
    Covers a wide range of frequencies simultaneously. (Section 3.1)
    """
    def generate_jamming_signal(self, duration, bandwidth_mhz=10.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude()
        # White noise across full sampling bandwidth
        return t, np.random.normal(0, amplitude, len(t))

class MultiToneJammer(JammerBase):
    """
    Emits multiple discrete CW tones to jam specific frequencies efficiently.
    """
    def generate_jamming_signal(self, duration, tones_hz=[100e3, 200e3, 300e3]):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude() / len(tones_hz)
        signal = np.zeros_like(t)
        for f in tones_hz:
            signal += np.sin(2 * np.pi * f * t)
        return t, amplitude * signal

class AdaptiveNoiseJammer(NoiseJammer):
    """
    Electronic attack that adapts power based on detected threat severity.
    Automatically scales dBm up for higher risk threats.
    """
    def generate_jamming_signal(self, duration, threat_risk=5):
        # Scale power: risk 0-10 -> +0 to +10 dB boost
        boost = max(0, (threat_risk - 5) * 2.0)
        original_power = self.power_dbm
        self.set_power(original_power + boost)
        
        t, signal = super().generate_jamming_signal(duration)
        
        # Reset power for next cycle
        self.set_power(original_power)
        return t, signal

class SmartJammer(JammerBase):
    """
    Look-through Jamming: Cycles between listening and jamming to track target.
    """
    def __init__(self, sample_rate=1e6, look_ratio=0.2):
        super().__init__(sample_rate)
        self.look_ratio = look_ratio  # Fraction of time spent listening
        self.active = False

    def generate_jamming_signal(self, duration, target_detected=False, power_boost=2.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        if target_detected:
            self.active = True
            amplitude = self._get_amplitude() * power_boost
            signal = np.zeros_like(t)
            jam_end = int(len(t) * (1.0 - self.look_ratio))
            signal[:jam_end] = np.random.normal(0, amplitude, jam_end)
            return t, signal
        else:
            self.active = False
            return t, np.zeros_like(t)

class SpoofingJammer(JammerBase):
    """
    DRFM Based Spoofing prototype (Legacy).
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.rgpo_delay_us = 10.0
        self.rgpo_rate = 1.5

    def generate_jamming_signal(self, duration, pulse_delay=None, doppler_shift_hz=0.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        delay_s = (pulse_delay if pulse_delay else self.rgpo_delay_us * 1e-6)
        self.rgpo_delay_us += self.rgpo_rate
        carrier_freq = 150e3
        carrier_with_doppler = carrier_freq + doppler_shift_hz
        fake_echo = np.sin(2 * np.pi * carrier_with_doppler * (t - delay_s))
        envelope = np.exp(-((t - delay_s)**2) / (2 * (5e-6)**2))
        fake_signal = self._get_amplitude() * fake_echo * envelope
        return t, fake_signal

    def reset_rgpo(self):
        self.rgpo_delay_us = 10.0

class DRFMJammer(JammerBase):
    """
    Advanced Deception Jammer using Digital Radio Frequency Memory (DRFM).
    Leverages captured target waveforms to generate coherent false targets.
    
    Aegis-AI OMEGA: v3.0.0
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.kernel = DRFMKernel(sample_rate=sample_rate)
        self.is_primed = False

    def prime_with_signal(self, capture_signal):
        """Captures a target signal to 'prime' the DRFM memory."""
        self.kernel.capture(capture_signal)
        self.is_primed = True

    def generate_jamming_signal(self, duration, technique="rgpo", **kwargs):
        """
        Produces deception signal based on target waveform.
        Techniques: 'rgpo', 'vgpo', 'combined'
        """
        if not self.is_primed:
            return np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False), \
                   np.random.normal(0, 0.1, int(self.sample_rate * duration))

        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        duration_ms = duration * 1000
        
        if technique == "rgpo":
            delay = kwargs.get("delay_ms", 5.0)
            signal = self.kernel.generate_rgpo(delay, duration_ms)
        elif technique == "vgpo":
            shift = kwargs.get("freq_shift_hz", 1000.0)
            signal = self.kernel.generate_vgpo(shift, duration_ms)
        else: # combined
            delay = kwargs.get("delay_ms", 5.0)
            shift = kwargs.get("freq_shift_hz", 1000.0)
            signal = self.kernel.generate_combined_deception(delay, shift, duration_ms)

        amplitude = self._get_amplitude()
        return t, amplitude * signal

class FrequencyHoppingJammer(JammerBase):
    """
    FHSS Tracking and Jamming.
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.hop_sequence = []
        self.detected_hops = []
        self.dwell_time_s = 0.001

    def set_hop_sequence(self, sequence):
        self.hop_sequence = sequence

    def detect_and_learn_hop(self, freqs, magnitudes, threshold=0.4):
        peak_idx = np.argmax(magnitudes)
        peak_mag  = magnitudes[peak_idx]
        peak_freq = freqs[peak_idx]
        if peak_mag > threshold:
            self.detected_hops.append(peak_freq)
            if len(self.detected_hops) > 20:
                self.detected_hops.pop(0)
            return True, peak_freq
        return False, 0.0

    def predict_next_hop(self):
        if len(self.detected_hops) < 2:
            return None
        deltas = np.diff(self.detected_hops)
        avg_delta = np.mean(deltas)
        return self.detected_hops[-1] + avg_delta

    def generate_jamming_signal(self, duration, current_hop_index=0, target_freq=None):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude()
        freq = target_freq
        if freq is None:
            if self.hop_sequence and current_hop_index < len(self.hop_sequence):
                freq = self.hop_sequence[current_hop_index]
            elif self.detected_hops:
                freq = self.predict_next_hop() or self.detected_hops[-1]
        if freq:
            noise = np.random.normal(0, amplitude, len(t))
            modulated_noise = noise * np.cos(2 * np.pi * freq * t)
            return t, modulated_noise
        return t, np.zeros_like(t)

class GNSSJammer(JammerBase):
    """GPS L1 Deception."""
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.gps_l1_freq = 150e3

    def generate_jamming_signal(self, duration, target_lat=39.9, target_lon=32.8):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude()
        combined_gps = np.zeros_like(t)
        for i in range(4):
            fake_phase = (target_lat * 0.1 + target_lon * 0.05 + i * 0.25) * np.pi
            combined_gps += np.sin(2 * np.pi * self.gps_l1_freq * t + fake_phase)
        return t, (amplitude * combined_gps / 4.0)

class AnalogVoiceJammer(JammerBase):
    """Analog Voice Spoofing."""
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.carrier_freq = 120e3

    def generate_jamming_signal(self, duration, mode="FM", message_freq=1e3):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude()
        message = np.sin(2 * np.pi * message_freq * t) + 0.2 * np.random.normal(0, 1, len(t))
        if mode == "AM":
            signal = (1 + 0.8 * message) * np.cos(2 * np.pi * self.carrier_freq * t)
        else: # FM
            signal = np.cos(2 * np.pi * self.carrier_freq * t + 5.0 * message)
        return t, amplitude * signal

class JammerCoordinator:
    """
    Orchestrates multiple jamming assets.
    """
    def __init__(self, sample_rate=1e6):
        self.jammers = {
            "noise": NoiseJammer(sample_rate),
            "adaptive": AdaptiveNoiseJammer(sample_rate),
            "spoofing": SpoofingJammer(sample_rate),
            "fhss": FrequencyHoppingJammer(sample_rate),
            "gnss": GNSSJammer(sample_rate),
            "analog": AnalogVoiceJammer(sample_rate),
            "barrage": BarrageJammer(sample_rate),
            "multitone": MultiToneJammer(sample_rate),
            "drfm": DRFMJammer(sample_rate)
        }
        self.active_assignments = {}
        self.swarm_mode = False

    def assign_jammer(self, threat_id, threat_type, risk_score):
        if threat_type == "LPI_Radar":
            self.active_assignments[threat_id] = ("adaptive", risk_score)
        elif threat_type == "Radar_FC":
            self.active_assignments[threat_id] = ("drfm", risk_score)
        elif threat_type == "FHSS":
            self.active_assignments[threat_id] = ("fhss", risk_score)
        elif threat_type == "GNSS":
            self.active_assignments[threat_id] = ("gnss", risk_score)
        elif threat_type == "Analog_Telsiz":
            self.active_assignments[threat_id] = ("analog", risk_score)
        else:
            self.active_assignments[threat_id] = ("noise", risk_score)

    def enable_swarm_suppression(self, active=True):
        self.swarm_mode = active

    def generate_combined_signal(self, duration, look_through_active=True):
        N = int(self.jammers["noise"].sample_rate * duration)
        combined_signal = np.zeros(N)
        time_axis = np.linspace(0, duration, N, endpoint=False)
        if not self.active_assignments:
            return time_axis, combined_signal
        look_start_idx = int(N * 0.9) if look_through_active else N
        for threat_id, (jammer_key, risk) in self.active_assignments.items():
            jammer = self.jammers[jammer_key]
            if jammer_key == "adaptive":
                _, s = jammer.generate_jamming_signal(duration, threat_risk=risk)
            elif jammer_key == "fhss":
                _, s = jammer.generate_jamming_signal(duration, target_freq=150e3)
            elif jammer_key == "drfm":
                # DRFM needs priming in real use, but for combined signal we generate dummy deception
                _, s = jammer.generate_jamming_signal(duration, technique="combined")
            else:
                _, s = jammer.generate_jamming_signal(duration)
            combined_signal += s
        if look_through_active:
            combined_signal[look_start_idx:] = 0.0
        return time_axis, combined_signal
