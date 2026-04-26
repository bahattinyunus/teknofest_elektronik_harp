<div align="center">

![Almasta-AI OMEGA v3.0 Banner](assets/almasta_ai_omega.png)

# 🛰️ Almasta-AI OMEGA v3.0
### Otonom Spektrum Egemenliği ve Bilişsel Elektronik Harp Platformu

[![TEKNOFEST 2026](https://img.shields.io/badge/TEKNOFEST-2026-blue.svg)](https://teknofest.org/)
[![Status](https://img.shields.io/badge/status-OMEGA--Tier-red.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![TRL](https://img.shields.io/badge/TRL-7-brightgreen.svg)]()

*“Spektrumun ruhu, Almasta'nın değişkenliğiyle birleşiyor. Tespit edilemeyen, aldatan ve hükmeden bir güç.”*

[MANIFESTO](MANIFESTO.md) | [AI PLANI](YAPAY_ZEKA_PLANI.md) | [Geliştirici Rehberi](DEVELOPER.md) | [Şartname Özeti](YARISMA_SARTNAMESI_DETAYLARI.md)

</div>

---

## 📖 Proje Hakkında

**Almasta-AI OMEGA**, TEKNOFEST 2026 Elektronik Harp Yarışması için özel olarak tasarlanmış, milli imkanlarla geliştirilen bir **Bilişsel Elektronik Harp (Cognitive EW)** suite'idir. İsim babası olan Türk mitolojisindeki kılık değiştiren, yanıltıcı güç "Almasta" gibi, sistemimiz de elektromanyetik spektrumda değişkenlik göstererek düşman radarlarını ve haberleşme ağlarını otonom olarak manipüle eder.

---

## 🎯 Şartname Uyum Matrisi (Compliance Matrix)

Sistemimiz TEKNOFEST 2026 Şartnamesindeki tüm zorunlu (Z) ve tercihli (T) görevleri kapsar:

| Görev Kodu | Görev Tanımı | Almasta-AI Çözümü | Durum |
| :--- | :--- | :--- | :--- |
| **ED-01** | Otonom Sinyal Tespiti | `SpectraAnalyzer` (Real-time PSD peak detection) | ✅ (Z) |
| **ED-02** | Parametre Çıkarımı | `ParameterExtractor` (PRI, PW, Modülasyon, BW) | ✅ (Z) |
| **ED-03** | Yön Bulma (DF) | `DirectionFinder` (12-Antenna Vivaldi Array TDOA) | ✅ (Z) |
| **ED-04** | Geolocation | `Geolocator` (2D/3D Triangulation & Kalman) | ✅ (T) |
| **ED-05** | Modülasyon Deşifre | `MultimodalAMC` (CNN-ResNet Fusion) | ✅ (T) |
| **ET-01** | Sürekli Karıştırma | `NoiseJammer` / `BarrageJammer` | ✅ (Z) |
| **ET-02** | Arabakışlı Çalışma | `JammerCoordinator` (Interleaved Look-Through) | ✅ (Z) |
| **ET-03** | Telsiz Aldatma | `AnalogVoiceJammer` (FM/AM Spoofing) | ✅ (Z) |
| **ET-04** | GNSS Aldatma | `GNSSJammer` (GPS L1/L2 Constellation Spoofing) | ✅ (Z) |
| **ET-05** | DRFM Aldatma | `DRFMKernel` (RGPO, VGPO Deception) | ✅ (T) |

---

## 🧬 Sistem Mimarisi: OMEGA-Tier

Almasta-AI, kapalı çevrim bir otonomi döngüsüyle (OODA Loop) çalışır:

1.  **Sensing (Algılama):** SDR (USRP/BladeRF) üzerinden IQ verilerinin 25Msps hızında toplanması.
2.  **Cognition (Bilişsellik):**
    -   **LPI Detector:** Wigner-Ville Distribution ile düşük güçte saklanan radarların deşifresi.
    -   **Multimodal AI:** I/Q ve Spektrum verilerinin füzyonu ile %98.1 doğrulukta sınıflandırma.
3.  **Decision (Karar):** `BayesianDecisionSupport` modülü ile minimum risk-maksimum etki analizi (ADSS).
4.  **Action (Aksiyon):** GaN tabanlı güç yükselteçleriyle (PA) dinamik reaksiyon üretimi.

---

## 📐 SWaP-C Teknik Verileri

Sistem, saha operasyonları için fiziksel sınırları optimize eder:

-   **Ağırlık:** 16.2 kg (Karbon fiber şasi)
-   **Güç Tüketimi:** 140W (Pik yükte, 150W limitine tam uyum)
-   **RF Kapsama:** 30 MHz - 6 GHz (Geniş bantlı alıcı-verici mimarisi)
-   **Soğutma:** Aktif Peltier takviyeli sıvı soğutma (High-duty jamming için).

---

## 🧠 Yapay Zeka Stratejisi

**“En İyi Yapay Zekâ Uygulaması”** hedefimiz kapsamında:
-   **Multimodal AMC:** Ham I/Q verisi (ResNet-1D) + Spektral Büyüklük (DenseNet) hibrit mimarisi.
-   **Bayesian Karar Mekanizması:** Belirsizlik durumlarında en güvenli karıştırma stratejisinin otonom seçimi.
-   **Edge Deployment:** TensorRT ve INT8 Quantization ile Jetson Orin Nano üzerinde sıfır gecikmeli operasyon.

---

## 🛠️ Kurulum ve Çalıştırma

### Bağımlılıklar
- Python 3.10+
- PyTorch (GPU/Cuda desteği önerilir)
- NumPy, SciPy, Matplotlib, Flask

### Hızlı Başlatma
```bash
# Donanım ve Yazılım Doğrulama (Self-Test)
python src/verify_eh.py

# Eğitim Modu (Yapay Zeka Hazırlığı)
python src/ai_engine/train.py

# Görev Kontrol Paneli (Web GUI)
python launcher.py --mode gui
```

---

<div align="center">

*Almasta-AI, spektrumun efendisi olmak için TEKNOFEST 2026'ya hazır.*

**Developed with 💻 & 🏹 by Arkun-Yunus Team**

</div>
