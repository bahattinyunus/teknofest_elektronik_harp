from .threat_library import ThreatLibrary

class AutonomyManager:
    """
    Autonomous Decision Support System (ADSS).
    Decides the best action based on classified signals.
    """
    def __init__(self, classifier, jammers_map):
        self.classifier = classifier
        self.jammers = jammers_map
        self.active_strategy = None

    def process_detection(self, freqs, magnitudes, signal_params=None):
        """
        Analyzes detected signal and activates the best jammer.
        """
        features = self.classifier.extract_features(freqs, magnitudes)
        label = self.classifier.predict(features)
        
        # Consult Threat Library
        strategy = ThreatLibrary.get_countermeasure(label)
        self.active_strategy = strategy
        
        print(f"[Autonomy] Detected: {label} -> Selected Strategy: {strategy}")
        
        # In a real system, this would trigger the actual hardware or simulator
        return strategy

    def get_system_status(self):
        return {
            "last_strategy": self.active_strategy,
            "status": "Operational"
        }
