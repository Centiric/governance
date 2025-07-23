# Centiric Platformu Geliştirme Rehberi

Bu rehber, Centiric platformunu yerel makinede veya bir sunucuda geliştirmek için gerekli araçları, kurulum adımlarını ve en iyi pratikleri içerir.

---

## 1. Ön Gereksinimler

Platformu geliştirmek için aşağıdaki araçların sisteminizde kurulu olması gerekmektedir.

### Genel Araçlar
- **Git:** Versiyon kontrol sistemi.
- **Docker & Docker Compose (Önerilir):** Servisleri izole ortamlarda çalıştırmak için.
- **Bir Metin Düzenleyici:** VS Code, Neovim, GoLand, CLion vb.

### Dil ve Platforma Özel Araçlar
| Teknoloji | Gerekli Araçlar | Kurulum Komutu (Debian/Ubuntu) | Kurulum Komutu (Windows - choco) |
|:---|:---|:---|:---|
| **Go** (`core`) | Go Compiler (1.21+) | `sudo apt install golang-go` | `choco install golang` |
| | Protobuf Compiler | `sudo apt install protobuf-compiler` | `choco install protoc` |
| | gRPC Go Eklentileri| `go install ...` | `go install ...` |
| **Rust** (`signal`)| Rust Toolchain | `curl ... \| sh` | `winget install Rustlang.Rustup` |
| | C++ Build Tools | `sudo apt install build-essential` | Visual Studio Installer |
| **Node.js** (`bridge`)| Node.js (20+) & npm| `sudo apt install nodejs npm` | `choco install nodejs` |
| **Python** (`media, ai`)| Python (3.10+) & pip| `sudo apt install python3 python3-pip` | `choco install python` |

---

## 2. Proje Kurulumu

1.  **Tüm Repoları Klonlama:**
    Projenin tüm servislerini içeren bir ana klasör oluşturun.
    ```bash
    mkdir centiric-platform && cd centiric-platform
    
    # GitHub CLI ile veya manuel olarak tüm repoları klonlayın
    gh repo clone Centiric/governance
    gh repo clone Centiric/core
    gh repo clone Centiric/signal
    # ...diğer repolar...
    ```

---

## 3. Kodlama Standartları ve En İyi Pratikler

### a) Loglama

Tüm servisler **yapılandırılmış (structured) JSON formatında** log üretmelidir. Bu, logların merkezi bir sistemde (Loki, Elasticsearch) kolayca taranmasını ve analiz edilmesini sağlar. Her log satırı en az şu alanları içermelidir:

- `timestamp`: Olayın zamanı (ISO 8601 formatında).
- `level`: Log seviyesi (`INFO`, `WARN`, `ERROR`, `DEBUG`).
- `service`: Logu üreten servisin adı (örn: "signal", "core").
- `trace_id`: Olayın ilişkili olduğu çağrının veya işlemin benzersiz kimliği.
- `message`: Olayın açıklaması.

**Örnek Log Satırı (`signal` servisinden):**
```json
{"timestamp": "2023-10-16T10:00:01Z", "level": "INFO", "service": "signal", "trace_id": "uuid-abc-123", "message": "100 Trying gönderildi", "remote_addr": "194.48.95.2:5060"}
```

### b) İzlenebilirlik (Tracing)

Platformumuz, dağıtık izleme (distributed tracing) prensibini benimser.
1.  **`TraceID` Oluşturma:** Bir işlemi başlatan ilk Kenar Katmanı servisi (`signal`, `bridge`), eğer gelen istekte bir `TraceID` yoksa, yeni bir tane oluşturmakla yükümlüdür.
2.  **`TraceID` Yayılımı:** Bu `TraceID`, sonraki tüm servisler arası gRPC çağrılarının **metadata** bölümünde taşınmalıdır.
3.  **Loglama Entegrasyonu:** Her servis, aldığı `TraceID`'yi kendi ürettiği tüm log satırlarına dahil etmelidir.

---

## 4. Kodlama Standartları ve En İyi Pratikler

-   **Commit Mesajları:** `feat(core): Add user authentication` gibi [Conventional Commits](https://www.conventionalcommits.org/) standardını takip edin.
-   **Branch (Dal) İsimlendirme:** `feature/add-call-recording` veya `fix/memory-leak-in-signal` gibi şemalar kullanın.
-   **Dokümantasyon:** Eklenen her yeni public fonksiyon veya API endpoint'i için kod içi dokümantasyon eklenmelidir.

---

## 5. Sorun Giderme

-   **`protoc: command not found`:** Protobuf Compiler'ı kurduğunuzdan ve PATH'e eklediğinizden emin olun.
-   **`permission denied` (Port Hatası):** Çalıştırdığınız portun başka bir uygulama tarafından kullanılmadığını `netstat -ano` komutuyla kontrol edin. Gerekirse komut istemini yönetici olarak çalıştırın.
-   **Rust Derleme Hataları:** `build-essential` (Linux) veya C++ Build Tools'un (Windows) kurulu olduğundan emin olun. `cargo clean` komutuyla derleme önbelleğini temizlemeyi deneyin.
