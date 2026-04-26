# 🛠️ Almasta-AI Donanım Stratejisi ve Sistem Mimarisi

TEKNOFEST 2026 Elektronik Harp yarışması için belirlenen "Otonomi", "Hızlı Tarama" ve "Etkili Karıştırma" hedefleri doğrultusunda optimize edilmiş donanım mimarisidir.

## 1. Ana Kontrol ve İşleme Birimi (C&C)
Sistem, gerçek zamanlı sinyal işleme ve yapay zeka çıkarımı için yüksek performanslı ve düşük güç tüketimli bir birime ihtiyaç duyar.

*   **Birincil Kontrol Birimi:** **Raspberry Pi 5 (8GB)**
    *   **Neden:** Yeni nesil Broadcom BCM2712 işlemcisi ve geliştirilmiş I/O hızı ile mobil EH görevleri için ideal SwaP dengesi sunar.
    *   **Üst Segment Alternatif:** **NVIDIA Jetson Orin Nano / NX**
    *   **Neden:** CUDA çekirdekleri sayesinde karmaşık CNN (Sinyal Sınıflandırma) ve gerçek zamanlı spektrum analizini (TensorRT) daha düşük gecikmeyle yapabilir.

## 2. Yazılım Tanımlı Radyo (SDR) Birimi
Yarışma hem ED (Dinleme) hem de ET (Müdahale) gerektirdiği için Full-Duplex bir SDR kritiktir.

*   **Birincil Seçenek:** **Ettus USRP B210**
    *   **Kabiliyet:** 70 MHz - 6 GHz frekans aralığı, 56 MHz anlık bant genişliği.
    *   **Avantaj:** 2x2 MIMO (İki kanal alma, iki kanal verme). Yön Bulma (DF) için iki anten girişi aynı anda kullanılabilir.
*   **Bütçe Dostu:** **ADALM-Pluto (PlutoSDR)**
    *   **Kabiliyet:** Genişletilmiş frekans (325 MHz - 6 GHz), Full-Duplex.
*   **DF Uzmanlığı:** **KrakenSDR**
    *   **Kabiliyet:** 5 kanallı koherent RX. Sadece Yön Bulma (DoA) için mükemmeldir.

## 3. Anten Sistemi
Geniş spektrumlu tarama ve odaklanmış karıştırma için hibrit bir yapı önerilir.

*   **Tarama ve Yön Bulma (ED):** 12'li Vivaldi Anten Dizisi (360° Radyal Yerleşim).
    *   **Yön Bulma (DF):** MUSIC veya Genlik Karşılaştırma algoritmaları için optimize edilmiş 12 kanallı pasif dağıtıcı/switch sistemi.
    *   **Karıştırma (ET):** 70 MHz - 6 GHz geniş bant kapsama alanına sahip Log-Periyodik Anten (Tripod üstü dikey yerleşim).

## 4. Güç ve Enerji Yönetimi
Saha görevleri için otonom batarya sistemi.

*   **Batarya:** 4S - 6S LiPo Batarya + Kararlı Voltaj Regülatörleri (PDB).
*   **RF Filtreleme:** SDR girişlerinde LNA (Low Noise Amplifier) ve belirli bantlar için Band-Pass filtreler.

## 5. Donanım-Yazılım Entegrasyon Şeması

```mermaid
graph TD
    subgraph "Saha Birimi (Tripod)"
        Anten[12x Vivaldi Dairesel Dizi] --> LNA[Filtre & LNA Blokları]
        LNA --> SDR[SDR Birimi - USRP/HackRF]
        SDR -->|USB 3.0| RPi[Raspberry Pi 5]
        LogP[Log-Periyodik Anten] --- PA[Güç Yükseltici]
        PA --- SDR
    end
    
    RPi -->|WiFi/Ethernet| Laptop[Operatör Laptop]
    Laptop -->|Görselleştirme| UI[Almasta-UI Dashboard]
```

## 6. Donanım Uyumlu Kod Yapısı
Sistem, `SoapySDR` veya `UHD` kütüphanelerini kullanarak donanım abstraksiyonu sağlar. Kod içindeki `SignalGenerator` ve `SpectrumAnalyzer` sınıfları, donanım bağlı olduğunda "Hardware mode"a otomatik geçecek şekilde tasarlanmıştır.
