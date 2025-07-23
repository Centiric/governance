# Centiric Mimarisi ve Veri Akışı

Bu doküman, Centiric platformunun teknik mimarisini, servislerin sorumluluklarını ve aralarındaki veri akışını detaylı bir şekilde tanımlar.

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
| 🛡️ **`signal`** | SIP/RTP Sinyal Kalkanı | `Rust` | • `5060` UDP portunu dinlemek.<br>• Gelen SIP mesajlarını ayrıştırmak.<br>• **Gelen istekler için benzersiz bir `TraceID` oluşturmak.**<br>• Gelen `Via` ve `Record-Route` başlıklarını standartlara uygun işlemek.<br>• `core`'dan gelen kararlara göre SIP cevapları (1xx, 2xx) oluşturmak. |
| 🧠 **`core`** | Merkezi Motor | `Go` | • Servisler arası iş mantığını yönetmek.<br>• **Diğer servisler için bir "Servis Rehberi" (Service Registry) görevi görmek.**<br>• `signal`'dan gelen gRPC isteklerine göre çağrı yönlendirme kararları vermek.<br>• **Arama detay kayıtlarını (CDR) oluşturmak ve veritabanına yazmak.**<br>• `media` servisine medya oturumlarını başlatma/durdurma komutları vermek. |
| 🎙️ **`media`** | Ses İşleme | **Prototip: `Python`**<br>**Üretim: `Rust`/`C++`** | • **`10000-20000` UDP port aralığından dinamik olarak boş bir port seçmek.**<br>• Seçilen portu `core`'a bildirmek.<br>• Gelen RTP (ses) paketlerini almak ve işlemek.<br>• Ses kaydı ve codec dönüştürme (transcoding) yapmak.<br>• Ses akışının bir kopyasını `ai` servisine göndermek. |
| 🤖 **`ai`** | Yapay Zeka Analitiği | `Python` | • `media`'dan gelen sesi gerçek zamanlı olarak metne çevirmek (STT).<br>• Analiz sonuçlarını yapılandırılmış veri olarak `core`'a geri göndermek. |
| ... | *Diğer servisler...* | ... | ... |

---
## 3. Uçtan Uca Veri Akışı ve İzlenebilirlik

Bir çağrının yaşam döngüsü boyunca, `signal` tarafından oluşturulan tek bir **`TraceID`**, tüm servislerdeki loglara ve gRPC isteklerine eklenir. Bu, çağrının tüm yolculuğunu takip etmemizi sağlar.

| Adım | Servis | Eylem | Detay |
| :--- | :--- | :--- | :--- |
| 1 | **`signal`** | `INVITE` Alındı | Gelen SIP isteği için yeni bir `TraceID` (örn: `abc-123`) oluşturulur. |
| 2 | **`signal`** → **`core`** | gRPC: `RouteCall` | `TraceID: abc-123` gRPC metadata'sı ile gönderilir. `core` logları bu ID'yi içerir. |
| 3 | **`core`** → **`media`** | gRPC: `AllocatePort` | `TraceID: abc-123` ile `media`'dan boş bir port istenir. |
| 4 | **`media`** | Port Atama | `10000-20000` aralığından boş bir port (örn: `15012`) seçilir ve bu portu dinlemeye başlar. `media` logları bu ID'yi içerir. |
| 5 | **`media`** → **`core`** | gRPC Cevabı | Atanan port (`15012`) `TraceID` ile birlikte `core`'a bildirilir. |
| 6 | **`core`** → **`signal`** | gRPC Cevabı | `core`, `signal`'a çağrının kabul edildiğini ve medya portunun `15012` olduğunu bildirir. |
| 7 | **`signal`** | `200 OK` Gönderimi | `signal`, arayana gönderdiği SIP cevabının SDP kısmına medya portunu (`15012`) ve kendi IP adresini yazar. |
| 8 | **Operatör** → **`media`** | RTP Akışı | Arayan taraf, ses paketlerini doğrudan `media` servisinin dinlediği `15012` portuna göndermeye başlar. |
