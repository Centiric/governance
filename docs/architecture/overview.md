# Centiric VoIP Mimarisi

## Çekirdek Bileşenler
```mermaid
flowchart LR
    A[PSTN] --> B[telecom]
    B --> C[core]
    C --> D[signal]
    D --> E[media]
```

## Protokol Seçimleri
| Bileşen      | Protokol    | Gerekçe                     |
|--------------|-------------|----------------------------|
| Signal       | SIP over UDP| Düşük gecikme              |
| Core         | gRPC        | Yüksek performans          |
| Console      | WebSocket   | Gerçek zamanlı veri        |
