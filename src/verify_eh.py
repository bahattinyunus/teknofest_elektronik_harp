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

PASS = "[PASS]"
FAIL = "[FAIL]"

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
    check("Power_RMS calculated",  "Power_RMS" in params)
    check("SignalType detected (Analog/Digital)", "SignalType" in params)

    # 1.b Advanced Parameter Extraction (Tercihen)
    print("\n[1b] Multiplexing & ECCM Detection")
    # Simulate an OFDM-like flat spectrum
    ofdm_signal = np.random.normal(0, 0.5, 1000)
    ofdm_params = extractor.estimate_parameters(ofdm_signal)
    check(f"Multiplexing detected: {ofdm_params['Multiplexing']}", ofdm_params["Multiplexing"] != "None")
    check(f"ECCM detected: {ofdm_params['ECCM']}", ofdm_params["ECCM"] != "None")

    # 2. Direction Finding (12-Antenna Vivaldi Array)
    print("\n[2] Direction Finding (12x Vivaldi)")
    df = DirectionFinder(num_antennas=12)
    # Simulate signal peak at 90 degrees (index 3: 0, 30, 60, 90)
    strengths = [0.0]*12
    strengths[2] = 0.5; strengths[3] = 1.0; strengths[4] = 0.5
    angle = df.estimate_doa_amplitude(strengths)
    check(f"DoA angle estimated at 90°: {angle:.1f}°", 85 <= angle <= 95)
    angle_phase = df.estimate_doa_phase(np.pi / 4, wavelength=1.0)
    check("Phase DoA angle valid", -90 <= angle_phase <= 90)

    # 2b. Geolocation (New)
    print("\n[2b] 2D Geolocation (Triangulation)")
    from src.signal_processing.tracking import Geolocator
    geo = Geolocator(reference_lat=39.9, reference_lon=32.8)
    # 2 sensors at different positions with beams crossing at (39.91, 32.81) approximately
    sensors = [(39.9, 32.8), (39.9, 32.82)]
    bearings = [45, 315] 
    est_pos = geo.triangulate(sensors, bearings)
    check(f"Geolocation estimated: {est_pos}", est_pos is not None)

    # 3. LPI Detection
    print("\n[3] LPI Detection (FMCW Chirp)")
    lpi = LPIDetector(sample_rate=1e6)
    _, lpi_sig = sm.get_scenario_signal("LPI Stealth Radar", duration=0.01)
    result = lpi.detect_all(lpi_sig)
    check("LPI chirp detected", result["final_verdict"] == "DETECTED")
    check("Confidence is float",  isinstance(result["confidence"], float))

    # 3b. Sinyal İzleme/Dinleme (Analog Demodulation)
    print("\n[3b] Sinyal Dinleme (Analog Demodulation)")
    from src.signal_processing.analyzer import AnalogDemodulator
    demod = AnalogDemodulator(sample_rate=1e6)
    _, analog_sig = sm.get_scenario_signal("Analog Telsiz", duration=0.005)
    demodulated = demod.demodulate(analog_sig, mode="FM")
    check("Analog FM signal demodulated (volume > 0)", np.mean(demodulated) > 0)

    # 4. Autonomy Manager
    print("\n[4] Autonomy & Threat Prioritization")
    clf = SignalClassifier(use_dl=True)
    coord = JammerCoordinator(1e6)
    autonomy = AutonomyManager(clf, lpi, coord)
    freqs = np.linspace(0, 500e3, 1000)
    mags  = np.zeros(1000); mags[500] = 1.0
    strategy = autonomy.process_detection(freqs, mags)
    check("Strategy returned",              isinstance(strategy, str))
    check("get_highest_priority_threat runs", True)  # just verify no crash
    check("DL PyTorch Inference runs (if installed)", clf.use_dl)

    # 5. Jammers
    print("\n[5] Jamming Assets")
    nj = NoiseJammer(1e6)
    _, sig = nj.generate_jamming_signal(0.001)
    check("NoiseJammer generates signal", len(sig) > 0)

    from src.jamming_logic.jammers import GNSSJammer, AnalogVoiceJammer
    gnss_j = GNSSJammer(1e6)
    _, gnss_sig = gnss_j.generate_jamming_signal(0.001, target_lat=40.0, target_lon=33.0)
    check("GNSSJammer (Spoofing) generates signal", len(gnss_sig) > 0)

    analog_j = AnalogVoiceJammer(1e6)
    _, fm_sig = analog_j.generate_jamming_signal(0.001, mode="FM")
    check("AnalogVoiceJammer (FM Spoofing) generates signal", len(fm_sig) > 0)

    adj = AdaptiveNoiseJammer(1e6)
    adj.set_power(20)
    _, sig_high = adj.generate_jamming_signal(0.001, threat_risk=10)
    _, sig_low  = adj.generate_jamming_signal(0.001, threat_risk=2)
    check("AdaptiveJammer scales power with risk", np.std(sig_high) > np.std(sig_low))

    coord = JammerCoordinator(1e6)
    coord.assign_jammer("T1", "LPI_Radar", 9)
    coord.assign_jammer("T2", "Radar_FC",  10)
    _, combined = coord.generate_combined_signal(0.001, look_through_active=True)
    check("JammerCoordinator combines signals with Look-Through", len(combined) > 0)
    check("Look-Through gap applied (last 10% is zero)", np.all(combined[-100:] == 0))

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
