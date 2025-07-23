# Centiric - Nihai Sistem Mimarisi

Bu doküman, Centiric platformunu oluşturan tüm servislerin mimari yapısını, sorumluluklarını ve aralarındaki veri akışını detaylandırmaktadır.

---

### **Mimari Diyagram**

Aşağıdaki diyagram, servislerin katmanlı yapısını ve aralarındaki temel iletişim akışlarını göstermektedir.

```mermaid
graph TD
    %% ===== STİL TANIMLARI =====
    classDef external fill:#f8f9fa,stroke:#6c757d,stroke-dasharray:5,5;
    classDef edge fill:#e7f5ff,stroke:#228be6;
    classDef core fill:#ebfbee,stroke:#40c057,stroke-width:2px;
    classDef media fill:#fff4e6,stroke:#fd7e14;
    classDef ai fill:#ffebee,stroke:#e53935;
    classDef console fill:#e3f2fd,stroke:#1e88e5;
    
    %% ===== DIŞ SİSTEMLER =====
    PSTN["PSTN Ağı\n(FXO/ISDN Sinyalleri)"]
    Kullanici["Kullanıcı Arayüzü\n(Web Tarayıcısı)"]
    HariciAPI["Harici API\n(CRM/ERP Sistemleri)"]
    
    %% ===== KENAR KATMANI =====
    telecom["telecom\nC++ PSTN Gateway\n• FXO/ISDN → SIP/RTP\n• Sinyal dönüşümü"]
    signal["signal\nRust SIP/RTP Sunucusu\n• 5060 UDP dinler\n• SIP parsing\n• gRPC entegrasyonu"]
    bridge["bridge\nNode.js API Gateway\n• REST/GraphQL API\n• OAuth2 yetkilendirme\n• gRPC çevirimi"]
    
    %% ===== ÇEKİRDEK KATMAN =====
    core["core\nGo Merkezi Motor\n• İş mantığı yürütme\n• Veritabanı işlemleri\n• Faturalandırma\n• Yönlendirme kararları"]
    
    %% ===== MEDYA & AI KATMANI =====
    media["media\nPython/C Ses İşleme\n• RTP (10000-20000 UDP)\n• Ses kaydı & transcoding\n• WebRTC köprüleme"]
    ai["ai\nPython Analitik\n• Speech-to-Text\n• Duygu analizi\n• Anahtar kelime tespiti"]
    
    %% ===== YÖNETİM ARAYÜZÜ =====
    console["console\nReact+TS Yönetim Paneli\n• Gerçek zamanlı izleme\n• Yapılandırma arayüzü\n• WebSocket entegrasyonu"]
    
    %% ===== NUMARALANDIRILMIŞ AKIŞLAR =====
    PSTN -- "1. Fiziksel Sinyal" --> telecom
    telecom -- "2. SIP Mesajı\nINVITE, 5060 UDP" --> signal
    signal -- "3. gRPC İsteği\nCallRequest, 50051 TCP" --> core
    core -- "4. Yönlendirme Kararı" --> signal
    core -- "5. Medya Oturumu Aç" --> media
    media -- "6. Port Bilgisi" --> core
    core -- "7. SDP Bilgisi" --> signal
    signal -- "8. 200 OK + SDP" --> telecom
    telecom -- "9. RTP Ses Akışı\n10000-20000 UDP" --> media
    media -- "10. Ses Kopyası" --> ai
    ai -- "11. Analiz Sonuçları" --> core
    Kullanici -- "12. HTTPS/WebSocket\n443/80 TCP" --> console
    console -- "13. WebSocket\nGerçek Zamanlı Veri" --> core
    HariciAPI -- "14. REST API\n8443 TCP" --> bridge
    bridge -- "15. gRPC\n50051 TCP" --> core
    
    %% ===== STİL ATAMALARI =====
    class PSTN,Kullanici,HariciAPI external
    class telecom,signal,bridge edge
    class core core
    class media,ai media
    class ai ai
    class console console
```


---
Basit gösterim
```mermaid
graph TD
    PSTN["PSTN Ağı"] --> telecom
    telecom -->|SIP| signal
    signal -->|gRPC| core
    core -->|Yönlendirme| signal
    core -->|Medya Komut| media
    media -->|Port Bilgisi| core
    core -->|SDP| signal
    signal -->|SIP Cevabı| telecom
    telecom -->|RTP| media
    media -->|Ses Kopyası| ai
    ai -->|Analiz| core
    Kullanici["Kullanıcı Arayüzü"] --> console
    console -->|WebSocket| core
    HariciAPI["Harici API"] --> bridge
    bridge -->|gRPC| core
    
    classDef external fill:#f5f5f5,stroke:#666
    class PSTN,Kullanici,HariciAPI external
```

---

### Akış Numaraları ve Protokol Tablosu:
| Akış | Kaynak | Hedef | Protokol | Port | Açıklama |
|------|--------|-------|----------|------|----------|
| 1 | PSTN | telecom | FXO/ISDN | - | Fiziksel sinyal |
| 2 | telecom | signal | SIP | 5060 | Çağrı başlatma |
| 3 | signal | core | gRPC | 50051 | Yönlendirme isteği |
| 4 | core | signal | gRPC | 50051 | Yönlendirme kararı |
| 5 | core | media | gRPC | 50051 | Medya oturum aç |
| 6 | media | core | gRPC | 50051 | Port bilgisi |
| 7 | core | signal | gRPC | 50051 | SDP bilgisi |
| 8 | signal | telecom | SIP | 5060 | Onay mesajı |
| 9 | telecom | media | RTP | 10000-20000 | Ses akışı |
| 10 | media | ai | gRPC | 50051 | Ses kopyası |
| 11 | ai | core | gRPC | 50051 | Analiz sonuçları |
| 12 | Kullanıcı | console | HTTPS | 443 | Arayüz bağlantısı |
| 13 | console | core | WebSocket | 80/443 | Gerçek zamanlı veri |
| 14 | Harici API | bridge | REST | 8443 | Entegrasyon |
| 15 | bridge | core | gRPC | 50051 | İç iletişim |

