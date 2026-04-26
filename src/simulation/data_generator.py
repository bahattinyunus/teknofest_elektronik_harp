import numpy as np
import logging

class SignalChannelModel:
    """
    Advanced channel model for simulating realistic Electronic Warfare environments.
    Includes Rayleigh fading, Doppler shifts, and AWGN.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def apply_awgn(self, signal, snr_db):
        """
        Adds Additive White Gaussian Noise (AWGN) to the signal based on SNR.
        """
        sig_pow = np.mean(np.abs(signal)**2)
        snr_linear = 10**(snr_db / 10.0)
        noise_pow = sig_pow / snr_linear
        
        # Generates complex noise if signal is complex, else real noise
        if np.iscomplexobj(signal):
            noise = (np.random.normal(0, np.sqrt(noise_pow/2), len(signal)) + 
                     1j * np.random.normal(0, np.sqrt(noise_pow/2), len(signal)))
        else:
            noise = np.random.normal(0, np.sqrt(noise_pow), len(signal))
            
        return signal + noise

    def apply_rayleigh_fading(self, signal):
        """
        Applies Rayleigh fading (multipath) to the signal.
        """
        # Rayleigh channel coefficient: complex Gaussian with zero mean
        # Magnitude is Rayleigh distributed
        h = (np.random.normal(0, 1/np.sqrt(2)) + 1j * np.random.normal(0, 1/np.sqrt(2)))
        return signal * h

    def apply_doppler_shift(self, signal, velocity_ms, freq_carrier):
        """
        Applies Doppler shift based on relative velocity.
        f_d = (v / c) * f_c
        """
        c = 3e8 # Speed of light
        doppler_freq = (velocity_ms / c) * freq_carrier
        t = np.arange(len(signal)) / self.sample_rate
        shift = np.exp(1j * 2 * np.pi * doppler_freq * t)
        return signal * shift

class IQDataGenerator:
    """
    Generates complex I/Q baseband signals for various modulation types.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate
        self.channel = SignalChannelModel(sample_rate)

    def generate_bpsk(self, num_symbols, samples_per_symbol):
        """Generates a BPSK signal."""
        symbols = np.random.choice([-1, 1], num_symbols)
        iq_signal = np.repeat(symbols, samples_per_symbol).astype(complex)
        return iq_signal

    def generate_qpsk(self, num_symbols, samples_per_symbol):
        """Generates a QPSK signal."""
        symbols = np.random.choice([1+1j, 1-1j, -1+1j, -1-1j], num_symbols) / np.sqrt(2)
        iq_signal = np.repeat(symbols, samples_per_symbol).astype(complex)
        return iq_signal

    def generate_16qam(self, num_symbols, samples_per_symbol):
        """Generates a 16-QAM signal."""
        points = [-3, -1, 1, 3]
        symbols = []
        for _ in range(num_symbols):
            re = np.random.choice(points)
            im = np.random.choice(points)
            symbols.append(re + 1j*im)
        symbols = np.array(symbols) / np.sqrt(10) # Normalize energy
        iq_signal = np.repeat(symbols, samples_per_symbol).astype(complex)
        return iq_signal

    def get_labeled_batch(self, modulation_type, snr_db=20, num_samples=1024):
        """
        Generates a batch of labeled I/Q data with channel effects.
        """
        sps = 8 # Samples per symbol
        num_symbols = num_samples // sps
        
        if modulation_type == "BPSK":
            sig = self.generate_bpsk(num_symbols, sps)
        elif modulation_type == "QPSK":
            sig = self.generate_qpsk(num_symbols, sps)
        elif modulation_type == "16QAM":
            sig = self.generate_16qam(num_symbols, sps)
        else:
            sig = np.random.normal(0, 0.1, num_samples) + 1j * np.random.normal(0, 0.1, num_samples)
        
        # Apply channel effects
        sig = self.channel.apply_rayleigh_fading(sig)
        sig = self.channel.apply_awgn(sig, snr_db)
        
        return sig

if __name__ == "__main__":
    gen = IQDataGenerator()
    data = gen.get_labeled_batch("QPSK", snr_db=15)
    print(f"Generated {len(data)} samples of QPSK data with channel effects.")
