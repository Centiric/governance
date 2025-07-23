# ADR 001: `signal` Servisi için Rust Dilinin Seçilmesi

- **Tarih:** 2023-10-15
- **Durum:** Kabul Edildi

## Bağlam (Context)

`signal` servisi, platformun internete açık olan ilk savunma hattıdır. Yüksek hacimli SIP/RTP trafiğini karşılayacak, güvenli ve son derece performanslı olması gerekmektedir.

## Değerlendirilen Alternatifler

1.  **Go:** `core` servisiyle aynı dili kullanmanın getireceği geliştirme kolaylığı. Ancak, manuel bellek yönetimi olmaması (Garbage Collector) nedeniyle en düşük gecikme (lowest-latency) senaryolarında performans dalgalanmaları yaşanabilir.
2.  **C++:** En yüksek ham performansı sunar. Ancak, bellek yönetimi hatalarına (memory safety issues) son derece açıktır, bu da güvenlik zafiyetlerine yol açabilir.
3.  **Rust:** C++'a yakın performans sunarken, derleyici seviyesinde bellek güvenliğini (memory safety) garanti eder ("Borrow Checker" sayesinde). Modern asenkron çalışma (async/await) yetenekleri, ağ programlama için idealdir.

## Karar

Yüksek performans, düşük gecikme ve en önemlisi **bellek güvenliği** garantisi nedeniyle `signal` servisi için **Rust** dili seçilmiştir. Bu karar, servisin hem hızlı hem de güvenli olmasını sağlayarak platformun genel kararlılığını artıracaktır.

## Sonuçlar (Consequences)

-   **Pozitif:** Güvenlik zafiyeti riski (CVE) azalır. Öngörülebilir ve düşük gecikmeli performans.
-   **Negatif:** Ekip içinde yeni bir dil öğrenme eğrisi olabilir. Go'ya göre geliştirme hızı başlangıçta daha yavaş olabilir.
