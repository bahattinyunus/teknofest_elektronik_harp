# 🏗️ Aegis-AI Sistem Yapısı: DKB & YKB Tanımları

TEKNOFEST 2026 Elektronik Harp Şartnamesi (Bölüm 6.1.2) gereğince, sistemin Donanım Konfigürasyon Birimleri (DKB) ve Yazılım Konfigürasyon Birimleri (YKB) aşağıda tanımlanmıştır.

## 1. Donanım Konfigürasyon Birimleri (DKB)

| DKB Kodu | Birim Adı | Fonksiyonel Açıklama |
| :--- | :--- | :--- |
| **DKB-01** | **SDR Alıcı/Verici Ünitesi** | Geniş bantlı RF sinyallerini I/Q verisine dönüştüren ve karıştırma sinyallerini yayan ana RF katmanı (Ettus USRP / PlutoSDR). |
| **DKB-02** | **İşleme Birimi (SBC)** | Algoritmaların koştuğu, GPU destekli yüksek performanslı işlemci ünitesi (NVIDIA Jetson / x86 PC). |
| **DKB-03** | **Anten Dizisi** | Yön Bulma (DF) ve Karıştırma (Jamming) için kullanılan 4x Monopol ve 1x Yönlü anten seti. |
| **DKB-04** | **Güç ve Enerji Yönetimi** | Sistemin saha operasyonları için ihtiyaç duyduğu DC/AC dönüşümü ve batarya bloğu. |

## 2. Yazılım Konfigürasyon Birimleri (YKB)

| YKB Kodu | Birim Adı | Temel Sorumluluklar |
| :--- | :--- | :--- |
| **YKB-01** | **Sinyal Analiz Motoru** | FFT, Parametre Çıkarımı (PRI, PW, BW), Modülasyon ve Çoklama (Multiplexing) Tanıma. |
| **YKB-02** | **AI Karar Destek Birimi** | Tehdit Kütüphanesi eşleşmesi, Otonom Strateji Belirleme ve Tehdit Önceliklendirme. |
| **YKB-03** | **ET Kontrol Modülü** | Karıştırma (Jamming) ve Aldatma (Spoofing) sinyal üretimi, Co-site girişim engelleme. |
| **YKB-04** | **Taktik Arayüz (UI)** | Operatöre anlık spektrum görünümü, tehdit lokasyonu (2D) ve sistem durumu sunan web tabanlı panel. |
| **YKB-05** | **Görev Simülatörü** | Test ve eğitim amaçlı sentetik EH ortamı ve emitter oluşturma ünitesi. |

---
*Bu yapı, sistemin modülerliğini ve TEKNOFEST EH görevlerinin her birine karşılık gelen spesifik bir birim olduğunu doğrulamaktadır.*
