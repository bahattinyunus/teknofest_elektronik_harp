# TEKNİK YETERLİLİK FORMU CEVAPLARI - TEKNOFEST ELEKTRONİK HARP YARIŞMASI 2026

**1. Yarışmaya katılacak olan Elektronik Harp (EH) Sistemi hangi alt sistemlerden oluşmaktadır?**
- [x] Elektronik Destek ve Elektronik Taarruz

**2. Yarışmaya katılacak olan EH Sistemi kaç adet Sistem’den oluşmaktadır?**
Sistem, coğrafi olarak dağıtık **2 ana üniteden** oluşmaktadır: Bir adet **Ana ED/ET Ünitesi** ve bir adet **Yavru ED/ET Ünitesi**. Bu yapı, hem Elektronik Destek (konum belirleme vb.) hem de Elektronik Taarruz görevlerinin iki farklı noktadan koordineli yürütülmesini sağlar. Toplam sistem ağırlığı 20 kg'ın altında tutulacak şekilde optimize edilmiştir.

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
Sistem mimarimiz, **Ana Ünite** ve **Yavru Ünite** olmak üzere iki temel ayaktan oluşur. Ana ünite, 20x30 cm boyutlarında dairesel dizilmiş 8 adet Vivaldi antenden oluşan bir ED dizisine ve hemen üzerinde 1 metre yüksekliğinde Log-Periyodik ET antenine sahiptir. Yavru ünite ise 90 derece yerleşimli Vivaldi anten dizisi ve benzer bir ET birimi barındırır. Her iki ünite de 120 cm boyundaki tripodlar üzerine konumlandırılmıştır. I/Q verileri bu iki ünite arasında senkronize edilerek merkezi işleme birimine aktarılır.

**6. Sistemin entegre olacağı platformu açıklayınız.**
- [x] Karada, Taşınabilir (kullanım sırasında sabit)
**Kullanım Şekli:**
Sistem, operasyon bölgesine tekerlekli veya askeri taşıma çantalarıyla intikal ettirilebilen "Manga/Tim Seviyesi Taşınabilir" bir yapıdadır. Kurulum aşamasında tripod veya taktiksel kule benzeri yapılar üzerine anten dizileri yerleştirilerek, kullanım sırasında sabit (fixed-site) kalacak biçimde işletilecektir. 

**7. Elektronik Destek Sisteminin “Çalışma Frekans Bandı” nedir?**
70 MHz - 6000 MHz

**8. Elektronik Destek Sistemi kaç kanaldan oluşacaktır? Almaç anlık bant genişliği için ne öngörülmektedir?**
- DF için Kanal Sayısı: 8 kanal (Ana ünite dairesel dizilim için)
- DF için Almaç Anlık Bant Genişliği: 160 MHz (Donanım limitlerine bağlı olarak optimize edilecektir)
- Monitör/İzleme için Kanal Sayısı: 2 kanal (Ana ve Yavru üniteler için)
- Monitör/İzleme için Anlık Bant Genişliği: 160 MHz

**9. Elektronik Destek Sistemi’nde “Sinyal Tespiti” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Geniş bantlı spektrum tarama yöntemiyle elde edilen I/Q verileri üzerinden sürekli FFT işlemleri uygulanacak ve oluşturulan güç spektral yoğunluk (PSD) verisi, CFAR (Constant False Alarm Rate) ve Enerji Tespiti algoritmaları ile işlenecektir. Arka planda değişen gürültü eşikleri dinamik hesaplanıp, gürültü zemininin üzerine çıkan dar ve geniş bantlı muhabere sinyalleri otomatik olarak tespit edilerek kaydedilecektir.

**10. Elektronik Destek Sistemi’nde “Parametre Çıkarımı” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Tespit edilen sinyalin I/Q örnekleri üzerinden Digital Down Conversion (DDC) uygulanarak sinyal ana banda indirilecektir. Hilbert dönüşümü ve anlık faz/frekans/genlik analizleriyle; Merkez Frekansı, Bant Genişliği, Sinyal/Gürültü Oranı (SNR) gibi temel parametreler elde edilecektir. Modülasyon Tipi (AM, FM, ASK, FSK, PSK, QAM varyantları) ve Sembol Hızı (Baud Rate) çıkarımı ise otonom yapay zeka (Derin Öğrenme) algoritmalarımız ile IQ verisinden ve spektrogram özelliklerinden doğrudan saptanacaktır.

**11. Elektronik Destek Sistemi’nde “Sinyal İzleme/Dinleme” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Hedef sinyale uygulanan DDC işleminin ardından, saptanan modülasyon tipine (AM, FM veya sayısal modülasyonlar) uygun demodülatör bloklarımız (Costas loop, PLL vb. ile kilitlenerek) devreye girecektir. Analog ses içerikli telsiz sinyalleri demodüle edilerek doğrudan operatörün ses arayüzüne veya kayıt ortamına (WAV) aktarılacaktır. Sayısal sinyaller ise bit katmanına kadar çıkarılarak binary (HAM) data şeklinde izlenecebilecek ve analiz için veritabanına kaydedilebilecektir.

**12. Elektronik Destek Sistemi’nde “Yön Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Ana ünitede bulunan 20x30 cm boyutlarındaki dairesel dizilimli **8 adet Vivaldi anten** üzerinden MUSIC ve Correlative Interferometry algoritmaları koşturulacaktır. Antenlere gelen sinyallerin uzamsal faz farkları ve genlik oranları işlenerek yüksek çözünürlüklü yön (AOA) kestirimi yapılacaktır. Vivaldi antenlerin geniş bant ve yüksek kazanç karakteristiği sayesinde RMS yön doğruluğu hedefimiz < 3 derecedir.

**13. Elektronik Destek Sistemi’nde “Konum Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Konum bulma, coğrafi olarak ayrılmış **Ana ve Yavru sistem (2 istasyon)** üzerinden gerçekleştirilecektir. Her iki ünite de hedef sinyali GPS/PPS zaman damgalarıyla etiketleyecektir. İki noktadan alınan veriler üzerinden hem Varış Zamanı Farkı (TDOA) hem de AOA (Yön) verileri füzyonlanarak hedefin koordinatları kestirilecektir. Tripodlar arası mesafe ve GPS hassasiyeti konum doğruluğunu belirleyen temel unsurlar olacaktır.

**14. Elektronik Destek Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
Sistemimizde, sinyal yoğunluğunun yüksek ve gürültü karakteristiğinin dinamik olduğu harp sahası koşullarını yönetmek için çok katmanlı bir Yapay Zeka mimarisi kullanılacaktır:
1.  **Otomatik Modülasyon Sınıflandırma (AMC):** Ham I/Q verileri üzerinden derin öznitelik çıkaran ResNet tabanlı evrişimli ağlar (CNN) ve sinyalin zamansal bağımlılıklarını yakalayan Attention (Transformer) mekanizmaları entegre edilecektir. Bu sayede düşük SNR (-5dB ve altı) değerlerinde bile yüksek doğrulukla modülasyon teşhisi yapılacaktır.
2.  **Sinyal Ayrıştırma (De-interleaving):** Karmaşık darbe katarı (pulse train) içerisinden farklı kaynaklara ait sinyalleri ayırmak için 'Unsupervised Clustering' (DBSCAN/HDBSCAN) ve LSTM tabanlı dizi tahminleyiciler kullanılacaktır.
3.  **Anomali Tespiti:** Spektrumun normal davranışını öğrenen 'Autoencoder' yapıları ile siber-fiziksel saldırılar veya yeni nesil 'Low Probability of Intercept' (LPI) sinyalleri anlık olarak tespit edilecektir.
Modellerimiz ONNX formatına dönüştürülerek uç cihazlarda (Edge AI) TensorRT optimizasyonu ile gerçek zamanlı (latency <10ms) koşturulacaktır.

**15. Yarışmaya katılacak olan Elektronik Destek Alt Sistemi’nin SwaP (Size, Weight and Power) bilgilerini belirtiniz.**
- **Boyutlar:** Ana ED ünitesi 20x30 cm dairesel dizeye sahiptir. Yerden yükseklik tripod dahil 120 cm'dir.
- **Ağırlık:** Ünite başına < 10 kg, toplam sistem (ED+ET+Destek) < 20 kg.
- **Güç:** Sistemin toplam güç tüketimi (ET dahil, laptop hariç) < 150 Watt olarak öngörülmektedir.

**16. Elektronik Taarruz Sisteminin Çalışma Frekans Bandı nedir?**
70 MHz - 6000 MHz

**17. Elektronik Taarruz Sistemi kaç Alt Banttan oluşacaktır? Bant başına RF çıkışı gücü için ne öngörülmektedir?**
- Karıştırma/Aldatma için Alt Bant Sayısı: **4 farklı bant** (Dinamik olarak seçilebilir).
- Bant Başına RF Çıkış Gücü: Her iki ünitede (Ana ve Yavru) yer alan 100 cm yüksekliğindeki **Log-Periyodik antenler** kullanılacaktır. Toplamda 4 adet güç yükseltici (PA) üzerinden beslenen sistemde, antenlere aktarılan güç ve donanım beslemeleri dahil toplam tüketim 150W altında kalacak şekilde tasarım yapılmıştır. PA birimleri metal kafes ve aktif fan soğutmalı bölmelerde muhafaza edilmektedir.

**18. Elektronik Taarruz Sistemi’nde “Sürekli Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Sürekli karıştırma modunda sistem, DRFM (Digital Radio Frequency Memory) ve DDS (Direct Digital Synthesizer) mantıklarını yazılımsal olarak simüle ederek çalışacaktır. Hedefe Spot (dar bant, yüksek yoğunluklu ses tonu ya da gürültü), Sweep (belirli bir frekans aralığını dinamik süpürerek 5-10 hedefe kadar çoklu etki) ve Baraj Karıştırma (örneğin 20 MHz genişliğinde bant örtücü AWGN veya Comb karıştırma) uygulanacabilecektir. 

**19. Elektronik Taarruz Sistemi’nde “Arabakışlı Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Look-through (Ara-bakış) karıştırmada SDR platformunun hızlı TX/RX anahtarlama yeteneğinden faydalanılacaktır. Sistem örneğin %90 oranında Karıştırma (TX), %10 oranında Dinleme (RX) zaman dilimlerine ayrılacaktır (Mili/Mikro-saniye seviyesinde anahtarlama tahsisleri). Dinleme periyodunda hedef sinyalin hala yayında olup olmadığı anlık FFT/enerji tespiti ile yoklanacaktır. Yayını kesen hedefler için karıştırma otomatik durdurularak spektrum hijyeni ve güç tasarrufu sağlanacak, frekans atlayan hedefler varsa yeni kanala hızlıca yönelme yapılacaktır.

**20. Elektronik Taarruz Sistemi’nde “Analog Telsiz Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Analog telsiz ve haberleşme sistemlerine yönelik asimetrik taarruz için, önceden hazırlanmış veya anlık sentezlenmiş yanıltıcı ses örnekleri, hedef kanalın spesifik modülasyonuyla (çoğunlukla NBFM/AM) modüle edilecektir. Operasyonel kanala, gerçek hedeften "daha güçlü" (Power Capture / Capture Effect) bir sinyal sızdırması yapılarak düşman haberleşme ağına sahte rapor, ton veya parazitli anons sokma şeklinde aldatma koşturulacaktır.

**21. Elektronik Taarruz Sistemi’nde “GNSS Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
GPS (L1, 1575.42 MHz) spektrumunda, SDR üzerinden GPS uydu efemeris(yörünge) verileri dinamik bir şekilde yeniden sentezlenecektir (Spoofing). Böylece hedef GNSS alıcısının kilitlendiği asıl uydu sinyalleri üzerine, daha güçlü fakat yanlış zaman (Timing Spoofing) veya yanlış koordinat (Position Spoofing) taşıyan sentetik PRN kodları ve navigasyon mesajları gönderilecek, hedefin rotasından çıkması veya senkronizasyon kaybetmesi sağlanacaktır.

**22. Elektronik Taarruz Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
Elektronik Taarruz (ET) alt sistemimiz, konvansiyonel karıştırma yerine 'Bilişsel Elektronik Harp' (Cognitive EW) prensilerini temel alan bir karar mekanizmasına sahiptir:
1.  **Akıllı Karıştırma Stratejisi (RL):** Hedef telsizin frekans atlama (Frequency Hopping) paternini veya dinamik güç kontrol mekanizmasını çözmek için 'Deep Reinforcement Learning' (PPO/DQN) tabanlı ajanlar kullanılacaktır. Ajan; spektrumu gözlemleyerek (State), hangi frekansa ne kadar güçle (Action) müdahale edeceğine karar verecek ve 'Look-through' periyodundaki başarı oranına göre (Reward) kendini optimize edecektir.
2.  **Dinamik Dalga Şekli Optimizasyonu:** Hedefin hata düzeltme (FEC) veya spektrum yayma tekniklerini etkisiz bırakacak en verimli karıştırma dalga şeklini (Waveform Optimization) üretmek için Genetik Algoritmalar ve Sinir Ağları hibrit olarak kullanılacaktır.
3.  **Adaptif Karar Destek:** Hedefin 'anti-jamming' yeteneklerini analiz ederek, hedefi istenen frekans bölgesine 'steering' (yönlendiren) proaktif aldatma senaryoları yapay zeka tarafından yönetilecektir.
Bu yaklaşım, kısıtlı RF gücü ile maksimum spektral etkinlik (Smart Jamming) sağlayacaktır.

**23. Yarışmaya katılacak olan Elektronik Taarruz Alt Sistemi’nin SwaP bilgilerini belirtiniz.**
- **Boyutlar:** ET anten yüksekliği 100 cm'dir. Sistem toplam yüksekliği 220 cm'yi (120 cm tripod + 100 cm ET) aşmamaktadır.
- **Ağırlık:** Ünite bazlı ağırlık < 10 kg'dır. Tüm bileşenler dahil toplam sistem ağırlığı < 20 kg'dır.
- **Güç:** 4 adet PA ve soğutma fanları dahil toplam güç tüketimi < 150 Watt öngörülmektedir.
- **Koruma:** TA antenleri ve PA birimleri aktif fanlı metal kafes haznede muhafaza edilmektedir.
