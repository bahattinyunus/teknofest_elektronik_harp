# Mergen-AI: Kapsamlı Yazılım Mimarisi ve Şartname Uyum Rehberi

Bu doküman, Mergen-AI projesinin yazılım mimarisini, TEKNOFEST 2026 Elektronik Harp Şartnamesi'nde belirtilen kurallar, fiziksel kısıtlar (SWaP) ve teknik isterler çerçevesinde detaylı bir biçimde incelemek üzere hazırlanmıştır. Amacı, geliştirici ekibe ve teknik değerlendiricilere sistemin nasıl çalıştığını profesyonel ve yapılandırılmış bir eğitim dokümanı formatında aktarmaktır.

Hiyerarşik ve modüler bir yapıda tasarlanan yazılımımız, yalnızca bir kod bütünü değil; donanım limitlerine saygı duyan, deterministik kararlar alabilen ve kapalı çevrim çalışan bir karar destek (otonomi) sistemidir.

---

## 1. Fiziksel Kısıtların Yazılım Mimarisine Etkisi (SWaP Optimizasyonu)

Şartname gereği, sistemin Boyut, Ağırlık ve Güç (SWaP - Size, Weight, and Power) kısıtlarına tam uyum sağlaması gerekmektedir:
*   **Fiziksel Yapı:** Sistem, Ana ve Yavru Ünite olmak üzere iki birimden oluşur. Toplam ağırlık maksimum 20 kg (ünite başına <10 kg) ile sınırlandırılmıştır.
*   **Güç Tüketimi:** Dizüstü bilgisayar haricinde tüm sistemin (SDR, işlemci, antenler ve Güç Yükselticiler dahil) toplam anlık güç tüketimi **150 Watt** sınırını aşmamalıdır.
*   **Yüksek Enerji Çeken Birimler:** Elektronik Taarruz (ET) katmanında bulunan 4 adet Güç Yükseltici (PA), sistemin birincil güç tüketicileridir (yaklaşık 80-100W). 

**Yazılım Perspektifinden Optimizasyon İhtiyacı:**
Bu kısıtlar altında, algoritmik verimlilik hayati önem taşır. C++ ve Python dilleriyle geliştirilen çekirdek yazılım modüllerimizin (özellikle FFT ve Yapay Zeka çıkarım süreçlerinin), Raspberry Pi 5 veya NVIDIA Jetson gibi Edge (uç/sınır) donanımlarda **en düşük CPU/GPU döngüsüyle** çalışması zorunludur. Yazılımda yaşanacak bir bellek sızıntısı (memory leak) veya verimsiz bant genişliği kullanımı, işlemcinin daha fazla güç çekmesine neden olarak tüm sistemi 150W sınırının ötesine taşıyarak diskalifiye riski yaratacaktır.

---

## 2. Yazılım Konfigürasyon Birimleri (YKB) Çerçevesi

Sistem, `DKB_YKB_STRUCTURE.md` standartlarında belirtilen modüler yapıdaki Yazılım Konfigürasyon Birimlerine (YKB) bölünmüştür. Bu birimler şöyledir:

*   **`YKB-01` Sinyal Analiz Motoru:** Dijital sinyal işleme (DSP) yeteneklerini barındırır. Spektrum taranması, Darbe Genişliği (PW), Bant Genişliği (BW) ve Darbe Tekrarlama Aralığı (PRI) tayini bu modülde işletilir.
*   **`YKB-02` AI Karar Destek Birimi:** Otomatik Modülasyon Sınıflandırma (AMC) ve elde edilen sinyal özelliklerinin "Tehdit Kütüphanesi" ile eşleştirilerek hedefin teşhis edilmesi süreçlerini yönetir.
*   **`YKB-03` ET Kontrol Modülü:** Elektronik Taarruz stratejilerinin (Karıştırma ve Aldatma) algoritmik olarak sentezlendiği ve SDR (Software Defined Radio) üzerinden yayına verildiği katmandır.
*   **`YKB-04` Taktik Arayüz (UI):** Operatörün tüm sinyal ortamını ve otonom kararları gerçek zamanlı olarak izlediği, müdahalelerde bulunduğu komuta kontrol katmanıdır.

---

## 3. Elektronik Destek (ED) Süreçleri: Tespit ve Analiz

Elektronik Destek (ED) yeteneği, 70 MHz ile 6000 MHz aralığındaki hedeflerin (gizli frekans dâhil) otonom olarak bulunmasını hedefler.

### 3.1. Sinyal Tespiti ve Parametre Çıkarımı
SDR üzerinden akan milyonlarca I/Q (In-phase/Quadrature) örneği, öncelikle pencereleme işlemlerinden (örneğin Hanning, Blackman-Harris) geçirilerek Hızlı Fourier Dönüşümüne (FFT) tabi tutulur.
*   **Dinamik Eşikleme (CFAR):** Sistem, sürekli olarak çevre gürültüsünü hesaplar (Noise Floor). Sabit Yanlış Alarm Oranı (CFAR) algoritması sayesinde, gürültü zeminini belli bir eşik değerin üzerinde aşan gerçek sinyal tepe noktaları (peak) matematiksel olarak izole edilir.
*   **Parametre Çıkarımı:** İzole edilen sinyale uygulanan analitik hesaplamalarla sinyalin Taşıyıcı Frekansı, Bant Genişliği (BW) ve efektif güç seviyesi (dBm) hesaplanıp kayıt altına alınır.

### 3.2. Yapay Zeka ile Modülasyon Sınıflandırma (AMC)
Yalnızca enerji tespitine dayalı yaklaşımlar, modern LPI (Düşük Tespit Edilme Olasılıklı) radarları teşhis etmede yetersiz kalır. Bu engeli aşmak adına, makine öğrenmesi algoritmaları entegre edilmiştir.
*   Zaman serisi halindeki I/Q verileri, **Wigner-Ville Distribution (WVD)** veya eşzamanlı Spektrogram kullanılarak 2 boyutlu zaman-frekans matrislerine dönüştürülür.
*   Bu matrisler, önceden eğitimli 1B/2B Evrişimli Sinir Ağlarına (CNN) beslenerek, çok yollu sönümlenme (multipath fading) ve Doppler kayması gibi bozucular altında dahi modülasyon tipi (QPSK, FM, vb.) yüksek ihtimalle sınflandırılır.

### 3.3. Yön (DoA) ve Coğrafi Konum (Geolocation) Hesaplama
*   **DoA (Direction of Arrival):** Ana ünite üzerindeki çoklu Vivaldi anten dizisi (dairesel yerleşimli), gelen sinyal dalga cephesinin anten elemanlarına ulaşma sürelerindeki nanosaniyelik faz farkını işler. Dar bantta MUSIC (Multiple Signal Classification) algoritması kullanılarak sinyalin geliş açısı yüksek bir çözünürlükle ve düşük RMS hata payıyla saptanır.
*   **TDOA Füzyonu (Geolocation):** Ana ve Yavru ünitelerin hesapladığı yön vektörleri, ağ üzerinden merkez işlemciye iletilir. İki farklı istasyondan gelen Varış Zaman Farkı (TDOA - Time Difference of Arrival) ve kesişim açıları korele edilerek, tehdit unsurunun 2 boyutlu coğrafi koordinatı hesaplanmakta ve taktik haritaya işlenmektedir.

---

## 4. Elektronik Taarruz (ET) Süreçleri: Müdahale ve Karşı Tedbir

Şartname, elektronik harp sahasında saldırı tekniklerinin dinamik ve asimetrik olmasını zorunlu kılar.

### 4.1. Sürekli (Continuous) Karıştırma
Kritik bir frekans bloğunun tamamen devredışı bırakılması hedefleniyorsa, algoritma **Toplu Gürültü (Barrage AWGN)** veya tek bir taşıyıcı frekansı hedef alan **Nokta (Spot)** karıştırma sinyalleri sentezler. Bu sinyaller, belirlenen frekans bandına SDR gücü ve Güç Yükselticisi (PA) aracılığıyla aktarılır.

### 4.2. Arabakışlı (Look-through) Karıştırma
Şartnamenin en ileri düzey beklentilerinden biri olan zaman paylaşımlı taarruzdur. Arabakışlı karıştırmada sistem, hedefe tamamen kör bir biçimde sürekli bastırma uygulamak yerine, **%90 Gönderme (TX) / %10 Dinleme (RX)** iş çevrimine (Duty Cycle) girer. 
*   **İşleyiş:** Karıştırma işlemi çok kısa bir süre duraklatılır, ortam dinlenir. Hedefin yayını kesip kesmediği veya başka bir kanala frekanslayıp atlamadığı tespit edilir. Eğer hedef ortadan kalkmışsa karıştırma durdurularak gereksiz güç (Watt) kaybı önlenir; farklı bir frekansa atlamışsa (FHSS), taarruz algoritması saniyeden kısa süre içinde hedefin yeni frekansına taşınır.

### 4.3. Analog ve GNSS (GPS L1) Aldatma Kurgusu
*   **Analog Aldatma (Spoofing):** Operatör veya sistem, hedef telsiz kanalının üzerine "Ele Geçirme Etkisi (Capture Effect)" mantığıyla daha yüksek bir yayın basar ve sahte bir ses taşıyıcısı kanalize eder.
*   **GNSS Spoofing:** Modern İHA'ları etkisiz kılmanın en kritik yöntemidir. Sistem, güncel Uydu Efemeris (Yörünge) verilerini işleyerek sentetik bir PRN (Pseudo-Random Noise) kod üreteci çalıştırır. SDR üzerinden GPS L1 (1575.42 MHz) bandında yayınlanan bu yörünge aldatmacası füzelerin ve dronların otonom seyir bilgisayarını aldatarak, aracı sanal ve yanlış bir coğrafi konuma sürükler.

---

## 5. Bilişsel (Cognitive) EH ve Teknoloji Yığını

Mergen-AI projesi, endüstri standardı bir araştırma ve geliştirme felsefesini kullanır:

*   **Pekiştirmeli Öğrenme (RL - Reinforcement Learning):** Düşmanın frekans atlama desenini öğrenerek "bir sonraki hedef noktasını" önceden tahmin eden PPO ve DQN tabanlı akıllı ajanların eğitim süreci entegre edilmiştir.
*   **Uç Yonga Çıkarımı (Edge AI Inferencing):** Eğitimli derin öğrenme ağları, donanım kaynaklarını optimize etmek amacıyla NVIDIA TensorRT altyapısında Float16 (FP16) veya INT8 hassasiyetine quantize edilmiştir.
*   **Genişletilebilir Donanım Katmanı:** `SoapySDR` kullanılarak yazılan DSP mimarisi, farklı donanım portföyleriyle (USRP, HackRF, PlutoSDR vb.) donanımdan tamamen bağımsız olarak kullanılabilir.

---

## 6. Komuta Kontrol Alanı: Taktik Arayüz (YKB-04)

Bütüncül bir durumsal farkındalık (Situational Awareness), modern bir EH sisteminin kilit bileşenidir. Kurallar, sürecin mutlaka bir Kullanıcı Arayüzünden idare edilmesini gerektirir.

*   Sistemin arka ucu (Backend), Flask veya FastAPI ile asenkron bir web sunucusu çalıştırır.
*   **Veri Görselleştirme:** Milisaniyelik gecikmelerle akan Şelale (Waterfall) ve Spektrum yoğunluk grafikleri, `WebSocket` protokolü aracılığıyla tarayıcıya iletilir.
*   Arayüz üzerinde I/Q Takımyıldızları (Constellation), Yapay Zeka Karar Güven Haritaları (Softmax Outputs) ve Leaflet.js destekli otonom hedeflerin konumlandığı 2B taktiksel bir dijital harita yer almaktadır.

---

## 7. Örnek Operasyonel Senaryo Tahlili

Sistemin bütünsel döngüsünü somutlaştırmak adına şu uçtan uca akış incelenebilir:
1. **Tespit:** Ana ünite üzerindeki tarayıcı anten katarı, 2.4 GHz frekans bloğunda bir yayın keşfeder.
2. **Karakterizasyon:** `analyzer.py` algoritması sinyalin dar bantlı, periyodik veri pakteleri (Drone kontrol sinyali) formunda olduğunu hesaplar.
3. **Sınıflandırma:** Evrişimli Sinir Ağı modeli, bu paketin %96 olasılıkla özel bir FHSS kontrol protokolüne ait olduğunu operatörün ekranına loglar.
4. **Coğrafi Bildirim:** TDOA kullanan `tracking.py` modülü, hedef yönünü 120 derece Doğu olarak belirler ve dijital haritada işaretler.
5. **Karşı Tedbir:** Sistemin "Reaktif" durumdan "Taarruz" durumuna alınması durumunda, Karar Destek AI modülü Arabakışlı (Look-through) Karıştırma prosedürünü işletir.
6. **Sonuçlandırma:** Sentezlenen 10W'lık taarruz sinyali, L1 GPS aldatma paketi ile birleştirilerek hedefe gönderilir; hedefin kendi ağıyla teması kesilir ve sahte operasyon bölgesine düşmesi sağlanır. Sistemin otonom güç yönetimi, bu akışı 150W tavan sınırının daima altında tutarak tamamlar.

> *Bu doküman, sistem donanımı ve yazılımının, birbiriyle izole çalışmak yerine tek bir akıl olarak TEKNOFEST kalite normlarına nasıl asimile edildiğini profesyonel ve teknik bir dille özetlemektedir.*
