# Centiric - Nihai Sistem Mimarisi

Bu doküman, Centiric platformunu oluşturan tüm servislerin mimari yapısını, sorumluluklarını ve aralarındaki veri akışını detaylandırmaktadır.

---

### **Mimari Diyagram**

Aşağıdaki diyagram, servislerin katmanlı yapısını ve aralarındaki temel iletişim akışlarını göstermektedir.

```mermaid
graph TD
    subgraph " "
        direction LR
        subgraph "<b>Dış Dünya</b>"
            direction TB
            A[("📞<br>PSTN Ağı")]
            B[("💻<br>Kullanıcı Arayüzü")]
            C[("🔌<br>Harici API")]
        end

        subgraph "<b>Centiric Platformu</b>"
            direction LR
            subgraph "🛡️<br><b>Kenar Katmanı</b>"
                direction TB
                E["<b>signal</b><br><small>Rust<br><i>SIP/RTP Sunucusu</i></small>"]
                D["<b>telecom</b><br><small>C++<br><i>PSTN Gateway</i></small>"]
                F["<b>bridge</b><br><small>Node.js<br><i>API Gateway</i></small>"]
            end
            
            subgraph "🧠<br><b>Çekirdek Katman</b>"
                direction TB
                G(((<b>core</b><br><small>Go<br><i>İş Mantığı Motoru</i></small>)))
            end

            subgraph "🎙️<br><b>Medya Katmanı</b>"
                direction TB
                H["<b>media</b><br><small>Python<br><i>Ses İşleme & WebRTC</i></small>"]
                I["<b>ai</b><br><small>Python<br><i>Yapay Zeka Analitiği</i></small>"]
            end
        end
    end

    %% --- Veri Akışları & Protokoller ---
    A -- "1. Fiziksel Sinyal" --> D
    D -- "2. SIP (UDP:5060)" --> E
    E -- "3. gRPC İsteği" --> G
    G -- "4. Yönlendirme Kararı" --> E

    B -- "HTTPS/WebSocket" --> G
    C -- "REST/GraphQL" --> F
    F -- "gRPC İsteği" --> G

    E -- "6. Medya Bilgisi (SDP)" --> H
    G -- "5. Medya Oturumu Aç" --> H
    D -- "7. RTP (Ses Akışı)" --> H
    H -- "8. Ses Kopyası" --> I
    I -- "9. Analiz Verisi" --> G
    
    %% --- Stil Tanımları ---
    classDef default fill:#fff,stroke:#555,stroke-width:2px,font-family:Arial,font-size:12px
    classDef edge fill:#e3f2fd,stroke:#1e88e5
    classDef core fill:#e8f5e9,stroke:#388e3c,stroke-width:3px
    classDef media fill:#fff3e0,stroke:#f57c00
    classDef external fill:#f5f5f5,stroke:#8d8d8d,stroke-dasharray: 5 5

    class A,B,C external
    class D,E,F edge
    class G core
    class H,I media
