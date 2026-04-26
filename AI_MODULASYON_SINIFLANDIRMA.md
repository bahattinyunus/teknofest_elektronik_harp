# 🧠 Mergen-AI: Yapay Zeka Destekli Modülasyon Sınıflandırma (AMC) Raporu

Bu rapor, Mergen-AI projesinde yer alan Elektronik Destek (ED) alt sisteminin en kritik bileşenlerinden biri olan **Otomatik Modülasyon Sınıflandırma (AMC)** mekanizmasını, kullanılan derin öğrenme mimarilerini ve gelecekteki geliştirme planlarını detaylandırmaktadır.

## 1. Mevcut Mimari: Hibrit Yaklaşım

Mergen-AI, yalnızca derin öğrenmeye güvenmek yerine, **Kural Tabanlı Sezgisel (Heuristic)** ve **Derin Öğrenme (CNN)** modellerini birleştiren hibrit bir yapı kullanır.

### A. Kural Tabanlı Motor (`classifier.py`)
Sinyal parametreleri (PRI, PW, Bant Genişliği, Spectral Flatness) üzerinden çalışan hızlı bir karar verme mekanizmasıdır. 
*   **Hız:** Mikro saniye mertebesinde sonuç üretir.
*   **Kararlılık:** SNR (Sinyal-Gürültü Oranı) yüksek olduğunda %100 doğruluk sağlar.

### B. Derin Öğrenme Modeli (`dl_classifier.py`)
Şu anki altyapıda **1D CNN (Evrişimli Sinir Ağı)** mimarisi hazır bulunmaktadır.
*   **Girdi:** Spektral büyüklük dizisi (Magnitude Spectrum).
*   **Mimari:** 3 katmanlı Conv1d + Adaptive Average Pooling + 2 katmanlı Tam Bağlantılı (Linear) katman.
*   **Avantajı:** Sinyaldeki karmaşık dokuları (texture) ve modülasyon karakteristiklerini hiyerarşik olarak öğrenir.

## 2. "God-Tier" Geliştirme Önerileri ve Yol Haritası

Şartnamenin ötesine geçmek ve sahada üstünlük sağlamak için aşağıdaki tekniklerin entegrasyonu planlanmaktadır:

### 🔬 Multimodal IQ-Spectrum Fusion
Sadece frekans spektrumuna bakmak yerine, zaman domainindeki ham **I/Q (In-phase/Quadrature)** verilerini de işleyen iki kollu (two-stream) bir ağ:
1.  **Koli 1:** I/Q verileri üzerinden ham faz değişimlerini öğrenen 1D-ResNet.
2.  **Kol 2:** Spektrogram (STFT) görüntülerini işleyen 2D-CNN.
3.  **Birleştirme:** İki koldan gelen özellik vektörlerinin (feature vectors) "concatenation" yöntemiyle birleştirilip son karara varılması.

### 🌊 Zaman-Frekans Analizi: WVD ve Wavelets
LPI (Low Probability of Intercept) radarların kullandığı **LFM (Chirp)** sinyalleri, standart FFT ile her zaman net ayrıştırılamaz. 
*   **Wigner-Ville Distribution (WVD):** Zaman ve frekans çözünürlüğünü maksimize ederek sinyal imzasını bir "resim" gibi AI'ya sunar.
*   **Yapay Zeka Etkisi:** CNN modelleri, WVD çıktısı üzerindeki eğimleri (slope) öğrenerek chirp oranını (chirp rate) hatasız tespit edebilir.

### 🛡️ Kanal Etkileri ve Veri Artırma (Data Augmentation)
Modelin sahada (noise, multipath, doppler) çökmemesi için eğitim setinde şu teknikler uygulanacaktır:
*   **Rayleigh Fading:** Şehir içi yansımalı ortam simülasyonu.
*   **AWGN Entegrasyonu:** Farklı SNR seviyelerinde (-20dB ile +30dB arası) dinamik eğitim.
*   **Phase Offset / Frequency Drift:** SDR donanımlarının saat hatalarının simüle edilmesi.

## 3. Donanım Optimizasyonu (Edge AI)

TEKNOFEST sahasında sistemin **Raspberry Pi 5** veya **NVIDIA Jetson** üzerinde gecikmesiz çalışması için:
*   **RPi Interfacing:** USRP/HackRF verilerinin USB 3.0 üzerinden yüksek hızda çekilmesi ve C++ DSP bloklarıyla işlenmesi.
*   **TensorRT (Jetson):** Modelin FP16 veya INT8 hassasiyetine indirilerek (quantization) GPU çekirdeklerinde hızlandırılması.

## 4. Taktik Arayüz (UI/UX) Vizyonu

Yapay zeka sonuçlarının operatöre en efektif şekilde sunulması için planlanan arayüz geliştirmeleri:

*   **IQ Takımyıldız (Constellation) Diyagramı:** Sinyalin I/Q uzayındaki dağılımını göstererek modülasyon tipinin (BPSK/QPSK/16QAM vb.) görsel olarak teyit edilmesini sağlar.
*   **AI Güven Isı Haritası (Confidence Heatmap):** Sadece tek bir etiket yerine, AI'nın olasılık dağılımını (Softmax çıktıları) bar grafik olarak göstererek operatöre belirsizlik durumlarında karar yetkisi verir.
*   **Spektral Overlay:** Spektrum grafiği üzerinde tespit edilen her bir sinyal tepesinin (peak) üzerine AI tarafından atanan etiketlerin anlık "tooltip" olarak bindirilmesi.

## 5. Akademik Referanslar ve Kaynakça

AMC geliştirme sürecinde aşağıdaki temel kaynaklar baz alınmıştır:
1.  **O'Shea, T. J., & West, N. (2016).** "Radio Machine Learning Dataset Generation with GNU Radio".
2.  **DeepSig RadioML Veriseti:** Dünya standardı olan modülasyon veri seti.
3.  **ResNet-Based AMC:** Daha derin ağların faz karmaşıklığını çözmedeki başarısı.

---
*Hazırlayan: Mergen-AI Savunma Teknolojileri Ekibi*
