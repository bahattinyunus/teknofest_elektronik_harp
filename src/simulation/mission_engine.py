import numpy as np
import time

class MissionEngine:
    """
    Simulates a dynamic operational environment with moving emitters
    and evolving signal characteristics.
    """
    def __init__(self):
        self.emitters = [
            {"id": "E1", "type": "Radar_L", "base_freq": 1.3e9, "pos": [100, 100], "velocity": [5, -2]},
            {"id": "E2", "type": "Comm_Link", "base_freq": 2.4e9, "pos": [-50, 200], "velocity": [-3, 10]}
        ]
        self.start_time = time.time()

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
            "complexity": "High"
        }

if __name__ == "__main__":
    engine = MissionEngine()
    for _ in range(5):
        obs = engine.update_environment()
        print(f"Step Observation: {obs}")
        time.sleep(0.5)
