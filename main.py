import time
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("Mergen-AI")

from src.signal_processing.generator import SignalGenerator
from src.signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor
from src.ai_engine.classifier import SignalClassifier
from src.ai_engine.autonomy_manager import AutonomyManager
from src.signal_processing.lpi_detector import LPIDetector
from src.jamming_logic.jammers import SmartJammer
from src.simulation.scenario_manager import ScenarioManager

def run_autonomous_loop():
    logger.info("Mergen-AI Otonom EH Döngüsü Başlatılıyor [V2.1]...")
    
    sample_rate = 1e6
    duration = 0.01 # 10ms window
    
    # Initialize components
    gen = SignalGenerator(sample_rate)
    sa = SpectrumAnalyzer(sample_rate)
    pe = ParameterExtractor(sample_rate)
    scen = ScenarioManager(sample_rate)
    classifier = SignalClassifier()
    lpi_detector = LPIDetector(sample_rate)
    jammer_map = {"Smart": SmartJammer(sample_rate)}
    autonomy = AutonomyManager(classifier, lpi_detector, jammer_map)
    
    scenarios = [
        "Clear Sky",
        "Long Range Search",
        "Tracking Radar",
        "LPI Stealth Radar"
    ]
    
    try:
        for i, scenario_name in enumerate(scenarios, 1):
            print(f"--- [Senaryo {i}: {scenario_name}] ---")
            
            # 1. EM Spektrumu Tara (Simülasyon)
            if scenario_name == "Clear Sky":
                _, signal = gen.generate_noise(duration, noise_level=0.1)
                print("[ED] İzleme: Spektrum temiz.")
            elif scenario_name == "LPI Stealth Radar":
                # FMCW Chirp (LPI)
                t_lpi = np.linspace(0, duration, int(sample_rate*duration))
                signal = np.cos(2*np.pi*(100e3*t_lpi + 50e6*t_lpi**2))
                _, noise = gen.generate_noise(duration, noise_level=0.2)
                signal = gen.add_signals(signal, noise)
                print("[ED] İzleme: Karmaşık (LPI?) sinyal saptandı.")
            else:
                _, signal = scen.get_scenario_signal(scenario_name, duration)
                _, noise = gen.generate_noise(duration, noise_level=0.1)
                signal = gen.add_signals(signal, noise)
                print(f"[ED] İzleme: Aktif yayın saptandı ({scenario_name})")

            # 2. Teknik Parametre Çıkarımı
            params = pe.estimate_parameters(signal)
            if params["CenterFreq"]:
                print(f"[ED] Analiz: Frekans={params['CenterFreq']/1e3:.1f}kHz, PRI={params['PRI']*1e3:.2f}ms, PW={params['PW']*1e6:.1f}us")

            # 3. Otonom Analiz & Karar
            freqs, mags = sa.compute_fft(signal)
            strategy = autonomy.process_detection(freqs, mags, raw_signal=signal, params=params)
            
            # 4. Müdahale Uygula
            if strategy != "None" and strategy is not None:
                print(f"[ET] Karar: MÜDAHALE GEREKLİ! Strateji: {strategy}")
            else:
                print("[ET] Karar: İZLEME DEVAM EDİYOR.")
                
            print("\n")
            time.sleep(1.5)
            
    except KeyboardInterrupt:
        print("\nDöngü kullanıcı tarafından durduruldu.")

if __name__ == "__main__":
    run_autonomous_loop()
