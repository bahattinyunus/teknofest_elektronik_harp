class ThreatLibrary:
    """
    Database of known threat signatures and their characteristics.
    """
    THREATS = {
        "Long Range Radar": {
            "label": "Radar_L",
            "freq_range": (1.2e9, 1.4e9),
            "pw_range": (50e-6, 100e-6),
            "countermeasure": "NoiseJamming"
        },
        "Fire Control Radar": {
            "label": "Radar_FC",
            "freq_range": (8e9, 12e9),
            "pw_range": (0.1e-6, 1e-6),
            "countermeasure": "Spoofing"
        },
        "Tactical Data Link": {
            "label": "Comm_Link",
            "freq_range": (2e9, 4e9),
            "modulation": "QPSK",
            "countermeasure": "SmartJamming"
        }
    }

    @staticmethod
    def get_countermeasure(label):
        for threat, data in ThreatLibrary.THREATS.items():
            if data["label"] == label:
                return data["countermeasure"]
        return "NoiseJamming" # Default
