# TEKNOFEST ELEKTRONİK HARP YARIŞMASI - TEKNİK YETERLİLİK FORMU CEVAPLARI

**1. Yarışmaya katılacak olan Elektronik Harp (EH) Sistemi hangi alt sistemlerden oluşmaktadır?**
- [x] Elektronik Destek ve Elektronik Taarruz

**2. Yarışmaya katılacak olan EH Sistemi kaç adet Sistem’den oluşmaktadır?**
Sistem, 1 adet yüksek işlem kapasiteli dizüstü bilgisayar (C&C) ve 1 adet Full-Duplex SDR (USRP B210) içeren tek bir ana istasyondan oluşmaktadır. Yön bulma dâhil ED ve taktik ET görevleri, aynı SDR üstünden koherent 2x2 MIMO ve zaman paylaşımlı otonomiyle icra edilmektedir. Toplam sistem adedi: 1.

**3. Yarışmaya katılacak olan EH Sistemi hangi işlevleri yerine getirmektedir?**
**Elektronik Destek**
- [x] Sinyal Tespiti
- [x] Parametre Çıkarımı
- [x] Sinyal İzleme/Dinleme
- [x] Yön Bulma (DF)
- [ ] Konum Belirleme

**Elektronik Taarruz**
- [x] Sürekli Karıştırma
- [x] Ara-Bakışlı Karıştırma
- [x] Analog Telsiz Aldatma
- [x] GNSS Aldatma

**4. Yarışmaya katılacak olan EH Sistemini tanıtınız.**
Sistemimiz, Ettus USRP B210 SDR donanımı ve yüksek işlem gücüne sahip dizüstü bilgisayar temelinde geliştirilmiş, kütüphane bağımsız Bilişsel Elektronik Harp (CEW) mimarisidir. Sinyal işleme, otonom karar ve YZ çıkarımları yazılımla sağlanır, hazır arayüz kullanılmaz. RF dijitalleştirme işlemi SDR tarafından yapılırken; yön bulma, tehdit analizi, karıştırma (jamming) parametresi üretme ve anlık reaksiyon mekanizmaları, geliştirdiğimiz derin öğrenme algoritmalarıyla tam otonom yönetilmektedir.

**5. Sistem mimarinizi açıklayınız.**
- **Açıklama:** Geliştirilen mimaride anten dizisinden alınan analog RF sinyaller, filtre ve LNA katmanından geçtikten sonra USRP B210 SDR ile sayısal IQ verisine dönüştürülür. IQ verileri USB 3.0/Type-C üzerinden dizüstü bilgisayardaki ana kontrol birimine aktarılır. Bilgisayar üzerinde koşan ED Modülü (CNN tabanlı tespit) ve ET Modülü (DQN tabanlı karar) veriyi işler. Karar verilen karıştırma/aldatma sinyali tekrar SDR üzerinden RF'e çevrilip hedefe yönlendirilir. Özgün arayüz bulunur.
- **Not:** *Detaylı Sistem Blok Şeması başvuru ekranında görsel olarak (örn: sistem_mimarisi.png) sisteme yüklenecektir.*

**6. Sistemin entegre olacağı platformu açıklayınız.**
- [x] Karada, Taşınabilir (kullanım sırasında sabit)
- **Kullanım Şekli:** Sistem donanımları, zorlu taktik saha şartlarına dayanıklı, taşınabilir bir mobil çanta formunda operasyon alanına intikal ettirilir. Görev bölgesinde SDR ve anten dizilimi hızla tripoda kurularak dizüstü bilgisayara bağlanıp sabitlenir. Cihaz gücünü esnek yapıda sunar; varsa AC şebekeden, yoksa askeri standartlardaki DC güç istasyonları ile lityum hücrelerinden sağlayarak, sahada dış müdahaleden bağımsız biçimde, çok uzun saatler boyunca aralıksız ve tam otonom taarruz görevi icra eder.

**7. Elektronik Destek Sisteminin “Çalışma Frekans Bandı” nedir?**
70 - 6000 (Açıklama: 70 MHz ile 6000 MHz arası geniş bant aralığı)

**8. Elektronik Destek Sistemi kaç kanaldan oluşacaktır? Almaç anlık bant genişliği için ne öngörülmektedir?**
- DF için Kanal Sayısı: 2 (Faz uyumlu coherent RX)
- DF için Almaç Anlık Bant Genişliği: 56
- Monitör/İzleme için Kanal Sayısı: 2
- Monitör/İzleme için Anlık Bant Genişliği: 56

**9. Elektronik Destek Sistemi’nde “Sinyal Tespiti” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Taktik sahada SDR’ın taradığı periyotlardaki geniş bantlı RF enerjisi, sistemde Hızlı Fourier Dönüşümü (FFT) ile Güç Spektral Yoğunluğu (PSD) verisine dönüştürülür. Spektrum üzerinde CFAR (Constant False Alarm Rate) tabanlı adaptif enerji eşikleme algoritmaları yüksek hızda koşturulur. Dinamik termal zemin gürültüsünü aşarak referansın üstüne çıkan anomali pikleri DSP ile otonom tespit edilir ve varlığı izole edilerek anında doğrulanan sinyaller, kritik parametre çıkarım modülüne beslenir.

**10. Elektronik Destek Sistemi’nde “Parametre Çıkarımı” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Eşiği aşan frekans bölgelerinden izole edilmiş yüksek çözünürlüklü dijital IQ verileri, sistemimizde ön işleme adımlarından geçerek temel parametreleri sayısal olarak ayıklanır. Genlik, faz ve zaman analiziyle merkez frekansı, anlık/efektif bant genişliği, Sinyal-Gürültü Oranı (SNR), Darbe Tekrarlama Frekansı (PRF) ve sinyal süresi (Pulse Width) gibi metrikler yüksek kesinlikle ölçülür. Daha karmaşık bir teşhis gerektiren örüntüler; sinyalin zaman-frekans tabanlı spektrogram matrisine dönüştürülmesiyle Evrişimli Sinir Ağları (CNN) modelimize aktarılır. Bilişsel yapay zekâmız, bu spektrogram özellikleri üzerinden hedef sinyalin modülasyon tipini (AM, FM, FSK, PSK türevleri) otonom sınıflandırarak radarın kimliğini ve işlevini deşifre eder.

**11. Elektronik Destek Sistemi’nde “Sinyal İzleme/Dinleme” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Geniş spektrum tespitleriyle algılanan yapılandırılmamış ardışık analog telsiz veya PMR/DMR tarzı sayısal ses radyo sinyalleri, SDR kanallarıyla hedef dar banda kilitlenerek eşzamanlı kaydedilir. Yazılımımızdaki dijital filtreler ve Python/GNU Radio DSP blokları aracılığıyla baseband IQ verileri doğrudan AM/FM gibi analog modlar için ses çerçevelerine demodüle edilir. Sayısal veri paketleri de temel modülasyon bazında bit seviyesine indirilerek komuta ekranından otonom sesle izleme sağlanır.

**12. Elektronik Destek Sistemi’nde “Yön Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Yön kestiriminde, SDR donanımının çift kanallı koherent (faz uyumlu) almaç yapısı kullanılarak gelişmiş Faz Karşılaştırma (Phase Interferometry / Pseudo-Doppler) metodu icra edilir. Eşzamanlı ulaşan RF radyo dalgaları arasındaki faz farkları (ΔΦ) ve yönsel zaman gecikmeleri sistemce mikro saniye çözünürlüğüyle anlık olarak hesaplanır. Geliş açısı (AoA) denklemleri çözülerek, tehdit vericisinin yön vektörü, sahada mükemmel konumlandırmayla 5 derecenin altında üstün RMS doğruluğuyla belirlenir.

**13. Elektronik Destek Sistemi’nde “Konum Bulma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Sahada tekli konfigürasyon bulunduğundan Yön Bulma (AoA) vektörleri zaman/mekan hareketleriyle çaprazlanarak yaklaşık konum kestirilir. Dinamik yansıma (multipath) ve sönümleme metrikleri modele dahil edilmiştir. Taktik sahada kesin harita koordinatları tespit edilemese dahi; hedef menzilindeki sinyal şiddeti (RSSI), atmosferik yol kayıpları ve ısı haritası algoritmaları yardımıyla yakınlık bölgesi tahmini çıkarılır. Bu otonom haritalama, dost unsurlar bölgesine güçlü hayatta kalma ve vizyon katar.

**14. Elektronik Destek Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
Sistemimizde "Bilişsel SIGINT" konseptiyle kütüphanesiz tespitte DRL ve Derin Öğrenme vardır. Düşmanın sıfırıncı gün sinyallerini algıladığında klasik parametre eşikleme yetersizleşir. IQ verilerinden türettiğimiz 2D Yüksek Çözünürlüklü Spektrogram matrislerini, önceden terabaytlarca veriyle eğitilmiş Evrişimli Sinir Ağlarına (ResNet tabanlı CNN) besliyoruz. Model, yeni nesil radarların frekans atlamalarını veya PMR modülasyon formlarını mili-saniyeler içinde %90+ üstün doğrulukla sınıflandırır.

**15. Yarışmaya katılacak olan Elektronik Destek Alt Sistemi’nin SwaP (Size, Weight and Power) bilgilerini belirtiniz.**
Boyutlar (E x B x Y): LPT C&C Bilgisayarı (~360 x 250 x 20 mm) ile SDR donanımı (150 x 120 x 40 mm) modülerdir.
Ağırlık: Kurulum aparatları ve anten dizisi kapsülünde toplam operasyon yükü sadece 3.5 kilogramdır.
Güç (ED Aktif): Sinyal izleme ve CNN analiz süreçlerinde LPT ve SDR'ın birleşik AC/DC güç sarfiyatı maksimum 70W seviyesindedir. Dahili lityum batarya grubuyla 4 saate varan otonom kesintisiz görev icra eder; ek olarak askeri tip 24V DC/AC saha güç istasyonlarıyla tam uyumluluk sunar.

**16. Elektronik Taarruz Sisteminin Çalışma Frekans Bandı nedir?**
70 - 6000 (Açıklama: SDR'nin yetenekleri doğrultusunda geniş spektrum, özellikle ISM, GNSS ve Telsiz bantları)

**17. Elektronik Taarruz Sistemi kaç Alt Banttan oluşacaktır? Bant başına RF çıkışı gücü için ne öngörülmektedir?**
- Karıştırma için Alt Bant Sayısı: 2 (Ara-Bakışlı veya Eşzamanlı atlamalı karıştırma için SDR 2 TX kanalı)
- Karıştırma için Bant Başına RF Çıkış Gücü: 
SDR alt yapısı RX/TX izolasyonuyla sinyali 50-100 mW olarak çıkartır. Ancak otonom taktik operasyonda bu güç doğrudan Hedef frekansa göre optimize edilen ve harici beslenen Genişbant Güç Yükselteçleri (RF PA) bloğuna girer. Anten sistemimizde, RF çıkışında bant başına asgari 1 Watt - 2 Watt sürekli güç (CW) sağlanacaktır. Yönsüz anten yerine hedefe doğrudan enerjiyi odaklayan Log-Periyodik veya 7-12 dBi'lik Yagi Antenler kurularak, efektif ışıma gücü (ERP) taarruzu maksimize edecek seviyededir.
- Aldatma için Alt Bant Sayısı: 1 (L1 bandajlı / Hedef bantlı)
- Aldatma için Bant Başına RF Çıkış Gücü: 
Elektronik Aldatma (Spoofing) görevlerinde yüksek RF gücünden ziyade sinyal bütünlüğü asıldır. Aldatma, radyo dalgalarında sızıntıyı ve sivil enterferansı mutlak önlemek adına PA yükselteci bypass edilerek milivatt (mW) ölçeğinde minimal yapılır. Cihaz direkt SDR çıkışından 50 mW'tan az gücü GNSS sinyaline iletir. Yönlü patch veya ufuk anteni (3-5 dBi) vasıtasıyla spesifik hedef uydu alıcısına doğru sızdırılır. Böylelikle hedefin algılama limitlerinde fısıldayarak şüphe uyandırmadan kandırır.

**18. Elektronik Taarruz Sistemi’nde “Sürekli Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Dijital SDR altyazısıyla Sürekli Karıştırma, aralıksız yüksek enerjili RF enterferansı (DRFM tarzı) basımıdır. Tekil aktif düşman ağlarına uyguladığımız Nokta (Spot) Karıştırmayla, 1 MHz altı dar bantları doğrudan kilitleyerek Susturulması sağlanır. Alternatif olarak, SDR donanımımızın 50 MHz üstündeki devasa anlık bant genişliği yeteneğiyle Baraj (Barrage) Karıştırma atılır; böylece frekans atlayan hedeflere ve salkım radyolara eşzamanlı engelleme çökertmesi sağlanarak tam saha EH etkisi kurulur.

**19. Elektronik Taarruz Sistemi’nde “Arabakışlı Karıştırma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Taktik sağırlaşmayı önlemek adına Zaman-Bölmeli Çift Yönleme (TDD) ile tasarlanmış yarı-otonom Ara-Bakışlı (Look-Through) yöntem işletilir. Karıştırma esnasında SDR, donanımsal körlüğü yenmek için hedeflenen 56 MHz spektruma (10-15 ms'lik) nano-saniyelik dinleme pencereleri asar. Gelen sinyalin durumu tarandıktan hemen sonra mikrosaniye cinsi reaksiyonla donanım tekrar TX karıştırma fazına döner. Bu atik geçişler arayüzden yönetilir, düşman frekans zıplamaları anlık yakalanarak jammer adapte olur.

**20. Elektronik Taarruz Sistemi’nde “Analog Telsiz Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Düşman operasyonel komuta-kontrol ses ağına sinsice sızmayı amaçlar. Taktik yapay zekâ veya istihbarat arşiviyle önceden üretilmiş sentetik komut dosyaları (yanıltıcı ses ve mors), Python/DSP altyapımızla modülasyona (FM/AM) sokulur ve ham IQ paketine dönüştürülür. SDR ağ geçidinden geçirilerek düşman ağının zamanlama periyoduna tam senkronize eş-merkezli yüksek RF yayını olarak dinleyiciye çakılır. Tespit edilmiş açık kanal telsiz operatörleri bu metotla alıkonularak düşman iletişimi felç edilir.

**21. Elektronik Taarruz Sistemi’nde “GNSS Aldatma” görevinin nasıl yapılacağı hakkında bilgi veriniz.**
Yazılım tabanlı simülatör modelimiz üzerinden, GNSS L1 (1575.42 MHz) spesifikasyonlarında sahte efemeris ve almanak parametreleriyle "Spoofed" konum veya hız dijital verileri sentetik olarak yaratılır ve IQ stream oluşturulur. SDR altyapısından çok düşük yansıma (milliwatt) değerlerinde basılarak sivil hedef alıcıların GPS Takip Döngüleri (Tracking Loop) ele geçirilir. Sistem hedeflerine saniye saniye değişen sahte koordinat haritası çizerek onları yanlış taktik seyir noktalarına otonom sürükler.

**22. Elektronik Taarruz Sistemi’nde Yapay Zekâ kullanım hakkında bilgi veriniz.**
Sistem, kütüphane bağımsız Bilişsel Elektronik Taarruz (CEW) mimarisindedir. Bilinmeyen (sıfırıncı gün) sinyallerin IQ verilerinden spektral özellik çıkarımı ve tespiti CNN ile yapılır. Dinamik taktik sahada hedefe uygun karıştırma tekniği (modülasyon, güç, zamanlama) seçimi Derin Q-Ağı (DQN) ve Q-Learning algoritmalarıyla anlık optimize edilir. Bu derin pekiştirmeli (DRL) zekâ, klasik kütüphaneleri aşarak radarlara karşı eşzamanlı, tahminsiz ve otonom aktif taarruz yeteneği sunar.

**23. Yarışmaya katılacak olan Elektronik Taarruz Alt Sistemi’nin SwaP (Size, Weight and Power) bilgilerini belirtiniz.**
Platformumuzda ET (Taarruz) sistemi, ED analiz yapısıyla aynı koherent donanım şasisinde (LPT+SDR) yer alarak lojistik fayda sunar.
Boyut: LPT Bilgisayar (~360x250x20 mm) ve USRP SDR (~150x120x40 mm).
Ağırlık: Güç yükselteçleri dâhil mobil ağırlık yak. 3.5 kg.
Güç (ET Aktif): Normal dinlemede 60-70W çeken donanım, Taarruz anında SDR TX zincirinin ve RF Yükselteç (PA) devrelerinin pik yüklenmesiyle LPT dâhil tam 120-130W enerji sarfiyatına ulaşır. Uzun operasyon için destekli saha (AC/DC) ünitesi gerekir.
