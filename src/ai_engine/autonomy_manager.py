import time
from .threat_library import ThreatLibrary

# Risk score mapping for threat types
RISK_SCORES = {
    "Radar_FC": 10,     # Fire Control Radar = Highest threat
    "LPI_Radar": 9,
    "Radar_L":   6,
    "FHSS":      7,
    "Comm_Link": 4,
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
            # Simple threshold: only jam risks >= 5 or if specifically prioritized
            if self.risk_score >= 5 or label in ["Radar_FC", "LPI_Radar", "FHSS", "Analog_Telsiz"]:
                jam_key = label.lower()
                # Specialized logic for Interleaved Jamming
                if strategy == "InterleavedJamming":
                    self.jammer_coord.assign_jammer("T1", "adaptive", self.risk_score)
                elif "Spoofing" in strategy:
                    self.jammer_coord.assign_jammer("T1", "spoofing", self.risk_score)
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
        
        return {
            "risk_score": max_risk,
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
