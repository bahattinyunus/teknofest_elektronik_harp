# 🧠 Mergen-AI: Stratejik Yapay Zeka Geliştirme Planı

Bu doküman, TEKNOFEST 2026 Elektronik Harp Yarışması'nda **"En İyi Yapay Zekâ Uygulaması"** ödülünü hedefleyen, Mergen-AI sisteminin bilişsel yeteneklerini ve otonom karar destek mekanizmalarını detaylandırır.

---

## 1. Vizyon: Bilişsel Elektronik Harp (Cognitive EW)
Geleneksel EH sistemleri önceden tanımlanmış kütüphanelere (Threat Library) bağlıdır. Mergen-AI, yapay zeka ile **tanımlanmamış veya yeni (zero-day)** sinyal karakteristiklerini öğrenen ve otonom olarak karşı tedbir (Countermeasure) üreten bir mimariye evrilmektedir.

---

## 2. Teknik Yol Haritası ve Fazlar

### 📡 Faz 1: Dinamik Veri Üretimi ve Kanal Modelleme
AI modellerinin sahada başarılı olması için sentetik değil, gerçekçi verilerle eğitilmesi şarttır.
- **Model:** GNU Radio tabanlı I/Q veri jeneratörü.
- **Kanal Etkileri:** Rayleigh/Rician Fading, Doppler Shift ve AWGN (Additive White Gaussian Noise) entegrasyonu.
- **Veri Artırma:** SDR donanımlarının saat kaymalarını (Clock drift) simüle eden "Phase Noise Injection" teknikleri.

### 🔬 Faz 2: Multimodal AMC (Automatic Modulation Classification)
Sinyal modülasyon tipini tespit etmek için hibrit bir sinir ağı mimarisi kullanılacaktır.
- **I/Q Kolu (Zaman Domaini):** Ham I/Q örnekleri üzerinden faz değişimlerini yakalayan **1D-ResNet** bloğu.
- **Spektrum Kolu (Frekans Domaini):** Spektrogram (STFT) görüntülerini işleyen **2D-EfficientNet-v2** bloğu.
- **Fusion Layer:** İki koldan gelen özellik vektörlerinin birleştirilerek nihai sınıflandırmanın (BPSK, 16QAM, FHSS vb.) yapılması.

### 🛡️ Faz 3: Otonom Karar Destek Sistemi (ADSS)
ED verilerini ET aksiyonuna dönüştüren akıllı mantık katmanı.
- **Bayesian Risk Analysis:** Karıştırma (Jamming) yapılmasının risk/kazanç oranını hesaplar (Örn: "Düşman radarı beni fark etti mi?").
- **Dinamik Kaynak Yönetimi:** Sınırlı ET gücünü (140W), en yüksek tehdit önceliğine sahip frekanslara otonom olarak bölüştürür.

---

## 💻 Donanım ve Edge AI Optimizasyonu

Yapay zeka modellerinin sahada (Edge) gecikmesiz çalışması için şu teknikler uygulanacaktır:

1.  **Model Quantization:** FP32 modellerin INT8/FP16 hassasiyetine indirilmesi.
2.  **NVIDIA TensorRT Entegrasyonu:** NVIDIA Jetson üzerinde GPU hızlandırmalı çıkarım (Inference).
3.  **On-Device Training:** Sahadan toplanan yeni sinyal örneklerinin, sistem boşta iken yerel olarak eğitilip modelin güncellenmesi (Incremental Learning).

---

## 🏆 Şartnameye Uyumluluk ve Puanlama Hedefi

| Şartname Kriteri | AI Çözümümüz | Etki / Puan |
| :--- | :--- | :--- |
| **Parametre Çıkarımı** | Derin öğrenme ile %98+ doğruluk oranı. | Yüksek (ED Puanı) |
| **Otonomluk** | Operatör müdahalesi olmadan tehdit önceliklendirme. | Kritik (Otonomi Puanı) |
| **Yenilikçi Yaklaşım** | Multimodal IQ-Spectrum Fusion mimarisi. | "En İyi AI" Ödülü Adaylığı |

---

## 📅 Uygulama Takvimi

- **Q2 2026:** Veri seti hazırlığı ve model temelinin atılması.
- **Q3 2026:** Saha verileriyle ince ayar (Fine-tuning) ve donanım testleri.
- **Final:** Sahada tam otonom ED/ET döngüsünün sergilenmesi.

---
*Bu plan, Mergen-AI projesinin teknik üstünlüğünü ve yarışma hedeflerine olan bağlılığını temsil eder.*
