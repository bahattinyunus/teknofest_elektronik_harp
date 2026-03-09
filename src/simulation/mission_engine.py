import numpy as np
import time

class MissionEngine:
    """
    Simulates a dynamic operational environment with moving emitters
    and evolving signal characteristics.
    """
    def __init__(self):
        self.emitters = [
            {"id": "E1", "type": "Radar_L",   "base_freq": 1.3e9,  "pos": [100, 100],  "velocity": [5,  -2]},
            {"id": "E2", "type": "Comm_Link", "base_freq": 2.4e9,  "pos": [-50, 200],  "velocity": [-3, 10]},
            {"id": "E3", "type": "LPI_Radar", "base_freq": 9.5e9,  "pos": [300, -100], "velocity": [-8,  3]},
            {"id": "E4", "type": "Radar_FC",  "base_freq": 15.5e9, "pos": [200, 50],   "velocity": [10, -5]},
        ]
        self.start_time = time.time()

    def add_emitter(self, emitter_id, emitter_type, freq, pos, velocity):
        """Dynamically add a new emitter to the simulation."""
        self.emitters.append({
            "id": emitter_id, "type": emitter_type,
            "base_freq": freq, "pos": pos, "velocity": velocity
        })

    def remove_emitter(self, emitter_id):
        """Remove an emitter from the simulation by ID."""
        self.emitters = [e for e in self.emitters if e["id"] != emitter_id]

    def update_environment(self):
        """
        Updates positions of emitters and returns current observation data.
        """
        dt = 1.0 # Simulate 1 second per tick
        observations = []
        
        for e in self.emitters:
            # Update position: p = p + v*dt
            e["pos"][0] += e["velocity"][0] * dt
            e["pos"][1] += e["velocity"][1] * dt
            
            # Calculate Bearing from Origin (Sensor Position)
            bearing = np.degrees(np.arctan2(e["pos"][0], e["pos"][1]))
            bearing = (bearing + 360) % 360
            
            # Add some measurement noise
            noisy_bearing = bearing + np.random.normal(0, 2.0)
            
            observations.append({
                "id": e["id"],
                "type": e["type"],
                "freq": e["base_freq"] + np.random.normal(0, 1e6),
                "bearing": noisy_bearing,
                "signal_strength": 100.0 / (np.linalg.norm(e["pos"]) + 1)
            })
            
        return observations

    def get_mission_summary(self):
        return {
            "active_emitters": len(self.emitters),
            "mission_time": time.time() - self.start_time,
            "emitter_types": list(set(e["type"] for e in self.emitters)),
            "complexity": "High" if len(self.emitters) >= 4 else "Medium"
        }

if __name__ == "__main__":
    engine = MissionEngine()
    for _ in range(5):
        obs = engine.update_environment()
        print(f"Step Observation: {obs}")
        time.sleep(0.5)
