import unittest
import numpy as np
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor
from src.ai_engine.swarm_engine import SwarmCorrelationEngine
from src.signal_processing.tracking import Geolocator

class TestAegisOmega(unittest.TestCase):
    def setUp(self):
        self.sample_rate = 1e6
        self.sa = SpectrumAnalyzer(self.sample_rate)
        self.pe = ParameterExtractor(self.sample_rate)
        self.swarm = SwarmCorrelationEngine()
        self.geo = Geolocator()

    def test_spectral_analysis(self):
        # Generate 100kHz sine wave
        t = np.linspace(0, 0.01, int(self.sample_rate * 0.01))
        signal = np.cos(2 * np.pi * 100e3 * t)
        freqs, mags = self.sa.compute_fft(signal)
        peak_freq = freqs[np.argmax(mags)]
        self.assertAlmostEqual(peak_freq, 100e3, delta=1e3)

    def test_swarm_correlation(self):
        active_emitters = {
            "e1": {"aoa": 40.0, "last_seen": 1000.0, "label": "Radar"},
            "e2": {"aoa": 42.0, "last_seen": 1000.0, "label": "Radar"},
            "e3": {"aoa": 41.0, "last_seen": 1000.0, "label": "Radar"}
        }
        # Mock time to ensure emitters are "recent"
        import time
        for e in active_emitters.values():
            e['last_seen'] = time.time()
            
        clusters = self.swarm.analyze_emitters(active_emitters)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]['member_count'], 3)
        self.assertIn(clusters[0]['avg_aoa'], range(40, 43))

    def test_weighted_geolocation(self):
        sensors = [(39.9, 32.8), (39.9, 32.82)]
        bearings = [45, 315]
        # Intersection should be around 39.91, 32.81 
        pos = self.geo.triangulate(sensors, bearings)
        self.assertIsNotNone(pos)
        self.assertAlmostEqual(pos[0], 39.91, delta=0.01)
        self.assertAlmostEqual(pos[1], 32.81, delta=0.01)

if __name__ == '__main__':
    unittest.main()
