import numpy as np
from scipy.signal import hilbert

class DRFMKernel:
    """
    Digital Radio Frequency Memory (DRFM) Kernel.
    Allows capturing, storing, and manipulating RF waveforms for deception jamming.
    
    Mergen-AI OMEGA Core: v3.0.0
    """

    def __init__(self, buffer_size=4096, sample_rate=1e6):
        self.buffer_size = buffer_size
        self.sample_rate = sample_rate
        self.memory = np.zeros(buffer_size, dtype=complex)
        self.is_captured = False

    def capture(self, signal):
        """Digitizes and stores the incoming signal."""
        n = min(len(signal), self.buffer_size)
        # Convert to analytic signal (baseband-like) for easier manipulation
        self.memory[:n] = hilbert(signal[:n])
        self.is_captured = True

    def generate_rgpo(self, delay_ms, duration_ms):
        """
        Range Gate Pull Off (RGPO).
        Generates a delayed version of the stored signal to create a false target.
        """
        if not self.is_captured:
            return np.zeros(int(duration_ms * self.sample_rate / 1000))

        delay_samples = int(delay_ms * self.sample_rate / 1000)
        output_len = int(duration_ms * self.sample_rate / 1000)
        
        # Simple cyclic shift or padding for delay
        output = np.roll(self.memory, delay_samples)
        
        # Return truncated or tiled version to match requested duration
        if output_len > self.buffer_size:
            output = np.tile(output, (output_len // self.buffer_size) + 1)[:output_len]
        else:
            output = output[:output_len]
            
        return np.real(output)

    def generate_vgpo(self, freq_shift_hz, duration_ms):
        """
        Velocity Gate Pull Off (VGPO).
        Generates a frequency-shifted version of the stored signal.
        """
        if not self.is_captured:
            return np.zeros(int(duration_ms * self.sample_rate / 1000))

        output_len = int(duration_ms * self.sample_rate / 1000)
        t = np.arange(output_len) / self.sample_rate
        
        # Base signal from memory
        base = np.tile(self.memory, (output_len // self.buffer_size) + 1)[:output_len]
        
        # Frequency shift: exp(j * 2 * pi * f_shift * t)
        shift_vec = np.exp(1j * 2 * np.pi * freq_shift_hz * t)
        output = base * shift_vec
        
        return np.real(output)

    def generate_combined_deception(self, delay_ms, freq_shift_hz, duration_ms):
        """Simultaneous Range and Velocity deception."""
        # First shift in time, then in frequency
        delayed = np.roll(self.memory, int(delay_ms * self.sample_rate / 1000))
        
        output_len = int(duration_ms * self.sample_rate / 1000)
        t = np.arange(output_len) / self.sample_rate
        
        base = np.tile(delayed, (output_len // self.buffer_size) + 1)[:output_len]
        shift_vec = np.exp(1j * 2 * np.pi * freq_shift_hz * t)
        
        return np.real(base * shift_vec)

    def generate_multi_target_deception(self, targets_params, duration_ms):
        """
        Simulates generating multiple false targets simultaneously.
        targets_params: List of dicts, e.g. [{"delay_ms": 5.0, "freq_shift_hz": 1000, "amplitude": 0.8}, ...]
        """
        if not self.is_captured or not targets_params:
            return np.zeros(int(duration_ms * self.sample_rate / 1000))

        output_len = int(duration_ms * self.sample_rate / 1000)
        t = np.arange(output_len) / self.sample_rate
        combined_output = np.zeros(output_len, dtype=complex)

        for params in targets_params:
            delay = params.get("delay_ms", 0.0)
            shift = params.get("freq_shift_hz", 0.0)
            amp = params.get("amplitude", 1.0)

            delayed = np.roll(self.memory, int(delay * self.sample_rate / 1000))
            base = np.tile(delayed, (output_len // self.buffer_size) + 1)[:output_len]
            shift_vec = np.exp(1j * 2 * np.pi * shift * t)
            
            combined_output += amp * (base * shift_vec)

        return np.real(combined_output)
