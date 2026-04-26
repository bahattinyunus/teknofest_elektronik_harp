# TEKNİK YETERLİLİK FORMU CEVAPLARI - TEKNOFEST ELEKTRONİK HARP YARIŞMASI 2026

**1. Yarışmaya katılacak olan Elektronik Harp (EH) Sistemi hangi alt sistemlerden oluşmaktadır?**
- [x] Elektronik Destek (ED) ve Elektronik Taarruz (ET)

**2. Yarışmaya katılacak olan EH Sistemi kaç adet Sistem’den oluşmaktadır?**
Sistem, coğrafi olarak dağıtık **2 ana üniteden** oluşmaktadır: Bir adet **Ana ED/ET Ünitesi** ve bir adet **Yavru ED/ET Ünitesi**. Bu yapı, hem Elektronik Destek (konum belirleme, TDOA vb.) hem de Elektronik Taarruz görevlerinin iki farklı noktadan koordineli yürütülmesini sağlar. Toplam sistem ağırlığı 20 kg'ın altında tutulacak şekilde yüksek dayanımlı polimer ve karbon fiber (tripod) malzemelerle optimize edilmiştir.

**3. Yarışmaya katılacak olan EH Sistemi hangi işlevleri yerine getirmektedir?**
**Elektronik Destek:**
- [x] Sinyal Tespiti (Energy Detection & CFAR)
- [x] Parametre Çıkarımı (PRI, PW, BW, Modulation ID)
- [x] Sinyal İzleme/Dinleme (Real-time Demodulation)
- [x] Yön Bulma (DF - MUSIC/Interferometry)
- [x] Konum Belirleme (AOA/TDOA Fusion)

**Elektronik Taarruz:**
- [x] Sürekli Karıştırma (Spot/Sweep/Barrage)
- [x] Ara-Bakışlı Karıştırma (Look-through Jamming)
- [x] Analog Telsiz Aldatma (Voice Spoofing)
- [x] GNSS Aldatma (Timing & Position Spoofing)
- [x] DRFM Aldatma (RGPO/VGPO/Coherent False Targets)

**4. Yarışmaya katılacak olan EH Sistemini tanıtınız.**
**Mergen-AI OMEGA**, modüler, yapay zeka destekli ve Software Defined Radio (SDR) tabanlı entegre bir Bilişsel Elektronik Harp (Cognitive EW) platformudur. Altyapı olarak Ettus USRP serisi SDR platformları kullanılacaktır. Hazır kullanıcı arayüzleri kesinlikle kullanılmamakta; Python/C++ tabanlı özgün DSP blokları ve kendi geliştirdiğimiz **Mergen-OS** komuta kontrol yazılımı üzerinden yönetilmektedir. Sistem, spektrumu akıllı otonom algoritmalarla analiz edip hedefe dinamik reaksiyon (karıştırma/aldatma) verebilen kapalı çevrim (closed-loop) bir otonomiye sahiptir.

**5. Sistem mimarinizi açıklayınız.**
Sistem mimarimiz, **Ana Ünite** ve **Yavru Ünite** olmak üzere iki temel ayaktan oluşur. Ana ünite, dairesel dizilmiş **12 adet Vivaldi antenden** oluşan bir ED dizisine ve hemen üzerinde dikey polarizasyonlu bir **Log-Periyodik ET antenine** sahiptir. Yavru ünite ise operasyonel senaryoya göre benzer bir dairesel dize barındırır. Her iki ünite de 120 cm boyundaki askeri standartta tripodlar üzerine konumlandırılmış, birincil kontrol birimi olarak **Edge AI (Raspberry Pi 5 / Jetson Orin)** ve yüksek bant genişlikli SDR platformları ile donatılmıştır. I/Q verileri bu iki ünite arasında düşük gecikmeli link ile senkronize edilerek merkezi işleme biriminde füzyonlanır.

**6. Sistemin entegre olacağı platformu açıklayınız.**
- [x] Karada, Taşınabilir (kullanım sırasında sabit)
**Kullanım Şekli:**
Sistem, operasyon bölgesine tekerlekli nakliye çantalarıyla intikal ettirilebilen "Manga/Tim Seviyesi Taşınabilir" bir yapıdadır. Kurulum aşamasında tripod veya taktiksel kule benzeri yapılar üzerine anten dizileri yerleştirilerek, kullanım sırasında sabit (fixed-site) kalacak biçimde işletilecektir. 

**7. Elektronik Destek Sisteminin “Çalışma Frekans Bandı” nedir?**
70 MHz - 6000 MHz (Yüksek kararlılıklı TCXO/GPSDO saat kaynağı ile).

**8. Elektronik Destek Sistemi kaç kanaldan oluşacaktır? Almaç anlık bant genişliği için ne öngörülmektedir?**
- DF için Kanal Sayısı: 12 kanal (Ana ünite 360° dairesel dizilim için koherent anahtarlamalı)
- DF için Almaç Anlık Bant Genişliği: 160 MHz (USRP B210 limitleri dahilinde optimize edilmiştir)
- Monitör/İzleme için Kanal Sayısı: 2 kanal (Ana ve Yavru üniteler için bağımsız izleme)
- Monitör/İzleme için Anlık Bant Genişliği: 160 MHz

**9. Elektronik Destek Sistemi’nde “Sinyal Tespiti” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Geniş bantlı spektrum tarama yöntemiyle elde edilen I/Q verileri üzerinden gerçek zamanlı FFT işlemleri uygulanacak ve oluşturulan güç spektral yoğunluk (PSD) verisi, **Adaptive CFAR (Constant False Alarm Rate)** ve Enerji Tespiti algoritmaları ile işlenecektir. Arka planda değişen gürültü eşikleri dinamik hesaplanıp, gürültü zemininin üzerine çıkan dar ve geniş bantlı muhabere sinyalleri otomatik olarak tespit edilerek "Threat Candidates" olarak etiketlenecektir.

**10. Elektronik Destek Sistemi’nde “Parametre Çıkarımı” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Tespit edilen sinyalin I/Q örnekleri üzerinden Digital Down Conversion (DDC) uygulanarak sinyal ana banda indirilecektir. Analitik sinyal (Hilbert) üzerinden; Merkez Frekansı, Bant Genişliği, Sinyal/Gürültü Oranı (SNR) gibi temel parametreler elde edilecektir. Modülasyon Tipi (AM, FM, ASK, FSK, PSK, QAM varyantları) ve Sembol Hızı (Baud Rate) çıkarımı ise otonom yapay zeka (Deep Learning - CNN) algoritmalarımız ile IQ verisinden ve spektrogram özelliklerinden doğrudan saptanacaktır.

**11. Elektronik Destek Sistemi’nde “Sinyal İzleme/Dinleme” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Hedef sinyale uygulanan DDC işleminin ardından, saptanan modülasyon tipine (AM, FM veya sayısal modülasyonlar) uygun demodülatör bloklarımız (Costas loop, PLL vb. ile kilitlenerek) devreye girecektir. Analog ses içerikli telsiz sinyalleri demodüle edilerek doğrudan operatörün ses arayüzüne veya kayıt ortamına (WAV) aktarılacaktır. Sayısal sinyaller ise bit katmanına kadar çıkarılarak analiz için veritabanına (Pulse Descriptor Word - PDW) kaydedilecektir.

**12. Elektronik Destek Sistemi’nde “Yön Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Ana ünitede bulunan dairesel dizilimli **12 adet Vivaldi anten** üzerinden **MUSIC (Multiple Signal Classification)** ve Correlative Interferometry algoritmaları koşturulacaktır. Antenlere gelen sinyallerin uzamsal faz farkları ve genlik oranları işlenerek yüksek çözünürlüklü yön (AOA) kestirimi yapılacaktır. Vivaldi antenlerin geniş bant karakteristiği sayesinde RMS yön doğruluğu hedefimiz < 3 derecedir.

**13. Elektronik Destek Sistemi’nde “Konum Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Konum bulma, coğrafi olarak ayrılmış **Ana ve Yavru sistem (2 istasyon)** üzerinden gerçekleştirilecektir. Her iki ünite de hedef sinyali GPS/PPS zaman damgalarıyla etiketleyecektir. İki noktadan alınan veriler üzerinden hem Varış Zamanı Farkı (TDOA) hem de AOA (Yön) verileri füzyonlanarak hedefin koordinatları harita üzerinde kestirilecektir.

**14. Elektronik Destek Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
Sistemimizde, sinyal yoğunluğunun yüksek olduğu harp sahası koşullarını yönetmek için çok katmanlı bir Yapay Zeka mimarisi kullanılacaktır:
1.  **Otomatik Modülasyon Sınıflandırma (AMC):** Ham I/Q verileri üzerinden derin öznitelik çıkaran ResNet tabanlı evrişimli ağlar (CNN) ile düşük SNR (-5dB ve altı) değerlerinde bile %90+ doğrulukla modülasyon teşhisi yapılacaktır.
2.  **Sinyal Ayrıştırma (De-interleaving):** Karmaşık darbe katarı içerisinden farklı kaynaklara ait sinyalleri ayırmak için unsupervised clustering (DBSCAN) algoritmaları kullanılacaktır.
3.  **Anomali Tespiti:** Spektrumun normal davranışını öğrenen 'Autoencoder' yapıları ile siber-fiziksel saldırılar veya yeni nesil 'Low Probability of Intercept' (LPI) sinyalleri anlık olarak tespit edilecektir.

**15. Yarışmaya katılacak olan Elektronik Destek Alt Sistemi’nin SwaP (Size, Weight and Power) bilgilerini belirtiniz.**
- **Boyutlar:** Ana ED ünitesi 12'li Vivaldi dairesel dizesine sahiptir (Çap: 45 cm). Yerden yükseklik tripod dahil 120 cm'dir.
- **Ağırlık:** Ünite başına < 10 kg, toplam taşınabilir sistem < 20 kg.
- **Güç:** Sistemin toplam güç tüketimi (ET dahil) < 150 Watt (Lityum-İyon batarya blokları ile 4+ saat operasyon).

**16. Elektronik Taarruz Sisteminin Çalışma Frekans Bandı nedir?**
70 MHz - 6000 MHz (Yüksek kazançlı Log-Periyodik anten dizileri ile).

**17. Elektronik Taarruz Sistemi kaç Alt Banttan oluşacaktır? Bant başına RF çıkışı gücü için ne öngörülmektedir?**
- Karıştırma/Aldatma için Alt Bant Sayısı: **4 farklı RF kanalı** (Dinamik anahtarlamalı).
- Bant Başına RF Çıkış Gücü: Her iki ünitede yer alan **Log-Periyodik antenler** kullanılacaktır. Toplamda 4 adet geniş bantlı güç yükseltici (PA) üzerinden beslenen sistemde, antenlere aktarılan güç ve donanım beslemeleri dahil toplam tüketim 150W altında kalacak şekilde tasarım yapılmıştır.

**18. Elektronik Taarruz Sistemi’nde “Sürekli Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Sürekli karıştırma modunda sistem, DRFM ve DDS mantıklarını yazılımsal olarak simüle ederek çalışacaktır. Hedefe Spot (dar bant, yüksek yoğunluklu), Sweep (frekans aralığını dinamik süpürerek çoklu etki) ve Baraj Karıştırma (AWGN veya Comb karıştırma) teknikleri uzman operatör veya otonom motor tarafından uygulanabilecektir.

**19. Elektronik Taarruz Sistemi’nde “Arabakışlı Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
**Look-through (Ara-bakış)** karıştırmada SDR platformunun hızlı TX/RX geçiş yeteneğinden faydalanılacaktır. Sistem örneğin %90 oranında Karıştırma (TX), %10 oranında Dinleme (RX) zaman dilimlerine ayrılacaktır (Mikro-saniye seviyesinde anahtarlama). Dinleme periyodunda hedef sinyalin hala yayında olup olmadığı anlık FFT/enerji tespiti ile yoklanacaktır.

**20. Elektronik Taarruz Sistemi’nde “Analog Telsiz Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Analog telsiz sistemlerine yönelik asimetrik taarruz için, önceden hazırlanmış veya anlık sentezlenmiş yanıltıcı ses örnekleri, hedef kanalın modülasyonuyla (NBFM/AM) modüle edilecektir. Güç yakalama (Capture Effect) prensibiyle hedef alıcıya sızma yapılarak sahte anons veya parazitli sinyal iletimi gerçekleştirilecektir.

**21. Elektronik Taarruz Sistemi’nde “GNSS Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
GPS (L1/L2) spektrumunda, SDR üzerinden GPS uydu efemeris verileri dinamik bir şekilde yeniden sentezlenecektir (**Spoofing**). Böylece hedef GNSS alıcısının kilitlendiği asıl uydu sinyalleri üzerine, daha güçlü fakat yanlış zaman veya yanlış koordinat taşıyan sentetik PRN kodları gönderilerek hedefin rotasından çıkması sağlanacaktır.

**22. Elektronik Taarruz Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
Elektronik Taarruz (ET) alt sistemimiz, 'Bilişsel Elektronik Harp' (Cognitive EW) prensiplerini temel alır:
1.  **Akıllı Karıştırma Stratejisi (RL):** Hedef telsizin frekans atlama (Frequency Hopping) paternini çözmek için Reinforcement Learning tabanlı ajanlar kullanılacaktır. Ajan, hangi frekansa ne kadar güçle müdahale edeceğine karar vererek müdahale etkinliğini maksimize edecektir.
2.  **Dinamik Dalga Şekli Optimizasyonu:** Hedefin anti-jamming tekniklerini etkisiz bırakacak en verimli karıştırma dalga şeklini (Waveform Optimization) üretmek için genetik algoritmalar kullanılacaktır.

**23. Yarışmaya katılacak olan Elektronik Taarruz Alt Sistemi’nin SwaP bilgilerini belirtiniz.**
- **Güç:** 4 adet PA ve soğutma fanları dahil toplam güç tüketimi < 150 Watt öngörülmektedir.
- **Koruma:** TA antenleri ve PA birimleri aktif fanlı metal kafes haznede muhafaza edilmektedir.
