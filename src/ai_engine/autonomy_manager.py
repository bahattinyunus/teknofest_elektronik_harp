import time
from .threat_library import ThreatLibrary
from .swarm_engine import SwarmCorrelationEngine

# Risk score mapping for threat types
RISK_SCORES = {
    "Radar_FC": 10,     # Fire Control Radar = Highest threat
    "LPI_Radar": 9,
    "Radar_L":   6,
    "FHSS":      7,
    "Comm_Link": 4,
    "Swarm_Node": 8,    # NEW: Swarm detection
    "Analog_Telsiz": 5,
    "Unknown":   3,
    "Noise":     0,
}

class TacticalCOP:
    """
    Tactical Common Operating Picture.
    Tracks multiple emitters over time to maintain situational awareness.
    """
    def __init__(self):
        self.active_emitters = {} # emitter_id -> status_dict

    def update_emitter(self, label, params, aoa):
        emitter_id = f"{label}_{params.get('CenterFreq', 0):.0f}"
        if emitter_id not in self.active_emitters:
            self.active_emitters[emitter_id] = {
                "first_seen": time.time(),
                "hits": 0,
                "label": label
            }
        
        entry = self.active_emitters[emitter_id]
        entry["last_seen"] = time.time()
        entry["hits"] += 1
        entry["aoa"] = aoa
        entry["params"] = params
        
        return emitter_id

    def correlate_emitters(self):
        """
        Groups active emitters into clusters (e.g., Swarms).
        Returns a list of identified 'emitter groups'.
        """
        if not self.active_emitters:
            return []
            
        # Simplistic correlation based on proximity and timing
        groups = []
        # Logic: If 3 or more emitters have similar AOA (within 10 deg), label as Swarm
        emitters_list = list(self.active_emitters.values())
        if len(emitters_list) >= 3:
            aoas = [e.get('aoa', 0) for e in emitters_list if time.time() - e.get('last_seen', 0) < 2.0]
            if len(aoas) >= 3 and (max(aoas) - min(aoas)) < 15.0:
                groups.append({"type": "Swarm", "count": len(aoas), "avg_aoa": sum(aoas)/len(aoas)})
                
        return groups

class AutonomyManager:
    """
    Autonomous Decision Support System (ADSS) — Phase 2.
    Decides the best action based on classified signals with risk prioritization.
    """
    def __init__(self, classifier, lpi_detector, jammer_coordinator):
        self.classifier = classifier
        self.lpi_detector = lpi_detector
        self.jammer_coord = jammer_coordinator
        self.active_strategy = None
        self.threat_log = []       # Running log of detections
        self.tcop = TacticalCOP()
        self.swarm_engine = SwarmCorrelationEngine()
        self.risk_score = 0

    def process_detection(self, freqs, magnitudes, raw_signal=None, params=None):
        """
        Multi-sensor fusion: Spectrum classifier + LPI check + Parametric emitter ID.
        Returns the chosen EW countermeasure strategy.
        """
        # 1. Broad Spectrum Classification (now returns label + confidence)
        features = self.classifier.extract_features(freqs, magnitudes)
        result = self.classifier.predict(features, pulse_params=params)
        # Classifier can return (label, confidence) or just label (backwards compat)
        if isinstance(result, tuple):
            label, confidence = result
        else:
            label, confidence = result, 0.80

        # 2. Specialized LPI Check
        lpi_result = {"final_verdict": "CLEAR"}
        if raw_signal is not None:
            lpi_result = self.lpi_detector.detect_all(raw_signal)

        # 3. LPI Detection overrides classifier (higher priority)
        if lpi_result["final_verdict"] == "DETECTED":
            strategy  = "SmartJamming_LPI"
            label     = "LPI_Radar"
            threat_name = "LPI Threat Detected"
            confidence  = lpi_result.get("confidence", 0.90)
        elif params and params.get("PRI") and params.get("CenterFreq"):
            # 4. Parametric emitter identification
            threat_name, threat_data = ThreatLibrary.identify_emitter(params)
            strategy = threat_data["countermeasure"]
            label    = threat_data["label"]
        else:
            # 5. Fallback — use classifier result
            strategy = ThreatLibrary.get_countermeasure(label)
            threat_name = label

        # 6.5 Update Tactical COP
        emitter_id = self.tcop.update_emitter(label, params or {}, params.get('AoA', 0) if params else 0)

        self.risk_score = RISK_SCORES.get(label, 3)
        
        # Log the detection event
        self.threat_log.append({
            "threat": threat_name, "label": label,
            "strategy": strategy, "confidence": confidence,
            "risk": self.risk_score
        })
        if len(self.threat_log) > 50:
            self.threat_log.pop(0)

        self.active_strategy = strategy
        risk_str = "HIGH" if self.risk_score >= 8 else ("MED" if self.risk_score >= 5 else "LOW")
        
        # 7. Execute Strategy (Autonomous Mode)
        if self.jammer_coord:
            # Swarm Suppression Check (Using Advanced Swarm Engine)
            clusters = self.swarm_engine.analyze_emitters(self.tcop.active_emitters)
            if clusters:
                self.jammer_coord.enable_swarm_suppression(True)
                # Escalate risk if swarm detected
                self.risk_score = min(10, self.risk_score + 2)
                strategy = "SwarmSuppression_Active"
                threat_name = f"Swarm: {clusters[0]['dominant_threat']}"
                label = "Swarm_Node"
            
            # Simple threshold: only jam risks >= 5 or if specifically prioritized
            if self.risk_score >= 5 or label in ["Radar_FC", "LPI_Radar", "FHSS", "Analog_Telsiz", "Swarm_Node"]:
                jam_key = label.lower()
                # Specialized logic for Interleaved Jamming
                if strategy == "InterleavedJamming":
                    self.jammer_coord.assign_jammer("T1", "adaptive", self.risk_score)
                elif "Spoofing" in strategy or label == "Radar_FC":
                    # Radar_FC now triggers OMEGA DRFM deception
                    self.jammer_coord.assign_jammer("T1", "drfm", self.risk_score)
                elif label == "Analog_Telsiz":
                    self.jammer_coord.assign_jammer("T1", "analog", self.risk_score)
                else:
                    self.jammer_coord.assign_jammer("T1", "noise", self.risk_score)
            else:
                # Remove jammer if threat is low/noise
                if "T1" in self.jammer_coord.active_assignments:
                    del self.jammer_coord.active_assignments["T1"]

        # Ensure confidence is float for formatting
        conf_val = float(confidence) if confidence is not None else 0.0
        print(f"[ADSS] {threat_name} | Label: {label} | Risk: {risk_str} | Conf: {conf_val:.0%} -> {strategy}")

        return strategy

    def risk_assessment(self):
        """Returns the current threat environment risk score (0-10) with granular analysis."""
        if not self.threat_log:
            return {"risk_score": 0, "threat_level": "CLEAR"}
        
        recent = self.threat_log[-5:]  # Last 5 detections
        max_risk = max(e["risk"] for e in recent)
        avg_confidence = float(sum(e["confidence"] for e in recent) / len(recent))
        
        level = "CRITICAL" if max_risk >= 9 else ("HIGH" if max_risk >= 7 else ("MEDIUM" if max_risk >= 4 else "LOW"))
        
        # OMEGA: Weighted Bayesian Risk
        # (Prioritizes high-confidence threats)
        weighted_risk = sum(e["risk"] * e["confidence"] for e in recent) / (sum(e["confidence"] for e in recent) + 1e-9)

        return {
            "risk_score": round(weighted_risk, 2),
            "max_base_risk": max_risk,
            "threat_level": level,
            "avg_confidence": round(avg_confidence, 2),
            "threat_count": len(self.threat_log),
            "recent_threats": recent
        }

    def get_highest_priority_threat(self):
        """Analyzes recent threat log to identify the most dangerous active emitter."""
        if not self.threat_log:
            return None
        
        # Sort by risk (descending) and then confidence (descending)
        sorted_threats = sorted(self.threat_log, key=lambda x: (x['risk'], x['confidence']), reverse=True)
        return sorted_threats[0]

    def get_system_status(self):
        return {
            "last_strategy": self.active_strategy,
            "status": "Operational",
            "risk": self.risk_assessment()
        }
