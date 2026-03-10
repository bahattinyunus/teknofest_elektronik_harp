import numpy as np
from abc import ABC, abstractmethod

class JammerBase(ABC):
    """
    Abstract base class for all Electronic Attack (ET) / Jamming modules.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate
        self.power_dbm = 20.0  # Default output power in dBm

    @abstractmethod
    def generate_jamming_signal(self, duration):
        pass

    def set_power(self, dbm):
        """Sets the jamming power in dBm."""
        self.power_dbm = dbm
    
    def _get_amplitude(self):
        """Converts power in dBm to a normalized amplitude."""
        return 10 ** ((self.power_dbm - 20.0) / 20.0)

class NoiseJammer(JammerBase):
    """
    Implements Barrage or Spot Noise Jamming.
    Effective against all radar types but easily detectable.
    """
    def generate_jamming_signal(self, duration, noise_level=1.0):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude() * noise_level
        return t, np.random.normal(0, amplitude, len(t))

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
    - During 'look' phase: receiver is active.
    - During 'jam' phase: full power jamming.
    This is more efficient than continuous barrage jamming.
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
            
            # Jam for (1-look_ratio) of the time, listen for look_ratio
            jam_end = int(len(t) * (1.0 - self.look_ratio))
            signal[:jam_end] = np.random.normal(0, amplitude, jam_end)
            # The remainder (look window) stays at zero so receiver can listen
            return t, signal
        else:
            self.active = False
            return t, np.zeros_like(t)


class SpoofingJammer(JammerBase):
    """
    DRFM (Digital Radio Frequency Memory) Based Spoofing.
    - Range Gate Pull-Off (RGPO): Creates a false range echo that gradually drifts.
    - Velocity Gate Pull-Off (VGPO): Simulates a false Doppler shift.
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.rgpo_delay_us = 10.0  # Microseconds — initial false range delay
        self.rgpo_rate = 1.5       # Microseconds per tick — drift rate

    def generate_jamming_signal(self, duration, pulse_delay=None, doppler_shift_hz=0.0):
        """
        Generates DRFM spoofing signal with RGPO and optional Doppler shift.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        
        # Use current RGPO delay if not specified
        delay_s = (pulse_delay if pulse_delay else self.rgpo_delay_us * 1e-6)
        
        # Drift the RGPO delay to lure the radar away
        self.rgpo_delay_us += self.rgpo_rate
        
        # Base carrier
        carrier_freq = 150e3  # Assume target radar at 150 kHz for sim
        # Apply VGPO Doppler shift
        carrier_with_doppler = carrier_freq + doppler_shift_hz
        
        # Delayed "echo" pulse with Doppler
        fake_echo = np.sin(2 * np.pi * carrier_with_doppler * (t - delay_s))
        # Amplitude envelope (Gaussian pulse shape)
        envelope = np.exp(-((t - delay_s)**2) / (2 * (5e-6)**2))
        fake_signal = self._get_amplitude() * fake_echo * envelope
        
        return t, fake_signal

    def reset_rgpo(self):
        """Resets the RGPO drift counter (start a new deception run)."""
        self.rgpo_delay_us = 10.0


class FrequencyHoppingJammer(JammerBase):
    """
    FHSS (Frequency Hopping Spread Spectrum) Tracking and Jamming.
    Detects the hop pattern from signal history and preemptively jams next hop.
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.hop_sequence = []
        self.detected_hops = []
        self.dwell_time_s = 0.001  # Default dwell time per hop

    def set_hop_sequence(self, sequence):
        self.hop_sequence = sequence

    def detect_and_learn_hop(self, freqs, magnitudes, threshold=0.4):
        """
        Detects a new hop frequency from a current spectrum snapshot.
        Stores it in the learned hop history.
        """
        peak_idx = np.argmax(magnitudes)
        peak_mag  = magnitudes[peak_idx]
        peak_freq = freqs[peak_idx]
        
        if peak_mag > threshold:
            self.detected_hops.append(peak_freq)
            if len(self.detected_hops) > 20:
                self.detected_hops.pop(0)  # Keep history window
            return True, peak_freq
        return False, 0.0

    def predict_next_hop(self):
        """
        Attempts to predict the next hop frequency using detected pattern.
        Returns the most likely next frequency.
        """
        if len(self.detected_hops) < 2:
            return None
        # Simple step-based prediction
        deltas = np.diff(self.detected_hops)
        avg_delta = np.mean(deltas)
        return self.detected_hops[-1] + avg_delta

    def generate_jamming_signal(self, duration, current_hop_index=0, target_freq=None):
        """
        Produces targeted noise jamming at the predicted or known hop frequency.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude()
        
        # Use predicted or known frequency
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
    """
    Implements GNSS (GPS L1) Deception / Spoofing.
    Simulates false positioning by emitting fake satellite signals.
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.gps_l1_freq = 150e3  # Scaled for simulation (Real is 1575.42 MHz)

    def generate_jamming_signal(self, duration, target_lat=39.9, target_lon=32.8):
        """
        Generates a spoofing signal that deceives the receiver into a false location.
        In this simulation, we modulate the time-of-flight phase.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude()
        
        # Simulate 4 "satellites" with slightly different phases to represent a position
        # Position is encoded in the relative phases (phi = 2*pi*f*d/c)
        combined_gps = np.zeros_like(t)
        for i in range(4):
            # Deterministic fake phase based on target coordinates
            fake_phase = (target_lat * 0.1 + target_lon * 0.05 + i * 0.25) * np.pi
            combined_gps += np.sin(2 * np.pi * self.gps_l1_freq * t + fake_phase)
            
        return t, (amplitude * combined_gps / 4.0)


class AnalogVoiceJammer(JammerBase):
    """
    Implements Analog Telsiz Aldatma (Spoofing).
    Modulates a carrier with fake voice/noise patterns.
    """
    def __init__(self, sample_rate=1e6):
        super().__init__(sample_rate)
        self.carrier_freq = 120e3 # FM/AM base frequency for sim

    def generate_jamming_signal(self, duration, mode="FM", message_freq=1e3):
        """
        Generates AM/FM modulated deception signals.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        amplitude = self._get_amplitude()
        
        # Fake "voice" signal (1kHz tone + noise)
        message = np.sin(2 * np.pi * message_freq * t) + 0.2 * np.random.normal(0, 1, len(t))
        
        if mode == "AM":
            # standard AM: (1 + m*cos(wm*t)) * cos(wc*t)
            signal = (1 + 0.8 * message) * np.cos(2 * np.pi * self.carrier_freq * t)
        else: # FM
            # standard FM: cos(wc*t + beta*sin(wm*t))
            integral_msg = -np.cos(2 * np.pi * message_freq * t) / (2 * np.pi * message_freq)
            signal = np.cos(2 * np.pi * self.carrier_freq * t + 5.0 * message)
            
        return t, amplitude * signal


class JammerCoordinator:
    """
    Orchestrates multiple jamming assets to handle multi-threat environments.
    Selects the best jammer/strategy for each target.
    """
    def __init__(self, sample_rate=1e6):
        self.jammers = {
            "noise": NoiseJammer(sample_rate),
            "adaptive": AdaptiveNoiseJammer(sample_rate),
            "spoofing": SpoofingJammer(sample_rate),
            "fhss": FrequencyHoppingJammer(sample_rate),
            "gnss": GNSSJammer(sample_rate),
            "analog": AnalogVoiceJammer(sample_rate)
        }
        self.active_assignments = {}

    def assign_jammer(self, threat_id, threat_type, risk_score):
        """Assigns a specific jammer to a threat based on its type."""
        if threat_type == "LPI_Radar":
            self.active_assignments[threat_id] = ("adaptive", risk_score)
        elif threat_type == "Radar_FC":
            self.active_assignments[threat_id] = ("spoofing", risk_score)
        elif threat_type == "FHSS":
            self.active_assignments[threat_id] = ("fhss", risk_score)
        elif threat_type == "GNSS":
            self.active_assignments[threat_id] = ("gnss", risk_score)
        elif threat_type == "Analog_Telsiz":
            self.active_assignments[threat_id] = ("analog", risk_score)
        else:
            self.active_assignments[threat_id] = ("noise", risk_score)

    def generate_combined_signal(self, duration):
        """Combines signals from all assigned jammers."""
        if not self.active_assignments:
            return np.linspace(0, duration, int(1e6 * duration), endpoint=False), np.zeros(int(1e6 * duration))
        
        combined_signal = None
        time_axis = None
        
        for jammer_key, risk in self.active_assignments.values():
            jammer = self.jammers[jammer_key]
            # Handle different method signatures
            if jammer_key == "adaptive":
                t, s = jammer.generate_jamming_signal(duration, threat_risk=risk)
            else:
                t, s = jammer.generate_jamming_signal(duration)
            
            if combined_signal is None:
                combined_signal = s
                time_axis = t
                combined_signal = combined_signal
            else:
                combined_signal += s
                
        return time_axis, combined_signal

