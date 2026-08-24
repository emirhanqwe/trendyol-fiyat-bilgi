# 📊 Trendyol Piyasa ve Segment Analiz Motoru v2.0

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-D22128?style=for-the-badge&logo=apache)
![Vibe Coding](https://img.shields.io/badge/Developed%20With-Vibe%20Coding-8A2BE2?style=for-the-badge)
![Trendyol](https://img.shields.io/badge/Target-Trendyol-F27A1A?style=for-the-badge)

Trendyol platformundaki ürün verilerini otomatik olarak toplayan, gelişmiş istatistiksel yöntemlerle (yüzdelik dilim / quantiles) fiyat segmentasyonu yapan, terminal üzerinden renkli rapor sunan ve neticesinde **Excel raporları** ile **yüksek çözünürlüklü grafikler** üreten modern bir piyasa analiz aracıdır.

> ⚡ **Not:** Bu proje, AI destekli hızlı ve verimli geliştirme yaklaşımı olan **Vibe Coding** ile hayata geçirilmiştir.

---

## 🌟 Öne Çıkan Özellikler

* **🛡️ Gelişmiş Web Kazıma (Scraping):** `curl_cffi` ile Chrome IP/TLS taklidi yapılarak anti-bot ve erişim engelleri aşılır.
* **📊 İstatistiksel Fiyat Segmentasyonu:** Ürün fiyatları `%33` ve `%66` quantiles (yüzdelik dilimler) baz alınarak otomatik olarak **1. Giriş Segmenti**, **2. Orta Segment** ve **3. Üst Segment** olarak sınıflandırılır.
* **💻 İnteraktif Terminal Arayüzü:** `colorama` destekli dinamik menüler, renkli tablolar, yükleme animasyonları ve ASCII logolar.
* **📈 Yüksek Çözünürlüklü Görselleştirme:** `matplotlib` ve `seaborn` kullanılarak modern renk paleti, segment bazlı ortalama fiyatlar, ürün adetleri ve yüzde dağılımlarını gösteren grafikler üretilir (PNG, 300 DPI).
* **📁 Otomatik Excel Raporlama:** `openpyxl` motoru ile ürün listesi, fiyatlar, puanlar, yorum sayıları ve segment özetleri otomatik olarak biçimlendirilmiş Excel dosyasına dönüştürülür.
* **🏆 Segment Bazlı En İyi Ürün Analizi:** Her segment içerisindeki en yüksek puana ve yorum sayısına sahip lider ürünler tespit edilip gösterilir.

---

## 🛠️ Teknolojiler ve Kütüphaneler

| Bileşen | Kullanılan Kütüphane / Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Veri Toplama** | `curl_cffi`, `beautifulsoup4` | Anti-bot korumalı web kazıma ve HTML ayrıştırma |
| **Veri Analizi** | `pandas`, `numpy` | Veri temizleme, quantiles ve istatistiksel hesaplamalar |
| **Görselleştirme** | `matplotlib`, `seaborn` | Görsel grafiklerin üretilmesi ve özelleştirilmesi |
| **Arayüz & CLI** | `colorama` | Renkli konsol çıktıları ve dinamik menü tasarımı |
| **Raporlama** | `openpyxl` | Excel formatında detaylı çıktı alma |

---

## 📂 Proje Yapısı

```
.
├── main.py       # Uygulamanın ana giriş noktası ve CLI menü yönetimi
├── veri_toplayici.py     # Trendyol veri çekme (scraping) ve deduplikasyon motoru
├── segment_motoru.py     # Quantile bazlı fiyat segmentasyonu ve istatistik hesaplama
├── gorsellestirme.py     # Matplotlib/Seaborn grafik çizim modülü
├── requirements.txt      # Gerekli Python kütüphaneleri listesi
├── install.bat           # Windows kullanıcıları için tek tıkla bağımlılık yükleyici
```

---

## 🚀 Kurulum ve Kullanım

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/4lon3D4rk/trendyol-fiyat-bilgi.git
cd trendyol-fiyat-bilgi
```

### 2. Bağımlılıkları Yükleyin

#### Windows:
`install.bat` dosyasına çift tıklayarak otomatik olarak yükleyebilirsiniz veya terminalden:
```cmd
install.bat
```

#### macOS / Linux:
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Çalıştırın
```bash
python main.py
```

---

## 🖥️ Kullanım Adımları

1. Uygulama başladığında ana menüden `[1] Yeni Analiz Başlat` seçeneğini seçin.
2. Analiz etmek istediğiniz ürün adını girin (örneğin: `kablosuz kulaklık`, `oyuncu faresi`).
3. Taranacak sayfa sınırını belirtin (Varsayılan olarak boş bırakırsanız tüm sayfalar taranır).
4. İşlem tamamlandığında:
   * Konsolda segment bazlı istatistikler ve en iyi ürünler listelenir.
   * `excel/` klasörüne detaylı `.xlsx` raporu kaydedilir.
   * `grafik/` klasörüne yüksek çözünürlüklü `.png` grafiği oluşturulur.
5. `[2] Klasörleri Aç` seçeneği ile çıktı klasörlerine doğrudan erişebilirsiniz.

---

## 📜 Lisans

Bu proje **Apache License 2.0** ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.

---

## ✨ Katkıda Bulunma

1. Bu depoyu Fork edin.
2. Yeni bir özellik dalı oluşturun (`git checkout -b feature/YeniOzellik`).
3. Değişikliklerinizi işleyin (`git commit -m 'Yeni özellik eklendi'`).
4. Dalınıza gönderin (`git push origin feature/YeniOzellik`).
5. Bir Pull Request oluşturun.
