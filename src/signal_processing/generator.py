import numpy as np

class SignalGenerator:
    """
    Simulates RF signal generation for testing purposes.
    Supports: CW, Noise, CHIRP (FMCW), BPSK, QPSK, Pulsed
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def _t(self, duration):
        return np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)

    def generate_cw(self, frequency, duration, amplitude=1.0):
        """Generates a Continuous Wave (CW) sinusoidal signal."""
        t = self._t(duration)
        return t, amplitude * np.sin(2 * np.pi * frequency * t)

    def generate_noise(self, duration, noise_level=0.1):
        """Generates Gaussian white noise."""
        t = self._t(duration)
        return t, np.random.normal(0, noise_level, len(t))

    def generate_chirp(self, f_start, f_end, duration, amplitude=1.0):
        """
        Generates an FMCW (Linear Chirp) signal — the primary waveform
        of LPI radars. Frequency sweeps linearly from f_start to f_end.
        """
        t = self._t(duration)
        k = (f_end - f_start) / duration  # chirp rate [Hz/s]
        phase = 2 * np.pi * (f_start * t + 0.5 * k * t**2)
        return t, amplitude * np.cos(phase)

    def generate_bpsk(self, carrier_freq, bit_rate, duration, amplitude=1.0):
        """
        Generates Binary Phase Shift Keying (BPSK) signal.
        Random bit sequence modulated onto the carrier.
        """
        t = self._t(duration)
        samples_per_bit = int(self.sample_rate / bit_rate)
        num_bits = int(np.ceil(len(t) / samples_per_bit))
        bits = np.random.choice([-1, 1], size=num_bits)
        bit_stream = np.repeat(bits, samples_per_bit)[:len(t)]
        carrier = np.cos(2 * np.pi * carrier_freq * t)
        return t, amplitude * bit_stream * carrier

    def generate_qpsk(self, carrier_freq, symbol_rate, duration, amplitude=1.0):
        """
        Generates Quadrature Phase Shift Keying (QPSK) signal.
        Two bits per symbol: I and Q components.
        """
        t = self._t(duration)
        samples_per_sym = int(self.sample_rate / symbol_rate)
        num_syms = int(np.ceil(len(t) / samples_per_sym))
        # Random QPSK symbols: phases = {45, 135, 225, 315} degrees
        phases = np.random.choice([np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4], size=num_syms)
        phase_stream = np.repeat(phases, samples_per_sym)[:len(t)]
        carrier = amplitude * np.cos(2 * np.pi * carrier_freq * t + phase_stream)
        return t, carrier

    def generate_pulsed(self, carrier_freq, pri, pw, duration, amplitude=1.0):
        """
        Generates a pulsed radar waveform with given PRI and PW.
        """
        t = self._t(duration)
        signal = np.zeros(len(t))
        carrier = np.cos(2 * np.pi * carrier_freq * t)
        pulse_mask = (t % pri) < pw
        signal[pulse_mask] = amplitude * carrier[pulse_mask]
        return t, signal

    def add_signals(self, signal1, signal2):
        """Adds two signals together (must be same length)."""
        if len(signal1) != len(signal2):
            raise ValueError("Signals must be of the same length to add.")
        return signal1 + signal2
