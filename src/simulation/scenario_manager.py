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
        elif scenario_name == "LPI Stealth Radar":
            # FMCW Chirp — Low Probability of Intercept
            n = int(self.sample_rate * duration)
            t = np.linspace(0, duration, n)
            f_start, f_end = 50e3, 400e3
            # Linear chirp: instantaneous freq increases from f_start to f_end
            chirp = np.cos(2 * np.pi * (f_start * t + ((f_end - f_start) / (2 * duration)) * t**2))
            # Add Gaussian noise to make interception harder
            chirp += np.random.normal(0, 0.15, n)
            return t, chirp
        elif scenario_name == "Fire Control Radar":
            # X-band equivalent: 480kHz (scaled), very short PRI (0.15ms), narrow PW (2us)
            return self.generate_pulse_stream(480e3, 0.15e-3, 2e-6, duration, amplitude=0.95)
        elif scenario_name == "GNSS Satellite":
            # GPS L1-like signal (Wide bandwidth, high carrier)
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            carrier = np.cos(2 * np.pi * 150e3 * t)
            # PRN code modulation (simulated by random bits)
            prn_code = np.repeat(np.random.choice([-1, 1], int(duration * 1.023e6)), 
                                 max(1, int(self.sample_rate / 1.023e6)))
            prn_code = prn_code[:len(t)]
            return t, carrier * prn_code + np.random.normal(0, 0.05, len(t))
        elif scenario_name == "Analog Telsiz":
            # FM Voice signal
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            voice = np.sin(2 * np.pi * 1e3 * t) # 1kHz tone simulation
            fm_signal = np.cos(2 * np.pi * 120e3 * t + 5.0 * np.cumsum(voice) / self.sample_rate)
            return t, fm_signal + np.random.normal(0, 0.05, len(t))
        elif scenario_name == "Drone Swarm":
            # 8 Nodes communicating at ~350kHz
            return self.generate_swarm_signal(8, duration, base_freq=350e3)
        elif scenario_name == "Cognitive Radar":
            # Radar that shifts freq in response to detection (simulated as rapid random agility)
            n = int(self.sample_rate * duration)
            t = np.linspace(0, duration, n)
            # Freq agility: 50 frequency steps per frame
            freqs = np.random.uniform(100e3, 400e3, 50)
            samples_per_step = n // 50
            signal = np.zeros(n)
            for i in range(50):
                s, e = i * samples_per_step, (i+1) * samples_per_step
                signal[s:e] = np.cos(2 * np.pi * freqs[i] * t[s:e])
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
