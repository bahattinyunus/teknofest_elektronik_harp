import numpy as np
import logging

class BayesianDecisionSupport:
    """
    Implements Bayesian Risk Analysis for Electronic Warfare.
    Evaluates whether to engage (jam) a target based on probability of detection 
    and mission importance.
    """
    def __init__(self):
        # Prior probabilities (Hypothesis: Target is Hostile vs Friendly)
        self.p_hostile = 0.5
        self.p_friendly = 0.5
        
        # Costs (Risk)
        # Cost of False Alarm (Jamming a friendly)
        self.cost_fa = 100 
        # Cost of Miss (Not jamming a hostile)
        self.cost_miss = 150
        # Cost of Jamming (Resource consumption / detection risk)
        self.cost_action = 10

    def evaluate_risk(self, ai_confidence, predicted_label):
        """
        Decision Rule: Act if Risk(Action) < Risk(No Action)
        """
        # Likelihoods based on AI confidence
        if predicted_label in ["Pulsed_Radar", "LPI_Radar", "FHSS"]:
            p_evidence_hostile = ai_confidence
            p_evidence_friendly = 1 - ai_confidence
        else:
            p_evidence_hostile = 1 - ai_confidence
            p_evidence_friendly = ai_confidence
            
        # Bayesian Update (Posterior)
        p_h_obs = (p_evidence_hostile * self.p_hostile) / (p_evidence_hostile * self.p_hostile + p_evidence_friendly * self.p_friendly + 1e-9)
        
        # Risk Calculation
        risk_jam = (1 - p_h_obs) * self.cost_fa + self.cost_action
        risk_stay_silent = p_h_obs * self.cost_miss
        
        should_jam = risk_jam < risk_stay_silent
        
        return {
            "should_jam": should_jam,
            "posterior_hostile_prob": p_h_obs,
            "risk_score": min(risk_jam, risk_stay_silent)
        }

class DynamicResourceManager:
    """
    Allocates transmission power and bandwidth across multiple targets.
    Optimizes the 140W (Aegis-AI v3.0) power limit.
    """
    def __init__(self, max_power_w=140):
        self.max_power_w = max_power_w
        self.active_targets = {}

    def allocate_resources(self, target_list):
        """
        target_list: List of dicts with {'id', 'threat_level', 'bandwidth_req'}
        threat_level: 1 (Low) to 10 (Critical)
        """
        if not target_list:
            return {}

        total_threat = sum(t['threat_level'] for t in target_list)
        allocations = {}
        
        for t in target_list:
            # Proportional allocation based on threat level
            power_allocated = (t['threat_level'] / total_threat) * self.max_power_w
            
            # Efficiency check: Avoid sub-threshold jamming
            if power_allocated < 5: # Min 5W to be effective
                power_allocated = 0
                
            allocations[t['id']] = {
                "power_w": round(power_allocated, 2),
                "is_active": power_allocated > 0
            }
            
        return allocations

if __name__ == "__main__":
    adss = BayesianDecisionSupport()
    decision = adss.evaluate_risk(0.92, "Pulsed_Radar")
    print(f"Decision: {'JAM' if decision['should_jam'] else 'SILENT'}")
    print(f"Hostile Probability: {decision['posterior_hostile_prob']:.2f}")
    
    rm = DynamicResourceManager()
    targets = [
        {'id': 'T1', 'threat_level': 8},
        {'id': 'T2', 'threat_level': 3},
        {'id': 'T3', 'threat_level': 5}
    ]
    resource_plan = rm.allocate_resources(targets)
    print(f"Resource Plan: {resource_plan}")
