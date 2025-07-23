# ADR 002: `media` Servisi için Hibrit Teknoloji Yaklaşımı

- **Tarih:** 2023-10-16
- **Durum:** Kabul Edildi

## Bağlam (Context)

`media` servisi, gerçek zamanlı ses paketlerini (RTP) işlemekle yükümlüdür. Bu görev, çok düşük gecikme (<20ms), yüksek verim ve minimum paket kaybı gerektirir. Aynı zamanda, hızlı bir şekilde çalışan bir prototipe ihtiyacımız var.

## Karar

`media` servisi için **iki aşamalı, hibrit bir teknoloji stratejisi** benimsenmiştir:

1.  **Aşama 1: Prototip ve MVP (Python):**
    *   İlk prototip, Python'un `asyncio` kütüphanesi kullanılarak geliştirilecektir.
    *   **Gerekçe:** Bu yaklaşım, `signal` ve `core` ile olan entegrasyonu hızla test etmemizi ve uçtan uca medya akışını kanıtlamamızı sağlar. Geliştirme hızı en yüksek önceliktir.
    *   **Risk:** Python'un GIL (Global Interpreter Lock) mekanizması, çok yüksek yük altında performans darboğazı yaratabilir.

2.  **Aşama 2: Üretim Optimizasyonu (Rust veya C++):**
    *   Prototip testleri sonucunda, Python'un performansı (gecikme, paket kaybı, CPU kullanımı) hedeflenen metrikleri karşılamazsa, servis **Rust veya C++** kullanılarak yeniden yazılacaktır.
    *   **Gerekçe:** Rust/C++, bellek üzerinde tam kontrol, GC (Garbage Collector) olmaması ve donanıma yakın çalışma yetenekleri sayesinde gerçek zamanlı medya işleme için en ideal performansı sunar.
    *   **Geçiş Kriteri:** Prototip, 100 eşzamanlı çağrı altında >%0.1 paket kaybı veya >20ms işlem gecikmesi gösterirse, Aşama 2'ye geçiş kararı alınacaktır.

## Sonuçlar (Consequences)

Bu hibrit yaklaşım, projenin hem hızlı bir şekilde ilerlemesini (Python sayesinde) hem de uzun vadede performans hedeflerinden ödün vermemesini (Rust/C++ opsiyonu sayesinde) garanti eder.
