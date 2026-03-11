import sys
import os
import random
import numpy as np
from flask import Flask, render_template, jsonify, request

# Setup path integration to access src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.simulation.mission_engine import MissionEngine
from src.simulation.scenario_manager import ScenarioManager
from src.jamming_logic.jammers import FrequencyHoppingJammer, JammerCoordinator
from src.signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor, SigMFExporter
from src.signal_processing.tracking import Geolocator, MultiTargetTrackerManager
from src.ai_engine.classifier import SignalClassifier
from src.ai_engine.autonomy_manager import AutonomyManager
from src.signal_processing.lpi_detector import LPIDetector

app = Flask(__name__)
mission_engine  = MissionEngine()
scen_mgr        = ScenarioManager(sample_rate=1e6)
spectrum_ana    = SpectrumAnalyzer(sample_rate=1e6)
param_extractor = ParameterExtractor(sample_rate=1e6)
classifier      = SignalClassifier()
lpi_detector    = LPIDetector(sample_rate=1e6)
jammer_coord    = JammerCoordinator(sample_rate=1e6)
autonomy        = AutonomyManager(classifier, lpi_detector, jammer_coord)
fhss_jammer     = FrequencyHoppingJammer(sample_rate=1e6)
sigmf_exporter  = SigMFExporter(sample_rate=1e6)
geolocator      = Geolocator()
tracker_mgr     = MultiTargetTrackerManager()

# Available scenarios to cycle through
SCENARIOS  = ["Clear Sky", "Long Range Search", "Tracking Radar", "LPI Stealth Radar", "Fire Control Radar", "FHSS Comms"]
# System State & Hardware Simulation
_tick       = [0]
_tuning     = {"center_freq": 150.0, "gain": 45, "sample_rate": 1.0}
_hardware   = {
    "gpu_load": 42, "gpu_temp": 54, "cpu_load": 28,
    "battery_v": 22.8, "sdr_status": "LOCKED",
    "is_recording": False
}
_spectrum_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """
    Live API: processes a real scenario signal and returns structured threat data.
    """
    scenario_name = SCENARIOS[_tick[0] % len(SCENARIOS)]
    _tick[0] += 1

    # Generate real signal
    _, signal = scen_mgr.get_scenario_signal(scenario_name, duration=0.01)
    freqs, mags = spectrum_ana.compute_fft(signal)
    params       = param_extractor.estimate_parameters(signal)

    # FHSS tracking update
    detected, hop_freq = fhss_jammer.detect_and_learn_hop(freqs, mags[:len(freqs)])
    next_hop = fhss_jammer.predict_next_hop()

    # Run full ADSS pipeline
    strategy = autonomy.process_detection(freqs, mags[:len(freqs)], raw_signal=signal, params=params)
    risk_info = autonomy.risk_assessment()

    # Collect mission environment observations
    observations = mission_engine.update_environment()
    detected_threats = []
    sensor_positions = [(39.9250, 32.8660), (39.9260, 32.8670)] # Simulated sensor positions
    
    # Update all trackers (prediction step)
    tracker_mgr.predict_all()
    active_ids = [obs["id"] for obs in observations]

    for obs in observations:
        # Update Multi-Target Tracker
        tracker_mgr.update_emitter(obs["id"], obs["bearing"])
        state = tracker_mgr.trackers[obs["id"]].get_state()

        # Triangulate Geolocation (Simulated use)
        # Using two bearings (real bearing + a slightly shifted one) for triangulation demo
        est_pos = geolocator.triangulate(sensor_positions, [obs["bearing"], obs["bearing"] + 5.0])

        detected_threats.append({
            "id": obs["id"],
            "type": obs["type"],
            "confidence": round(0.82 + random.random() * 0.15, 2),
            "direction": round(state["bearing"], 1),
            "frequency": f"{obs['freq'] / 1e6:.1f} MHz",
            "signal_strength": round(obs["signal_strength"], 3),
            "geoloc": est_pos
        })
    
    # Cleanup lost tracks
    tracker_mgr.remove_dead_tracks(active_ids)

    # LPI Detection Analysis
    lpi_results = lpi_detector.detect_all(signal)

    return jsonify({
        "system_status": "Operational",
        "scenario": scenario_name,
        "active_jammer": strategy,
        "risk_level": risk_info["threat_level"],
        "risk_score": risk_info["risk_score"],
        "detected_threats": detected_threats,
        "lpi_status": lpi_results["final_verdict"],
        "spectrum_data": mags[:100].tolist() if len(mags) >= 100 else mags.tolist(),
        "params": {k: round(v * 1000, 3) if isinstance(v, float) else v
                   for k, v in params.items()},
        "fhss": {
            "hop_detected": detected,
            "last_hop_freq_khz": round(hop_freq / 1e3, 1) if detected else None,
            "predicted_next_hop_khz": round(next_hop / 1e3, 1) if next_hop else None
        },
        "geolocs": [t["geoloc"] for t in detected_threats],
        "hardware": {
            "gpu_load": f"{_hardware['gpu_load'] + random.randint(-2, 2)}%",
            "gpu_temp": f"{_hardware['gpu_temp'] + random.random():.1f}°C",
            "battery": f"{_hardware['battery_v'] - (_tick[0]*0.001):.1f}V",
            "sdr": _hardware['sdr_status'],
            "recording": _hardware['is_recording']
        },
        "tuning": _tuning,
        "iq_samples": ([{"re": float(c.real), "im": float(c.imag)} for c in (np.cos(np.linspace(0, 10, 64)) + 1j*np.sin(np.linspace(0, 10, 64)) + np.random.normal(0, 0.1, 64))] 
                       if _tick[0] % 2 == 0 else 
                       [{"re": float(c.real), "im": float(c.imag)} for c in (np.random.normal(0, 0.5, 64) + 1j*np.random.normal(0, 0.5, 64))]),
        "ai_confidence": [
            {"label": "BPSK", "value": 0.82 if _tick[0] % 3 == 0 else 0.1},
            {"label": "QPSK", "value": 0.15 if _tick[0] % 3 == 0 else 0.75},
            {"label": "FHSS", "value": 0.03}
        ]
    })

@app.route('/api/threats')
def get_threats():
    """Returns the last 10 threat detections from the ADSS log."""
    log = autonomy.threat_log[-10:]
    return jsonify({"threats": log, "total": len(autonomy.threat_log)})

@app.route('/api/risk')
def get_risk():
    """Returns the current threat environment risk assessment."""
    return jsonify(autonomy.risk_assessment())

@app.route('/api/mission')
def get_mission():
    """Returns mission engine summary: active emitters, elapsed time, complexity."""
    return jsonify(mission_engine.get_mission_summary())

@app.route('/api/spectrum_history')
def get_spectrum_history():
    """Returns last 20 spectrum snapshots for trend analysis."""
    return jsonify({"history": _spectrum_history, "count": len(_spectrum_history)})

@app.route('/api/action/<action_type>', methods=['POST'])
def trigger_ea_action(action_type):
    """
    Handles Manual Electronic Attack triggers from the dashboard.
    Supported types: 'jam' (barrage, spot, interleaved), 'spoof' (analog, gnss, rgpo)
    """
    data = request.get_json(force=True, silent=True) or {}
    method = data.get("method", "unknown")
    threat_id = data.get("threat_id", "T1")

    if action_type == 'jam':
        # Map UI method to jammer type
        jt_map = {"barrage": "noise", "spot": "noise", "interleaved": "adaptive"}
        j_key = jt_map.get(method.lower(), "noise")
        
        jammer_coord.assign_jammer(threat_id, j_key, risk_score=8)
        print(f"[UI COMMAND] Triggering JAMMING. Method: {method.upper()} -> {j_key} on Target {threat_id}")
        return jsonify({"status": "success", "action": "jam", "method": method})
    
    elif action_type == 'spoof':
        # Map UI method to spoofing type
        st_map = {"analog": "analog", "gnss": "gnss", "rgpo": "spoofing"}
        s_key = st_map.get(method.lower(), "noise")
        
        jammer_coord.assign_jammer(threat_id, s_key, risk_score=10)
        print(f"[UI COMMAND] Triggering SPOOFING. Method: {method.upper()} -> {s_key} on Target {threat_id}")
        return jsonify({"status": "success", "action": "spoof", "method": method})
    
    elif action_type == 'record':
        _hardware["is_recording"] = True
        # Simulate capturing and exporting current signal to SigMF
        _, signal = scen_mgr.get_scenario_signal(SCENARIOS[_tick[0] % len(SCENARIOS)], duration=0.05)
        meta_path, data_path = sigmf_exporter.export(signal, filename_prefix="UI_Manual_Capture")
        print(f"[UI COMMAND] Recording saved to: {meta_path}")
        # Automatically set recording flag back after a while (simulated)
        return jsonify({"status": "success", "meta": meta_path, "data": data_path})
    
    elif action_type == 'tune':
        _tuning["center_freq"] = data.get("freq", _tuning["center_freq"])
        _tuning["gain"] = data.get("gain", _tuning["gain"])
        return jsonify({"status": "success", "tuning": _tuning})
    
    return jsonify({"status": "error", "message": "Unknown action type"}), 400

if __name__ == '__main__':
    # When running locally, accessible at http://127.0.0.1:5000
    app.run(debug=True, port=5000, host='0.0.0.0')

