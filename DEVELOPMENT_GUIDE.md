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

## 3. Servislerin Kurulumu ve Çalıştırılması

Her servisin kendi dizininde, o servise özel talimatları izleyin.

### a) `core` Servisi (Go)

`core` servisi, platformun iş mantığı merkezidir.

1.  **Dizine Girin:**
    ```bash
    cd core/
    ```
2.  **Protobuf Kodlarını Oluşturun:**
    `core`'un API tanımını Go koduna çevirin.
    ```bash
    protoc --go_out=. --go_opt=paths=source_relative \
           --go-grpc_out=. --go-grpc_opt=paths=source_relative \
           proto/core.proto
    ```
3.  **Bağımlılıkları Yükleyin:**
    ```bash
    go mod tidy
    ```
4.  **Servisi Çalıştırın:**
    ```bash
    go run .
    # Çıktı: Server started at [::]:50051
    ```

### b) `signal` Servisi (Rust)

`signal` servisi, dış dünyadan gelen SIP trafiğini karşılar.

1.  **Dizine Girin:**
    ```bash
    cd signal/
    ```
2.  **Derleme ve Çalıştırma:**
    `cargo`, Protobuf derlemesi dahil tüm süreci otomatik olarak yönetir.
    ```bash
    cargo run
    # Çıktı: SIP Sunucusu başlatıldı, dinleniyor: 0.0.0.0:5060
    ```
3.  **Sunucu Kurulumu Notu (Linux):**
    `signal`'ı bir sunucuda çalıştırıyorsanız, güvenlik duvarından `5060/udp` portuna izin verdiğinizden emin olun.
    ```bash
    sudo ufw allow 5060/udp
    sudo ufw reload
    ```

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
