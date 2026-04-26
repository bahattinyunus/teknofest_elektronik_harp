# 🛰️ TEKNOFEST 2026 Elektronik Harp Yarışması Kapsamlı Şartname Özeti

Bu doküman, TEKNOFEST 2026 Elektronik Harp (EH) yarışması şartnamesinin (V1.0) tüm teknik ve idari detaylarını içermektedir.

## 📌 1. Temel Bilgiler ve Takvim
- **Kategori:** Üniversite ve Üzeri (Ön Lisans, Lisans, Lisansüstü).
- **Takım Yapısı:** 3-8 öğrenci + 1 Danışman. (Finalde en fazla 5 kişi).
- **Önemli Tarihler:**
  - **Son Başvuru:** 10 Mart 2026
  - **Teknik Yeterlilik Formu (TYF):** 24 Mart 2026
  - **Kritik Tasarım Raporu (KTR):** 30 Nisan 2026
  - **Sistem Tanımlama Videosu (STV):** 14 Temmuz 2026 (Maks. 15 Dakika)
  - **Final:** Ağustos-Eylül 2026

## 🕵️‍♂️ 2. Elektronik Destek (ED) Görevleri
Sistemin EH operatörlerine durumsal farkındalık sağlama yetenekleridir.

### 2.1. Sinyal Tespiti
- Gürültü tabanını aşan yayınların otonom algılanması.
- Başlangıçta frekanslar gizli tutulur, takımlar kendisi bulmalıdır.

### 2.2. Parametre Çıkarımı
Şartname aşağıdaki parametrelerin çıkarılmasını bekler:
- Taşıyıcı Frekansı ve Bant Genişliği (BW).
- Güç Seviyesi.
- Analog/Sayısal Ayrımı.
- **Tercihen:** Modülasyon Türü, Protokol Türü, Çoklama Yöntemi (TDMA/FDMA/CDMA/OFDM), EKKT Tedbiri (FHSS/DSSS).

### 2.3. Sinyal İzleme ve Dinleme
- Tespit edilen yayının süreklilik takibi.
- **Analog Telsiz:** Demodülasyon ve ses çıkışı.
- **Sayısal Telsiz:** Kod çözümü (Tercihen puan artırır).

### 2.4. Yön Bulma (DF - Direction of Arrival)
- Önerilen Yöntemler: Genlik Tabanlı, Faz Karşılaştırmalı veya TDOA.
- Doğruluk "Derece RMS" olarak ölçülür.

### 2.5. Konum Belirleme (Geolocation)
- Sabit veya hareketli alıcılarla hedefin 2D/3D koordinat kestirimi.
- Hedefler yerde veya havada (Drone/İHA) olabilir.

## 🚀 3. Elektronik Taarruz (ET) Görevleri
Sistemin tehdit unsurlarını etkisiz hale getirme yetenekleridir.

### 3.1. Sürekli Karıştırma (Continuous Jamming)
- JSR (Jammer-to-Signal Ratio) optimizasyonu.
- Tipler: Tekli, Çoklu ve Baraj (Barrage) karıştırma.

### 3.2. Arabakışlı Karıştırma (Interleaved Jamming)
- Tespit ve karıştırma fazlarının zaman paylaşımlı yürütülmesi.
- Alıcı (Receiver) ile eşzamanlı çalışma gerektirir.

### 3.3. Analog Telsiz Aldatma (Spoofing)
- Hedefin "yanlış duymasını" sağlamak.
- Analog ses sinyallerinin taklidi veya modifiye edilerek yayılması.

### 3.4. GNSS Aldatma (GPS Spoofing)
- **Zorunlu:** GPS L1 aldatma sinyali.
- **Ek Puan:** L2, L5, GLONASS, GALILEO, BEIDOU servisleri.

## 🏆 4. Değerlendirme ve Ödül Kriterleri

### 4.1. Puanlama Dağılımı
- **KTR:** %15
- **Sistem Tanımlama Videosu:** %15
- **Görev Puanlaması (Saha):** %70

### 4.2. Minimum Başarı (Ödül Sıralaması İçin Şart)
Bir takımın ödül alabilmesi için en az şunları yapması şarttır:
- **ED:** Tespit + Parametre Çıkarımı + Yön Bulma (DF).
- **ET:** En az 1 Jamming (Örn: Sürekli) + En az 1 Spoofing (Örn: Analog Telsiz).

### 4.3. Özel Ödüller
- En İyi Takım Ruhu.
- ED/ET Alanında En İyi Sistem Mimarisi.
- En İyi Yapay Zekâ Uygulaması.
- En İyi Kullanıcı Arayüzü (UI).

## 🛠️ 5. Teknik Kontrol ve Kurallar
- Saha 1x1 km² açık alan olacaktır.
- Sistemler kullanıcı arayüzü üzerinden kontrol edilmeli ve anlık verileri gösterebilmelidir.
- Teknik kontrolde RF çıkış güçleri ve spektrum tarama kabiliyetleri test edilecektir.

---
*Almasta-AI projesi, yukarıdaki tüm zorunlu ve tercihli kriterleri (AI otonomi dahil) karşılayacak bir mimariyle geliştirilmektedir.*
