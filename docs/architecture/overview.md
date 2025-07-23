# Centiric Mimarisi ve Veri Akışı

Bu doküman, Centiric platformunun teknik mimarisini, servislerin sorumluluklarını ve aralarındaki veri akışlarını detaylı bir şekilde tanımlar.

---

## 1. Felsefe ve Genel Yaklaşım

Centiric, her biri tek bir sorumluluğa odaklanmış (Single Responsibility Principle) mikroservislerden oluşur. Mimarimiz, güvenlik, ölçeklenebilirlik ve bakım kolaylığı sağlamak üzere katmanlı bir yapıda tasarlanmıştır:

-   **Kenar Katmanı (Edge):** Dış dünyadan gelen "gürültülü" ve güvenilmeyen trafiği karşılayan, filtreleyen ve standartlaştıran "sınır muhafızlarıdır".
-   **Çekirdek Katman (Core):** Platformun "beyni"dir. Protokol karmaşıklığından arındırılmış, sadece saf iş mantığını çalıştırır.
-   **Medya & AI Katmanı:** Gerçek zamanlı ses/video akışlarını işleyen ve yapay zeka ile zenginleştiren uzman servislerdir.

---

## 2. Servislerin Detaylı Tanımı

| Repo / Servis | Sorumluluk | Teknoloji | Birincil Görevleri |
| :--- | :--- | :--- | :--- |
| 🛡️ **signal** | SIP/RTP Sinyal Kalkanı | `Rust` | • `5060` UDP portunu dinlemek.<br>• Gelen SIP mesajlarını (INVITE, BYE vb.) ayrıştırmak (parse).<br>• `core`'dan gelen kararlara göre SIP cevapları (200 OK, 404 vb.) oluşturmak.<br>• Medya oturum bilgilerini (SDP) `media` servisine iletmek. |
| 🧠 **`core`** | Merkezi Motor | `Go` | • Servisler arası tüm iş mantığını yönetmek.<br>• `signal`'dan gelen gRPC isteklerine göre çağrı yönlendirme kararları vermek.<br>• `media` servisine medya oturumlarını başlatma/durdurma komutları vermek.<br>• Veritabanı işlemlerini, kullanıcı yetkilendirmeyi ve faturalandırma mantığını yürütmek. |
| 🎙️ **`media`** | Ses İşleme | `Python/C`| • Belirli bir UDP port aralığını (örn: 10000-20000) dinleyerek RTP (ses) paketlerini almak.<br>• Ses kaydı yapmak, codec'ler arası dönüşüm (transcoding) sağlamak.<br>• WebRTC istemcileri için köprü görevi görmek.<br>• Ses akışının bir kopyasını `ai` servisine göndermek. |
| 🤖 **`ai`** | Yapay Zeka Analitiği | `Python` | • `media`'dan gelen sesi gerçek zamanlı olarak metne çevirmek (Speech-to-Text).<br>• Metin üzerinde duygu analizi, anahtar kelime tespiti yapmak.<br>• Analiz sonuçlarını yapılandırılmış veri olarak `core`'a geri göndermek. |
| ☎️ **`telecom`** | PSTN Gateway | `C++` | • Fiziksel telefon hatlarından (FXO/ISDN) gelen analog/dijital sinyalleri yakalamak.<br>• Bu sinyalleri SIP/RTP paketlerine çevirerek `signal` ve `media` servislerine iletmek. |
| 🔌 **`bridge`** | API Gateway | `Node.js` | • Harici sistemler (CRM, ERP) için güvenli bir REST API uç noktası sağlamak.<br>• Gelen API isteklerini yetkilendirip, gRPC formatına çevirerek `core`'a iletmek. |
| 💻 **`console`** | Yönetim Arayüzü | `React+TS`| • Yöneticilerin sistemi izleyebileceği, yapılandırabileceği web arayüzünü sunmak.<br>• `core` ile WebSocket üzerinden anlık veri alışverişi yapmak. |

---

## 3. Uçtan Uca Veri Akışı: Gelen Bir PSTN Çağrısı

Bu senaryo, sistemin tüm katmanlarının nasıl bir uyum içinde çalıştığını gösterir.

| Adım | Başlangıç Noktası | Eylem | Protokol / Port | Bitiş Noktası | Açıklama |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **PSTN Ağı** | Fiziksel arama sinyali gönderir. | FXO/ISDN | **`telecom`** | Donanım, hattın çaldığını algılar. |
| **2** | **`telecom`** | Sinyali SIP `INVITE` mesajına çevirir. | SIP / UDP:5060 | **`signal`** | Eski dünya sinyali, modern IP sinyaline dönüştürülür. |
| **3** | **`signal`** | `INVITE`'ı ayrıştırır ve gRPC isteği oluşturur. | gRPC / TCP:50051 | **`core`** | **Sınır Muhafızı**, temizlenmiş isteği **Beyin**'e sorar. |
| **4** | **`core`** | İş mantığını çalıştırır, yönlendirme kararı verir. | gRPC Cevabı | **`signal`** | Beyin, "Aramayı kabul et" kararını Sınır Muhafızı'na bildirir. |
| **5** | **`core`** | Medya oturumu açılması için komut gönderir. | gRPC / TCP | **`media`** | Beyin, **Ses Uzmanı**'na bir kanal hazırlamasını söyler. |
| **6** | **`media`** | Boş bir RTP portu (örn: 12010) ayarlar. | Dahili | **`core`** | Ses Uzmanı, "Hazırım, sesi 12010'a bekliyorum" der. |
| **7**| **`core`** | Medya bilgisini (SDP) `signal`'a iletir. | gRPC | **`signal`** | Beyin, sesin nereye gönderileceği bilgisini Sınır Muhafızı'na verir. |
| **8**| **`signal`** | Arayana `200 OK` cevabını SDP ile gönderir. | SIP / UDP:5060 | **PSTN Ağı** | Sınır Muhafızı, arayana "Bağlantı kuruldu, sesi 12010'a gönder" der. |
| **9**| **`telecom`** | Gelen ses paketlerini (RTP) iletir. | RTP / UDP:12010| **`media`** | Konuşma başlar. Gerçek ses akışı doğrudan Ses Uzmanı'na gider. |
| **10**| **`media`** | Ses akışının bir kopyasını analiz için gönderir.| gRPC (stream) | **`ai`** | Ses Uzmanı, bir kopyayı **Yapay Zeka**'ya dinletir. |
| **11**| **`ai`** | Sesi metne çevirir ve analiz sonucunu gönderir.| gRPC | **`core`** | Yapay Zeka, "Konuşmada 'sipariş' kelimesi geçti" gibi bilgileri Beyin'e raporlar. |

---

Bu yazılı doküman, bir diyagramın sunabileceğinden çok daha fazla detay ve netlik içerir. Her bir servisin sorumluluğu, kullandığı teknoloji ve diğer servislerle olan etkileşimi açıktır. Bu, projenizin "anayasası" olarak kullanılabilir ve herkesin aynı vizyon doğrultusunda çalışmasını sağlar.
