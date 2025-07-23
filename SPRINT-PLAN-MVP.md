# Sprint Planı: MVP Çekirdek Altyapısı

- **Amaç:** Temel SIP/UDP akışını uçtan uca çalışır hale getirmek.
- **Süre:** 2 Hafta
- **Hedef Çıktı:** Dışarıdan gelen bir SIP `INVITE` mesajını yakalayıp, `core`'da işleyip, `media`'da teorik bir ses oturumu başlatabilmek.

---

### **Aşama 1: Sinyal Yakalama ve Yönlendirme (Sprint 1. Hafta)**

**Hedef:** `signal` -> `core` iletişimini tamamlamak.

```mermaid
flowchart TD
    subgraph "Odak Alanı"
        A[Dış Dünya<br><i>Softphone</i>] -->|"1. SIP INVITE<br>(UDP:5060)"| B(<b>signal</b>)
        B -->|"2. SIP Ayrıştırma<br><i>From/To/Call-ID</i>"| C(Temizlenmiş Veri)
        C -->|"3. gRPC İsteği<br>(TCP:50051)"| D{<b>core</b>}
        D -->|"4. gRPC Cevabı<br><i>ACCEPT/REJECT</i>"| B
    end
```
