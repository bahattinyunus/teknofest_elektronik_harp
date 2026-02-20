import time
import numpy as np
from src.signal_processing.generator import SignalGenerator
from src.signal_processing.analyzer import SpectrumAnalyzer
from src.ai_engine.classifier import SignalClassifier
from src.jamming_logic.jammers import SmartJammer

def run_autonomous_loop():
    print("Aegis-AI Otonom EH Döngüsü Başlatılıyor...\n")
    
    sample_rate = 1e6
    duration = 0.005 # 5ms window
    
    # Initialize components
    gen = SignalGenerator(sample_rate)
    sa = SpectrumAnalyzer(sample_rate)
    classifier = SignalClassifier()
    jammer = SmartJammer(sample_rate)
    
    try:
        # Loop for 5 iterations to demo
        for i in range(1, 6):
            print(f"--- [Döngü {i}] ---")
            
            # 1. EM Spektrumu Tara (Listen)
            # Simüle edilmiş hedef: Döngü 3'te bir tehdit belirsin
            is_threat_active = (i >= 3)
            target_freq = 150e3 if is_threat_active else 0
            
            t, signal = gen.generate_noise(duration, noise_level=0.1)
            if is_threat_active:
                _, target = gen.generate_cw(target_freq, duration, amplitude=0.8)
                signal = gen.add_signals(signal, target)
                print(f"[ED] Spektrum Taraması: Sinyal saptandı ({target_freq/1e3} kHz)")
            else:
                print("[ED] Spektrum Taraması: Temiz.")

            # 2. Analiz ve Sınıflandırma (AI Engine)
            freqs, mags = sa.compute_fft(signal)
            features = classifier.extract_features(freqs, mags)
            classification = classifier.predict(features)
            
            print(f"[AI] Analiz Sonucu: {classification}")
            
            # 3. Karar ve Müdahale (ET Logic)
            if classification != "Noise":
                print(f"[ET] Karar: MÜDAHALE GEREKLİ! {classification} tipi bir tehdit saptandı.")
                _, jamming_signal = jammer.generate_jamming_signal(duration, target_detected=True)
                print(f"[*] SMART JAMMER DEVREDE: Spektrum baskılanıyor.")
            else:
                print("[ET] Karar: İZLEME DEVAM EDİYOR. Aktif bir tehdit yok.")
                
            print("\n")
            time.sleep(1) # Visual delay for demo
            
    except KeyboardInterrupt:
        print("\nDöngü kullanıcı tarafından durduruldu.")

if __name__ == "__main__":
    run_autonomous_loop()
