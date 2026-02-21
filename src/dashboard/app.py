from flask import Flask, render_template, jsonify
import random
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """
    Mock API for real-time data updates.
    """
    return jsonify({
        "system_status": "Operational",
        "active_jammer": random.choice(["Noise", "Spoofing", "Smart", "None"]),
        "detected_threats": [
            {"type": "Radar_L", "confidence": 0.89, "direction": 45},
            {"type": "Comm_Link", "confidence": 0.95, "direction": 120}
        ],
        "spectrum_data": (np.random.rand(100) * 0.5).tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
