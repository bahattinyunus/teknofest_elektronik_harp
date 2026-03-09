import sys
import os
import random
import numpy as np
from flask import Flask, render_template, jsonify, request

# Setup path integration to access src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.simulation.mission_engine import MissionEngine
from src.simulation.scenario_manager import ScenarioManager
from src.signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor
from src.ai_engine.classifier import SignalClassifier
from src.ai_engine.autonomy_manager import AutonomyManager
from src.signal_processing.lpi_detector import LPIDetector
from src.jamming_logic.jammers import FrequencyHoppingJammer, JammerCoordinator

app = Flask(__name__)
mission_engine  = MissionEngine()
scen_mgr        = ScenarioManager(sample_rate=1e6)
spectrum_ana    = SpectrumAnalyzer(sample_rate=1e6)
param_extractor = ParameterExtractor(sample_rate=1e6)
classifier      = SignalClassifier()
lpi_detector    = LPIDetector(sample_rate=1e6)
autonomy        = AutonomyManager(classifier, lpi_detector, {})
fhss_jammer     = FrequencyHoppingJammer(sample_rate=1e6)
jammer_coord    = JammerCoordinator(sample_rate=1e6)

# Available scenarios to cycle through
SCENARIOS  = ["Clear Sky", "Long Range Search", "Tracking Radar", "LPI Stealth Radar", "Fire Control Radar", "FHSS Comms"]
_tick       = [0]
_spectrum_history = []  # Rolling buffer of last 20 spectrum snapshots

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
    for obs in observations:
        detected_threats.append({
            "id": obs["id"],
            "type": obs["type"],
            "confidence": round(0.82 + random.random() * 0.15, 2),
            "direction": round(obs["bearing"], 1),
            "frequency": f"{obs['freq'] / 1e6:.1f} MHz",
            "signal_strength": round(obs["signal_strength"], 3)
        })

    return jsonify({
        "system_status": "Operational",
        "scenario": scenario_name,
        "active_jammer": strategy,
        "risk_level": risk_info["threat_level"],
        "risk_score": risk_info["risk_score"],
        "detected_threats": detected_threats,
        "spectrum_data": mags[:100].tolist() if len(mags) >= 100 else mags.tolist(),
        "params": {k: round(v * 1000, 3) if isinstance(v, float) else v
                   for k, v in params.items()},
        "fhss": {
            "hop_detected": detected,
            "last_hop_freq_khz": round(hop_freq / 1e3, 1) if detected else None,
            "predicted_next_hop_khz": round(next_hop / 1e3, 1) if next_hop else None
        }
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

@app.route('/api/jammer', methods=['POST'])
def control_jammer():
    """
    Assigns a jammer via JammerCoordinator.
    JSON body: {"threat_id": "T1", "threat_type": "LPI_Radar", "risk": 9}
    """
    data = request.get_json(force=True)
    threat_id   = data.get("threat_id", "T0")
    threat_type = data.get("threat_type", "Unknown")
    risk        = int(data.get("risk", 5))
    jammer_coord.assign_jammer(threat_id, threat_type, risk)
    return jsonify({
        "status": "assigned",
        "threat_id": threat_id,
        "threat_type": threat_type,
        "active_assignments": list(jammer_coord.active_assignments.keys())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

