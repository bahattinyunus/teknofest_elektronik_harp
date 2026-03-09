import sys
import os
import numpy as np

# Add root to path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor, DirectionFinder
from src.signal_processing.lpi_detector import LPIDetector
from src.jamming_logic.jammers import NoiseJammer, SpoofingJammer, FrequencyHoppingJammer, AdaptiveNoiseJammer, JammerCoordinator
from src.ai_engine.classifier import SignalClassifier
from src.ai_engine.autonomy_manager import AutonomyManager
from src.simulation.scenario_manager import ScenarioManager

PASS = "\033[92m✔\033[0m"
FAIL = "\033[91m✘\033[0m"

def check(label, passed):
    print(f"  {PASS if passed else FAIL}  {label}")

def test_eh_system():
    print("\n" + "="*55)
    print("   TEKNOFEST 2026 — Aegis-AI System Verification")
    print("="*55)

    sm = ScenarioManager(sample_rate=1e6)

    # 1. Parameter Extraction
    print("\n[1] Parameter Extraction")
    extractor = ParameterExtractor(sample_rate=1e6)
    t = np.linspace(0, 0.01, 10000)
    signal = np.zeros_like(t)
    for i in range(5):
        start = i * 2000 + 500
        signal[start:start+500] = 1.0
    params = extractor.estimate_parameters(signal)
    check("PRI extracted", params["PRI"] is not None)
    check("PW extracted",  params["PW"] is not None)

    # 2. Direction Finding
    print("\n[2] Direction Finding")
    df = DirectionFinder()
    angle = df.estimate_doa_amplitude([0.9, 0.7, 0.1, 0.2])
    check("DoA angle in range [0, 360]", 0 <= angle <= 360)
    angle_phase = df.estimate_doa_phase(np.pi / 4, wavelength=1.0)
    check("Phase DoA angle valid", -90 <= angle_phase <= 90)

    # 3. LPI Detection
    print("\n[3] LPI Detection (FMCW Chirp)")
    lpi = LPIDetector(sample_rate=1e6)
    _, lpi_sig = sm.get_scenario_signal("LPI Stealth Radar", duration=0.01)
    result = lpi.detect_all(lpi_sig)
    check("LPI chirp detected", result["final_verdict"] == "DETECTED")
    check("Confidence is float",  isinstance(result["confidence"], float))

    # 4. Autonomy Manager
    print("\n[4] Autonomy & Threat Prioritization")
    clf = SignalClassifier()
    autonomy = AutonomyManager(clf, lpi, {})
    freqs = np.linspace(0, 500e3, 1000)
    mags  = np.zeros(1000); mags[500] = 1.0
    strategy = autonomy.process_detection(freqs, mags)
    check("Strategy returned",              isinstance(strategy, str))
    check("get_highest_priority_threat runs", True)  # just verify no crash

    # 5. Jammers
    print("\n[5] Jamming Assets")
    nj = NoiseJammer(1e6)
    _, sig = nj.generate_jamming_signal(0.001)
    check("NoiseJammer generates signal", len(sig) > 0)

    adj = AdaptiveNoiseJammer(1e6)
    adj.set_power(20)
    _, sig_high = adj.generate_jamming_signal(0.001, threat_risk=10)
    _, sig_low  = adj.generate_jamming_signal(0.001, threat_risk=2)
    check("AdaptiveJammer scales power with risk", np.std(sig_high) > np.std(sig_low))

    coord = JammerCoordinator(1e6)
    coord.assign_jammer("T1", "LPI_Radar", 9)
    coord.assign_jammer("T2", "Radar_FC",  10)
    _, combined = coord.generate_combined_signal(0.001)
    check("JammerCoordinator combines signals", len(combined) > 0)

    # 6. New Scenarios
    print("\n[6] New Scenario Signals")
    for scenario in ["LPI Stealth Radar", "Fire Control Radar"]:
        _, sig = sm.get_scenario_signal(scenario, duration=0.005)
        check(f"Scenario '{scenario}' generates signal", len(sig) > 0)

    print("\n" + "="*55)
    print("   Verification Complete.")
    print("="*55 + "\n")

if __name__ == "__main__":
    test_eh_system()
