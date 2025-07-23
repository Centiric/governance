# Güvenlik Prensipleri

Centiric platformunun her katmanı, belirli tehdit vektörlerine karşı tasarlanmış güvenlik önlemleri içerir.

### Katman Bazlı Güvenlik Önlemleri

```mermaid
graph TD
    subgraph "Dış Dünya Tehditleri"
        A[SIP Flood / Malformed Packets]
        B[XSS / CSRF Saldırıları]
        C[SQL Injection / Auth Bypass]
    end

    subgraph "Güvenlik Duvarlarımız"
        subgraph "🛡️ Kenar Katmanı"
            D["<b>signal:</b><br>- Rate Limiting<br>- SIP Mesaj Doğrulama"]
            E["<b>console:</b><br>- HTTP Güvenlik Başlıkları<br>- CSRF Tokenları"]
            F["<b>bridge:</b><br>- API Yetkilendirme (OAuth2)<br>- Gelen Veri Temizleme (Sanitization)"]
        end
        subgraph "🧠 Çekirdek & Medya"
            G["<b>core / media:</b><br>- İç Ağda İletişim (mTLS)<br>- Minimum Yetki Prensibi"]
        end
    end
    
    A --> D
    B --> E
    C --> F
```

| Katman | Servis | Birincil Tehdit | Önlem |
|:---|:---|:---|:---|
| **Kenar** | `signal` | DDoS, SIP Flood, Geçersiz Paketler | **Rate Limiting**, SIP Başlık/Gövde Doğrulaması |
| | `bridge` | Yetkisiz API Erişimi, Enjeksiyon | **OAuth 2.0**, Gelen Veri Doğrulama ve Temizleme |
| | `console`| XSS, CSRF | **Content-Security-Policy**, Anti-CSRF Tokenları |
| **Çekirdek** | `core` | Yetkisiz İç Servis Erişimi | **mTLS ile servisler arası şifreleme**, RBAC (Rol Bazlı Erişim Kontrolü) |
| **Medya**| `media` | RTP Flood, Ses Manipülasyonu | **SRTP ile ses şifreleme**, Kaynak IP Doğrulaması |

### Fiziksel Güvenlik (`telecom` servisi)
- `telecom` servisini barındıran sunucular, kilitli ve erişimi kısıtlanmış sunucu odalarında bulunmalıdır.
- Fiziksel PSTN kartlarına yetkisiz erişim engellenmelidir.
