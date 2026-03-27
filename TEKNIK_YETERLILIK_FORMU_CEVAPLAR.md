# TEKNİK YETERLİLİK FORMU CEVAPLARI - TEKNOFEST ELEKTRONİK HARP YARIŞMASI 2026

**1. Yarışmaya katılacak olan Elektronik Harp (EH) Sistemi hangi alt sistemlerden oluşmaktadır?**
- [x] Elektronik Destek ve Elektronik Taarruz

**2. Yarışmaya katılacak olan EH Sistemi kaç adet Sistem’den oluşmaktadır?**
Sistem, toplamda **4 adet sistemden** oluşmaktadır. Elektronik Destek (ED) görevlerinde, özellikle TDOA (Time Difference of Arrival) ve AOA tabanlı konum belirleme işlemi için coğrafi olarak dağıtık 3 adet ED dinleme/kestirim sistemi, Elektronik Taarruz (ET) görevleri için ise 1 adet gelişmiş Karıştırma/Aldatma (ET) sistemi şeklinde planlanmıştır.

**3. Yarışmaya katılacak olan EH Sistemi hangi işlevleri yerine getirmektedir?**
**Elektronik Destek:**
- [x] Sinyal Tespiti
- [x] Parametre Çıkarımı
- [x] Sinyal İzleme/Dinleme
- [x] Yön Bulma (DF)
- [x] Konum Belirleme

**Elektronik Taarruz:**
- [x] Sürekli Karıştırma
- [x] Ara-Bakışlı Karıştırma
- [x] Analog Telsiz Aldatma
- [x] GNSS Aldatma

**4. Yarışmaya katılacak olan EH Sistemini tanıtınız.**
Sistemimiz; modüler, yapay zeka destekli ve Software Defined Radio (SDR) tabanlı entegre bir Elektronik Harp çözümüdür. Altyapı olarak Ettus USRP serisi ve/veya HackRF gibi SDR platformları kullanılacaktır. Hazır kullanıcı arayüzleri kesinlikle kullanılmayacak olup; C++/Python ve GNU Radio tabanlı DSP blokları entegrasyonuyla kendi geliştirdiğimiz özgün komuta kontrol yazılımı üzerinden yönetilecektir. Sistem, spektrumu akıllı otonom algoritmalarla analiz edip hedefe dinamik reaksiyon (karıştırma/aldatma) verebilen kapalı çevrim bir yapıya sahiptir.

**5. Sistem mimarinizi açıklayınız.**
Detaylı Sistem Blok Şeması daha sonra KYS sistemine görsel olarak eklenecektir. (Not: Sistem, SDR'dan gelen I/Q verilerini TCP/ZMQ üzerinden merkezi bir işleme ve Karar-Destek (AI) modülüne ileten ve karar sonucuna göre SDR Transmitter modülünü tetikleyen çevrim içi bir mimariden oluşmaktadır.)

**6. Sistemin entegre olacağı platformu açıklayınız.**
- [x] Karada, Taşınabilir (kullanım sırasında sabit)
**Kullanım Şekli:**
Sistem, operasyon bölgesine tekerlekli veya askeri taşıma çantalarıyla intikal ettirilebilen "Manga/Tim Seviyesi Taşınabilir" bir yapıdadır. Kurulum aşamasında tripod veya taktiksel kule benzeri yapılar üzerine anten dizileri yerleştirilerek, kullanım sırasında sabit (fixed-site) kalacak biçimde işletilecektir. 

**7. Elektronik Destek Sisteminin “Çalışma Frekans Bandı” nedir?**
70 MHz - 6000 MHz

**8. Elektronik Destek Sistemi kaç kanaldan oluşacaktır? Almaç anlık bant genişliği için ne öngörülmektedir?**
- DF için Kanal Sayısı: 4 kanal (Faz uyumlu)
- DF için Almaç Anlık Bant Genişliği: 160 MHz
- Monitör/İzleme için Kanal Sayısı: 1 kanal
- Monitör/İzleme için Anlık Bant Genişliği: 160 MHz

**9. Elektronik Destek Sistemi’nde “Sinyal Tespiti” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Geniş bantlı spektrum tarama yöntemiyle elde edilen I/Q verileri üzerinden sürekli FFT işlemleri uygulanacak ve oluşturulan güç spektral yoğunluk (PSD) verisi, CFAR (Constant False Alarm Rate) ve Enerji Tespiti algoritmaları ile işlenecektir. Arka planda değişen gürültü eşikleri dinamik hesaplanıp, gürültü zemininin üzerine çıkan dar ve geniş bantlı muhabere sinyalleri otomatik olarak tespit edilerek kaydedilecektir.

**10. Elektronik Destek Sistemi’nde “Parametre Çıkarımı” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Tespit edilen sinyalin I/Q örnekleri üzerinden Digital Down Conversion (DDC) uygulanarak sinyal ana banda indirilecektir. Hilbert dönüşümü ve anlık faz/frekans/genlik analizleriyle; Merkez Frekansı, Bant Genişliği, Sinyal/Gürültü Oranı (SNR) gibi temel parametreler elde edilecektir. Modülasyon Tipi (AM, FM, ASK, FSK, PSK, QAM varyantları) ve Sembol Hızı (Baud Rate) çıkarımı ise otonom yapay zeka (Derin Öğrenme) algoritmalarımız ile IQ verisinden ve spektrogram özelliklerinden doğrudan saptanacaktır.

**11. Elektronik Destek Sistemi’nde “Sinyal İzleme/Dinleme” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Hedef sinyale uygulanan DDC işleminin ardından, saptanan modülasyon tipine (AM, FM veya sayısal modülasyonlar) uygun demodülatör bloklarımız (Costas loop, PLL vb. ile kilitlenerek) devreye girecektir. Analog ses içerikli telsiz sinyalleri demodüle edilerek doğrudan operatörün ses arayüzüne veya kayıt ortamına (WAV) aktarılacaktır. Sayısal sinyaller ise bit katmanına kadar çıkarılarak binary (HAM) data şeklinde izlenecebilecek ve analiz için veritabanına kaydedilebilecektir.

**12. Elektronik Destek Sistemi’nde “Yön Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
4 kanallı, faz uyumlu (phase-coherent) SDR altyapısı ve dairesel veya doğrusal dizilimli ölçüm antenleri kullanılarak MUSIC (Multiple Signal Classification) ve Correlative Interferometry algoritmaları koşturulacaktır. Antenlere gelen sinyallerin uzamsal faz ve genlik farkları işlenerek yüksek çözünürlüklü yön tayini yapılacak, hedeflenen çalışma bandında RMS < 3-5 derece civarında bir yön bulma kesinliği hedeflenmektedir.

**13. Elektronik Destek Sistemi’nde “Konum Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Konum bulma, coğrafi olarak yayılmış 3 farklı ED donanım birimi üzerinden gerçekleştirilecektir. Sistemin her bir düğümü, hedef sinyali mikro-saniye hassasiyetli GPS zaman damgaları (PPS) ile etiketleyecektir. Ana merkeze aktarılan I/Q verileri çapraz korelasyona (Cross-Correlation) sokularak TDOA (Varış Zamanı Farkı) kestirimi yapılacak, eş zamanlı üretilen AOA (Yön) vektörleriyle birleştirilip Genişletilmiş Kalman Filtreleri (EKF) yardımıyla yüksek hassasiyetli X,Y lokasyon tahmini yapılacaktır.

**14. Elektronik Destek Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
Sinyal yoğunluğunun yüksek, gürültünün değişken olduğu karmaşık harp ortamında geleneksel algoritmalar hantallaşmaktadır. Bu nedenle ED alt sisteminde I/Q verilerini girdi olarak kabul eden 1D/2D Evrişimli Sinir Ağları (CNN) veya transformer tabanlı ağlar kullanılacaktır. Temel kullanım alanı; klasik yöntemlerle sınıflandırılması güçleşen düşük SNR'lı sinyallerin Modülasyon Türünü otomatik ve anlık olarak sınıflandırmak (AM/FM/FSK/BPSK/Lojik vb.) ve spektrogram görüntüleri üzerinden anomali veya spesifik frekans atlamalı (frequency hopping) hedeflerin tespit (Spectrum Sensing) işlemleridir.

**15. Yarışmaya katılacak olan Elektronik Destek Alt Sistemi’nin SwaP (Size, Weight and Power) bilgilerini belirtiniz.**
- Boyutlar (En x Boy x Yükseklik): 450 x 350 x 200 mm (SDR, işlemci üniteleri ve RF katı dahil muhafaza kutusu ölçüleridir, anten yayıcı birimler hariçtir.)
- Sistem Ağırlığı: ~8 kg (Birim başına)
- Çekilen Güç: 100 W (DC / 12-24V ile çalışacak şekilde optimize edilecektir.)

**16. Elektronik Taarruz Sisteminin Çalışma Frekans Bandı nedir?**
70 MHz - 6000 MHz

**17. Elektronik Taarruz Sistemi kaç Alt Banttan oluşacaktır? Bant başına RF çıkışı gücü için ne öngörülmektedir?**
- Karıştırma için Alt Bant Sayısı: 2
- Karıştırma için Bant Başına RF Çıkış Gücü: Yüksek verimli Solid State Güç Yükselteçleri (SSPA) kullanılarak bant başına 20 W RF çıkış gücü hedeflenmektedir. Göreve özgü, yönlü antenler (yaklaşık 8-12 dBi kazançlı Log-Periyodik veya Horn yapılı) tasarlanacak/kullanılacaktır. Eşyönlü (Omni) anten seçeneği de taktik duruma göre aktif edilebilecektir. 
- Aldatma için Alt Bant Sayısı: 2
- Aldatma için Bant Başına RF Çıkış Gücü: Aldatma konsepti gereği hedef almacı hassas olarak manipüle edeceğinden, 10 W çıkış güçlü bir yükselteç kullanılacaktır. Yönlü anten tercih edilecek (yaklaşık 10 dBi kazanç), böylece sızma (injection) etkinliği maksimize edilecektir.

**18. Elektronik Taarruz Sistemi’nde “Sürekli Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Sürekli karıştırma modunda sistem, DRFM (Digital Radio Frequency Memory) ve DDS (Direct Digital Synthesizer) mantıklarını yazılımsal olarak simüle ederek çalışacaktır. Hedefe Spot (dar bant, yüksek yoğunluklu ses tonu ya da gürültü), Sweep (belirli bir frekans aralığını dinamik süpürerek 5-10 hedefe kadar çoklu etki) ve Baraj Karıştırma (örneğin 20 MHz genişliğinde bant örtücü AWGN veya Comb karıştırma) uygulanacabilecektir. 

**19. Elektronik Taarruz Sistemi’nde “Arabakışlı Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Look-through (Ara-bakış) karıştırmada SDR platformunun hızlı TX/RX anahtarlama yeteneğinden faydalanılacaktır. Sistem örneğin %90 oranında Karıştırma (TX), %10 oranında Dinleme (RX) zaman dilimlerine ayrılacaktır (Mili/Mikro-saniye seviyesinde anahtarlama tahsisleri). Dinleme periyodunda hedef sinyalin hala yayında olup olmadığı anlık FFT/enerji tespiti ile yoklanacaktır. Yayını kesen hedefler için karıştırma otomatik durdurularak spektrum hijyeni ve güç tasarrufu sağlanacak, frekans atlayan hedefler varsa yeni kanala hızlıca yönelme yapılacaktır.

**20. Elektronik Taarruz Sistemi’nde “Analog Telsiz Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Analog telsiz ve haberleşme sistemlerine yönelik asimetrik taarruz için, önceden hazırlanmış veya anlık sentezlenmiş yanıltıcı ses örnekleri, hedef kanalın spesifik modülasyonuyla (çoğunlukla NBFM/AM) modüle edilecektir. Operasyonel kanala, gerçek hedeften "daha güçlü" (Power Capture / Capture Effect) bir sinyal sızdırması yapılarak düşman haberleşme ağına sahte rapor, ton veya parazitli anons sokma şeklinde aldatma koşturulacaktır.

**21. Elektronik Taarruz Sistemi’nde “GNSS Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
GPS (L1, 1575.42 MHz) spektrumunda, SDR üzerinden GPS uydu efemeris(yörünge) verileri dinamik bir şekilde yeniden sentezlenecektir (Spoofing). Böylece hedef GNSS alıcısının kilitlendiği asıl uydu sinyalleri üzerine, daha güçlü fakat yanlış zaman (Timing Spoofing) veya yanlış koordinat (Position Spoofing) taşıyan sentetik PRN kodları ve navigasyon mesajları gönderilecek, hedefin rotasından çıkması veya senkronizasyon kaybetmesi sağlanacaktır.

**22. Elektronik Taarruz Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
ET kapsamında "Bilişsel Elektronik Harp (Cognitive EW)" yaklaşımı uygulanacaktır. Özellikle frekans atlamalı (Frequency Hopping) veya otonom uyarlanabilir haberleşme yapan hedefleri kırmak için, Pekiştirmeli Öğrenme (Reinforcement Learning) modelleri kullanılacaktır. Bu modeller hedefin atlama paternlerini gerçek zamanlı olarak izleyip öğrenerek, bir sonraki geçeceği kanal frekansını ve zamanını tahmine (prediction) dayalı hedefleyici / akıllı önleyici karıştırma stratejilerini yöneteceklerdir.

**23. Yarışmaya katılacak olan Elektronik Taarruz Alt Sistemi’nin SwaP bilgilerini belirtiniz.**
- Boyutlar: 550 x 450 x 250 mm (Çoklu SDR ve Güç Yükselteç (PA) Soğutma blokajlı muhafaza.)
- Sistem Ağırlığı: ~15 kg (Isı alıcı bileşenlerle birlikte)
- Çekilen Güç: 300 W (Kullanılacak PA'ların durumuna göre AC 220V destekli yüksek kapasiteli PSU veya doğrudan DC 24-48V sistemler üzerinden besleme sağlanacaktır.)
