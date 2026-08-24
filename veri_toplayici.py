from curl_cffi import requests
from bs4 import BeautifulSoup
import re
import time
import random
from colorama import Fore, Style

def trendyol_veri_cek(kelime, max_sayfa=None):
    urunler = []
    gorulen_urunler = set()
    formatli_kelime = kelime.replace(' ', '+')

    session = requests.Session(impersonate="chrome120")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.trendyol.com/"
    }

    # Bağlantı başlatma
    print(f"{Fore.CYAN}🌐  Trendyol'a bağlanılıyor...{Style.RESET_ALL}")
    try:
        session.get("https://www.trendyol.com/", headers=headers, timeout=10)
        time.sleep(1.5)
        print(f"{Fore.GREEN}✅  Bağlantı başarılı!{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}⚠️  Bağlantı hatası: {e}{Style.RESET_ALL}")
        return urunler

    sayfa = 1
    bos_sayfa_sayaci = 0
    ardisik_hata_sayaci = 0
    ust_limit = max_sayfa if max_sayfa is not None else 30

    print(f"{Fore.YELLOW}📄  Sayfalar taranmaya başlıyor...{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   {'─' * 50}{Style.RESET_ALL}")

    while sayfa <= ust_limit:
        if sayfa == 1:
            url = f"https://www.trendyol.com/sr?q={formatli_kelime}&qt={formatli_kelime}&st={formatli_kelime}&os=1"
        else:
            url = f"https://www.trendyol.com/sr?q={formatli_kelime}&qt={formatli_kelime}&st={formatli_kelime}&os=1&pi={sayfa}"

        try:
            response = session.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                ardisik_hata_sayaci = 0
                soup = BeautifulSoup(response.text, "html.parser")
                kartlar = soup.select("a.product-card, a[data-testid='product-card']")

                if not kartlar:
                    print(f"{Fore.YELLOW}   📭 Sayfa {sayfa:2d} │ Boş döndü. Tarama sonlandırılıyor...{Style.RESET_ALL}")
                    break

                eklenen_sayisi = 0
                for kart in kartlar:
                    marka_elem = kart.select_one("span.product-brand")
                    ad_elem = kart.select_one("span.product-name")

                    marka = marka_elem.text.strip() if marka_elem else ""
                    ad = ad_elem.text.strip() if ad_elem else ""
                    tam_baslik = f"{marka} {ad}".strip() or "Bilinmeyen Ürün"

                    link_uzanti = kart.get("href", "")
                    tam_link = f"https://www.trendyol.com{link_uzanti}" if link_uzanti else ""

                    if tam_baslik in gorulen_urunler:
                        continue

                    fiyat_elem = kart.select_one("div.price-section, div[data-testid='price-section']")

                    puan_elem = kart.select_one("span.rating-score, div[data-testid='rating-score']")
                    yorum_elem = kart.select_one("span.ratingCount, span[data-testid='rating-count']")

                    puan = 0.0
                    if puan_elem:
                        try:
                            puan = float(puan_elem.text.strip().replace(',', '.'))
                        except ValueError:
                            pass

                    yorum_sayisi = 0
                    if yorum_elem:
                        yorum_metni = re.sub(r"\D", "", yorum_elem.text.strip())
                        if yorum_metni:
                            yorum_sayisi = int(yorum_metni)

                    if fiyat_elem:
                        fiyat_metni = fiyat_elem.text.strip()
                        temiz_fiyat = re.sub(r"[^\d,\.]", "", fiyat_metni).replace(".", "").replace(",", ".")
                        try:
                            fiyat_float = float(temiz_fiyat)
                            urunler.append({
                                "Ürün Adı": tam_baslik, 
                                "Fiyat (TL)": fiyat_float,
                                "Puan": puan,
                                "Yorum Sayısı": yorum_sayisi,
                                "Ürün Linki": tam_link
                            })
                            gorulen_urunler.add(tam_baslik)
                            eklenen_sayisi += 1
                        except ValueError:
                            continue

                durum_rengi = Fore.GREEN if eklenen_sayisi > 0 else Fore.YELLOW
                print(f"{durum_rengi}   📄 Sayfa {sayfa:2d} │ {eklenen_sayisi:3d} yeni ürün │ Toplam: {len(urunler):4d} ürün{Style.RESET_ALL}")

                if eklenen_sayisi == 0:
                    bos_sayfa_sayaci += 1
                    if bos_sayfa_sayaci >= 2:
                        print(f"{Fore.YELLOW}   ⛔ İki ardışık boş sayfa. Son sayfaya ulaşıldı.{Style.RESET_ALL}")
                        break
                else:
                    bos_sayfa_sayaci = 0

                sayfa += 1
            else:
                ardisik_hata_sayaci += 1
                print(f"{Fore.RED}   🚫 Sayfa {sayfa:2d} │ Erişim engeli (Kod: {response.status_code}){Style.RESET_ALL}")
                if ardisik_hata_sayaci >= 3:
                    print(f"{Fore.RED}   ⛔ Üç ardışık engelleme! Tarama güvenli şekilde durduruldu.{Style.RESET_ALL}")
                    break
                sayfa += 1

        except Exception as e:
            ardisik_hata_sayaci += 1
            print(f"{Fore.RED}   ⚠️  Sayfa {sayfa:2d} │ Hata: {str(e)[:40]}{Style.RESET_ALL}")
            if ardisik_hata_sayaci >= 3:
                print(f"{Fore.RED}   ⛔ Üç ardışık hata! Tarama durduruldu. Tekrar deneyiniz.{Style.RESET_ALL}")
                input(f"{Fore.LIGHTRED_EX}   ⏸️  Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
                break
            sayfa += 1

        time.sleep(random.uniform(1.5, 3.0))

    print(f"{Fore.LIGHTBLACK_EX}   {'─' * 50}{Style.RESET_ALL}")
    return urunler