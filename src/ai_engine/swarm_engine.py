import numpy as np
import time
import logging

class SwarmCorrelationEngine:
    """
    Advanced engine for correlating multiple emitters into swarm patterns.
    Uses spatial (AOA), temporal (Arrival Time), and spectral (Frequency Hop) correlation.
    
    Mergen-AI OMEGA: v3.0.0
    """
    def __init__(self, angle_threshold=12.0, time_window=3.0, min_members=3):
        self.angle_threshold = angle_threshold
        self.time_window = time_window
        self.min_members = min_members
        self.logger = logging.getLogger("SwarmEngine")

    def analyze_emitters(self, active_emitters):
        """
        Identifies swarm clusters from a dictionary of active emitters.
        active_emitters: {id: {aoa, last_seen, label, params}}
        """
        if len(active_emitters) < self.min_members:
            return []

        now = time.time()
        # Filter recent emitters
        recent_emitters = [
            e for e in active_emitters.values() 
            if now - e.get('last_seen', 0) < self.time_window
        ]

        if len(recent_emitters) < self.min_members:
            return []

        clusters = []
        # Sort by AOA for easier windowed clustering
        sorted_emitters = sorted(recent_emitters, key=lambda x: x.get('aoa', 0))

        current_cluster = [sorted_emitters[0]]
        for i in range(1, len(sorted_emitters)):
            prev_aoa = sorted_emitters[i-1].get('aoa', 0)
            curr_aoa = sorted_emitters[i].get('aoa', 0)

            if abs(curr_aoa - prev_aoa) <= self.angle_threshold:
                current_cluster.append(sorted_emitters[i])
            else:
                if len(current_cluster) >= self.min_members:
                    clusters.append(self._process_cluster(current_cluster))
                current_cluster = [sorted_emitters[i]]
        
        # Check last group
        if len(current_cluster) >= self.min_members:
            clusters.append(self._process_cluster(current_cluster))

        return clusters

    def _process_cluster(self, members):
        """
        Extracts cluster-level metadata.
        """
        aoas = [m.get('aoa', 0) for m in members]
        avg_aoa = sum(aoas) / len(aoas)
        
        # Determine swarm type based on member labels
        labels = [m.get('label', 'Unknown') for m in members]
        dominant_label = max(set(labels), key=labels.count)
        
        return {
            "type": "Coordinated_Swarm",
            "member_count": len(members),
            "avg_aoa": round(avg_aoa, 2),
            "span_aoa": round(max(aoas) - min(aoas), 2),
            "dominant_threat": dominant_label,
            "risk_multiplier": 1.5 if dominant_label == "Pulsed_Radar" else 1.2
        }

    def predict_swarm_intent(self, cluster):
        """
        Heuristic-based intent estimation.
        """
        if cluster['member_count'] > 10:
            return "Saturation_Attack"
        if cluster['span_aoa'] < 5.0:
            return "Formation_Flight"
        return "Area_Surveillance"
