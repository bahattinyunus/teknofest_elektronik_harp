import numpy as np

class ScenarioManager:
    """
    Generates realistic Electronic Warfare scenarios with pulses and noise.
    """
    def __init__(self, sample_rate=1e6):
        self.sample_rate = sample_rate

    def generate_pulse_stream(self, freq, pri, pw, duration, amplitude=1.0):
        """
        Generates a stream of pulses with specified frequency, PRI, and PW.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        signal = np.zeros_like(t)
        
        num_pulses = int(duration / pri)
        for i in range(num_pulses):
            start_time = i * pri
            end_time = start_time + pw
            
            if end_time > duration:
                break
                
            start_idx = int(start_time * self.sample_rate)
            end_idx = int(end_time * self.sample_rate)
            
            # Pulse carrier
            pulse_t = t[start_idx:end_idx]
            signal[start_idx:end_idx] = amplitude * np.cos(2 * np.pi * freq * pulse_t)
            
        return t, signal

    def generate_fhss_signal(self, hop_freqs, dwell_time, n_hops=None, amplitude=1.0):
        """
        Generates a Frequency Hopping Spread Spectrum (FHSS) signal.
        Hops through given frequencies using the specified dwell time per channel.
        """
        total_duration = dwell_time * (n_hops or len(hop_freqs))
        n_samples       = int(self.sample_rate * total_duration)
        t               = np.linspace(0, total_duration, n_samples)
        signal          = np.zeros(n_samples)
        samples_per_hop = int(self.sample_rate * dwell_time)

        hop_list = hop_freqs * (n_hops // len(hop_freqs) + 1) if n_hops else hop_freqs

        for i, freq in enumerate(hop_list[:n_hops or len(hop_list)]):
            start = i * samples_per_hop
            end   = min(start + samples_per_hop, n_samples)
            t_hop = t[start:end]
            signal[start:end] = amplitude * np.cos(2 * np.pi * freq * t_hop)

        return t, signal

    def generate_swarm_signal(self, n_emitters, duration, base_freq=200e3):
        """
        Simulates multiple Drone (UAV) emitters communicating in a cluster.
        Adds multi-path and slightly offset frequencies.
        """
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples)
        total_signal = np.zeros(n_samples)
        
        for i in range(n_emitters):
            # Each node has its own freq offset and phase
            freq = base_freq + (i * 2.5e3) 
            env = 0.5 + 0.5 * np.sin(2 * np.pi * 50 * t + i) # Rapid fading
            node_signal = env * np.cos(2 * np.pi * freq * t + (i * np.pi/4))
            total_signal += node_signal
            
        return t, total_signal / n_emitters

    def get_scenario_signal(self, scenario_name, duration=0.01):
        """
        Returns a signal based on predefined scenarios.
        Supported: Long Range Search, Tracking Radar, FHSS Comms,
                   LPI Stealth Radar, Fire Control Radar, Clear Sky.
        """
        if scenario_name == "Long Range Search":
            # 150kHz frequency, 2ms PRI, 100us PW
            return self.generate_pulse_stream(150e3, 2e-3, 100e-6, duration)
        elif scenario_name == "Tracking Radar":
            # 450kHz frequency, 0.4ms PRI, 5us PW
            return self.generate_pulse_stream(450e3, 0.4e-3, 5e-6, duration)
        elif scenario_name == "FHSS Comms":
            # Hops through 5 frequencies, 2ms dwell per hop
            hop_freqs = [100e3, 160e3, 220e3, 310e3, 380e3]
            n_hops    = max(1, int(duration / 0.002))
            return self.generate_fhss_signal(hop_freqs, dwell_time=0.002, n_hops=n_hops)
        elif scenario_name == "Swarm Incursion":
            # Coordinated swarm with 12 nodes, freq hopping and spatial spread
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            swarm_signal = np.zeros_like(t)
            for i in range(12):
                f_offset = np.random.uniform(-10e3, 10e3)
                phase = np.random.uniform(0, 2*np.pi)
                # Rapid fading to simulate multi-path/movement
                fading = 0.5 + 0.5 * np.sin(2 * np.pi * 15 * t + i)
                swarm_signal += fading * np.cos(2 * np.pi * (250e3 + f_offset) * t + phase)
            return t, swarm_signal / 12.0
        elif scenario_name == "LPI Stealth Radar":
            # Advanced FMCW Chirp — Low Probability of Intercept
            n = int(self.sample_rate * duration)
            t = np.linspace(0, duration, n)
            f_start, f_end = 50e3, 400e3
            # Non-linear chirp for better stealth
            chirp = np.cos(2 * np.pi * (f_start * t + 0.5 * ((f_end - f_start) / duration) * t**2 + 0.2 * np.sin(2*np.pi*100*t)))
            # Add Gaussian noise to make interception harder (Low SNR)
            chirp += np.random.normal(0, 0.4, n)
            return t, chirp
        elif scenario_name == "Cognitive Interference":
            # Jammer-resistant signal with random freq/phase/amplitude jumps
            n = int(self.sample_rate * duration)
            t = np.linspace(0, duration, n)
            signal = np.zeros(n)
            num_segments = 20
            seg_len = n // num_segments
            for i in range(num_segments):
                f = np.random.uniform(100e3, 450e3)
                amp = np.random.uniform(0.5, 1.0)
                signal[i*seg_len:(i+1)*seg_len] = amp * np.cos(2 * np.pi * f * t[i*seg_len:(i+1)*seg_len])
            return t, signal
        else:
            # Random noise (Clear Sky)
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            return t, np.random.normal(0, 0.1, int(self.sample_rate * duration))

    def export_dataset(self, scenario_name, num_samples, filename_prefix="dataset"):
        """
        Exports multiple signals of a scenario to a NumPy array for DL training.
        """
        import os
        import time
        
        logging_msg = f"Generating dataset for {scenario_name}..."
        print(logging_msg)
        dataset = []
        for _ in range(num_samples):
            # Vary duration slightly to add variance to the data
            dur = np.random.uniform(0.008, 0.012)
            t, signal = self.get_scenario_signal(scenario_name, duration=dur)
            dataset.append(signal)

        # Pad or truncate to a fixed size so we can stack
        ref_size = int(self.sample_rate * 0.01)
        dataset_padded = []
        for sig in dataset:
            if len(sig) > ref_size:
                dataset_padded.append(sig[:ref_size])
            else:
                dataset_padded.append(np.pad(sig, (0, ref_size - len(sig)), 'constant'))
                
        dataset_np = np.stack(dataset_padded)
        
        os.makedirs("data", exist_ok=True)
        filename = f"data/{filename_prefix}_{scenario_name.replace(' ', '_')}_{int(time.time())}.npy"
        np.save(filename, dataset_np)
        print(f"Exported {num_samples} samples to {filename}")
        return filename
