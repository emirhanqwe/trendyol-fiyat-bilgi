import pandas as pd
from veri_toplayici import trendyol_veri_cek
from segment_motoru import fiyatlari_segmentlere_ayir
from gorsellestirme import segment_grafigi_ciz
import os
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

def ekrani_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner_goster():
    banner = f"""
{Fore.CYAN}    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   {Fore.WHITE}████████╗██████╗ ███████╗███╗   ██╗██████╗ ██╗   ██╗       {Fore.CYAN}║
    ║   {Fore.WHITE}╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔══██╗╚██╗ ██╔╝       {Fore.CYAN}║
    ║   {Fore.WHITE}   ██║   ██████╔╝█████╗  ██╔██╗ ██║██║  ██║ ╚████╔╝        {Fore.CYAN}║
    ║   {Fore.WHITE}   ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║  ██║  ╚██╔╝         {Fore.CYAN}║
    ║   {Fore.WHITE}   ██║   ██║  ██║███████╗██║ ╚████║██████╔╝   ██║          {Fore.CYAN}║
    ║   {Fore.WHITE}   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝    ╚═╝          {Fore.CYAN}║
    ║                                                              ║
    ║   {Fore.YELLOW}📊  PİYASA ve SEGMENT ANALİZ MOTORU  v2.0{Style.RESET_ALL}                  {Fore.CYAN}║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def bilgi_kutusu(baslik, icerik, renk=Fore.CYAN):
    print(f"\n{renk}┌{'─' * 56}┐{Style.RESET_ALL}")
    print(f"{renk}│{Style.RESET_ALL} {Fore.WHITE}{baslik:<54}{Style.RESET_ALL}{renk} │{Style.RESET_ALL}")
    print(f"{renk}├{'─' * 56}┤{Style.RESET_ALL}")
    for satir in icerik:
        print(f"{renk}│{Style.RESET_ALL} {satir:<54}{Style.RESET_ALL}{renk} │{Style.RESET_ALL}")
    print(f"{renk}└{'─' * 56}┘{Style.RESET_ALL}")

def yukleniyor_animasyonu(mesaj, sure=1.5):
    import time
    print(f"\n{Fore.CYAN}⏳ {mesaj}{Style.RESET_ALL}", end="", flush=True)
    time.sleep(sure)
    print(f"\r{Fore.GREEN}✅ {mesaj} Tamamlandı!{Style.RESET_ALL}      ")

def kullanici_girdisi_al(mesaj, varsayilan=None, dogrulama=None):
    while True:
        if varsayilan:
            girdi = input(f"{Fore.MAGENTA}📝 {mesaj} {Fore.LIGHTBLACK_EX}[Varsayılan: {varsayilan}]{Style.RESET_ALL}: ").strip()
            if not girdi:
                girdi = varsayilan
        else:
            girdi = input(f"{Fore.MAGENTA}📝 {mesaj}{Style.RESET_ALL}: ").strip()

        if dogrulama and not dogrulama(girdi):
            print(f"{Fore.RED}⚠️  Geçersiz giriş! Lütfen tekrar deneyin.{Style.RESET_ALL}")
            continue
        return girdi

def analiz_sonuc_goster(df, istatistikler, urun_adi):
    print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}                    📈 ANALİZ SONUÇLARI{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")

    # Özet kartları
    print(f"\n{Fore.WHITE}   📦 Toplam Ürün: {Fore.CYAN}{len(df)}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   🔍 Analiz Edilen Ürün: {Fore.CYAN}{urun_adi.upper()}{Style.RESET_ALL}")

    # Segment bazlı en iyi ürünler
    print(f"\n{Fore.CYAN}   🏆 SEGMENT BAZLI EN İYİ ÜRÜNLER (Puan & Yorum){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   {'─' * 56}{Style.RESET_ALL}")

    for segment in ["1. Giriş Segmenti", "2. Orta Segment", "3. Üst Segment"]:
        seg_df = df[df["Segment"] == segment]
        if not seg_df.empty:
            seg_renk = Fore.GREEN if "Giriş" in segment else (Fore.YELLOW if "Orta" in segment else Fore.MAGENTA)
            # Puan ve yorum sayısına göre sırala
            seg_df_sorted = seg_df.sort_values(["Puan", "Yorum Sayısı"], ascending=[False, False])
            en_iyi = seg_df_sorted.iloc[0]

            print(f"   {seg_renk}● {segment}{Style.RESET_ALL}")
            print(f"      {Fore.WHITE}└─ {en_iyi['Ürün Adı'][:45]}{Style.RESET_ALL}")
            print(f"         {Fore.YELLOW}⭐ {en_iyi['Puan']:.1f}{Style.RESET_ALL} │ {Fore.CYAN}💬 {int(en_iyi['Yorum Sayısı'])} yorum{Style.RESET_ALL} │ {Fore.GREEN}{en_iyi['Fiyat (TL)']:,.2f} TL{Style.RESET_ALL}")

    print(f"{Fore.LIGHTBLACK_EX}   {'─' * 56}{Style.RESET_ALL}")

def excel_rapor_kaydet(df, segment_ozet, urun_adi):
    os.makedirs("excel", exist_ok=True)
    excel_dosya = os.path.join("excel", f"{urun_adi}_Piyasa_Analiz_Raporu.xlsx")

    try:
        with pd.ExcelWriter(excel_dosya, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Tüm Ürünler', index=False)
            segment_ozet.to_excel(writer, sheet_name='Segment Özetleri', index=False)

            # Sayfa genişliklerini ayarla
            for sheet in writer.sheets.values():
                for column in sheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if cell.value:
                                max_length = max(max_length, len(str(cell.value)))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    sheet.column_dimensions[column_letter].width = adjusted_width

        print(f"\n{Fore.GREEN}✅ Excel raporu başarıyla kaydedildi:{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}📁 {excel_dosya}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"\n{Fore.RED}❌ Excel kaydetme hatası: {e}{Style.RESET_ALL}")
        return False

def grafik_kaydet(segment_ozet, urun_adi):
    os.makedirs("grafik", exist_ok=True)
    grafik_dosya = os.path.join("grafik", f"{urun_adi}_segment_grafigi.png")

    try:
        segment_grafigi_ciz(segment_ozet, urun_adi, grafik_dosya)
        print(f"\n{Fore.GREEN}✅ Grafik başarıyla oluşturuldu:{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}📁 {grafik_dosya}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"\n{Fore.RED}❌ Grafik oluşturma hatası: {e}{Style.RESET_ALL}")
        return False

def ana_menu():
    ekrani_temizle()
    banner_goster()

    bilgi_kutusu(
        "HOŞ GELDİNİZ!",
        [
            "Bu uygulama Trendyol üzerindeki ürünleri analiz eder.",
            "Fiyat segmentasyonu, piyasa istatistikleri ve görsel",
            "raporlar oluşturur. Başlamak için bir ürün adı girin."
        ],
        Fore.GREEN
    )

    print(f"\n{Fore.CYAN}📋 MENÜ{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ┌{'─' * 30}┐{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   │{Style.RESET_ALL} {Fore.WHITE}[1] Yeni Analiz Başlat{Style.RESET_ALL}      {Fore.LIGHTBLACK_EX} │{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   │{Style.RESET_ALL} {Fore.WHITE}[2] Klasörleri Aç{Style.RESET_ALL}           {Fore.LIGHTBLACK_EX} │{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   │{Style.RESET_ALL} {Fore.WHITE}[Q] Çıkış{Style.RESET_ALL}                   {Fore.LIGHTBLACK_EX} │{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   └{'─' * 30}┘{Style.RESET_ALL}")

    secim = input(f"\n{Fore.MAGENTA}👉 Seçiminiz: {Style.RESET_ALL}").strip().lower()
    return secim

def yeni_analiz():
    ekrani_temizle()
    banner_goster()

    print(f"\n{Fore.CYAN}🔍 YENİ ANALİZ{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   {'─' * 50}{Style.RESET_ALL}\n")

    # Ürün adı al
    urun_adi = kullanici_girdisi_al(
        "Analiz edilecek ürün",
        dogrulama=lambda x: len(x) > 0
    )

    # Sayfa sayısı al
    sayfa_girdisi = input(f"{Fore.MAGENTA}📄 Kaç sayfa taranacak? {Fore.LIGHTBLACK_EX}[Boş=tümü, Sayı=limit]{Style.RESET_ALL}: ").strip()

    if sayfa_girdisi == "":
        max_sayfa = None
        print(f"{Fore.YELLOW}   ℹ️  Tüm okunabilir sayfalar taranacak.{Style.RESET_ALL}")
    elif sayfa_girdisi.isdigit() and int(sayfa_girdisi) > 0:
        max_sayfa = int(sayfa_girdisi)
        print(f"{Fore.YELLOW}   ℹ️  Maksimum {max_sayfa} sayfa taranacak.{Style.RESET_ALL}")
    else:
        max_sayfa = 2
        print(f"{Fore.YELLOW}   ℹ️  Geçersiz giriş. Varsayılan olarak 2 sayfa taranacak.{Style.RESET_ALL}")

    # Onay
    print(f"\n{Fore.CYAN}🚀 Analiz başlatılıyor...{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   Ürün: {urun_adi}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   Sayfa Limiti: {'Sınırsız' if max_sayfa is None else max_sayfa}{Style.RESET_ALL}\n")

    onay = input(f"{Fore.MAGENTA}▶️  Başlamak için Enter'a basın (İptal: q){Style.RESET_ALL}").strip().lower()
    if onay == 'q':
        print(f"\n{Fore.YELLOW}🛑 Analiz iptal edildi.{Style.RESET_ALL}")
        return False

    # 1. AŞAMA: Veri Toplama
    print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   1️⃣  AŞAMA: VERİ TOPLAMA{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")

    raw_veri = trendyol_veri_cek(urun_adi, max_sayfa=max_sayfa)

    if not raw_veri:
        print(f"\n{Fore.RED}{'═' * 60}{Style.RESET_ALL}")
        print(f"{Fore.RED}   ❌ HATA: Ürün verisi çekilemedi!{Style.RESET_ALL}")
        print(f"{Fore.RED}   🔧 Olası nedenler:{Style.RESET_ALL}")
        print(f"{Fore.RED}      • İnternet bağlantınızı kontrol edin{Style.RESET_ALL}")
        print(f"{Fore.RED}      • Ürün adını doğru yazdığınızdan emin olun{Style.RESET_ALL}")
        print(f"{Fore.RED}      • Trendyol erişim kısıtlaması olabilir{Style.RESET_ALL}")
        print(f"{Fore.RED}{'═' * 60}{Style.RESET_ALL}")
        return False

    df = pd.DataFrame(raw_veri)
    print(f"\n{Fore.GREEN}✅ Toplam {len(df)} adet benzersiz ürün verisi toplandı.{Style.RESET_ALL}")

    # 2. AŞAMA: Segmentasyon
    print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   2️⃣  AŞAMA: SEGMENTASYON ve İSTATİSTİKLER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")

    df, istatistikler, segment_ozet = fiyatlari_segmentlere_ayir(df)

    # 3. AŞAMA: Raporlama
    print(f"\n{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   3️⃣  AŞAMA: RAPORLARIN HAZIRLANMASI{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")

    excel_basari = excel_rapor_kaydet(df, segment_ozet, urun_adi)
    grafik_basari = grafik_kaydet(segment_ozet, urun_adi)

    # 4. AŞAMA: Sonuç Özeti
    analiz_sonuc_goster(df, istatistikler, urun_adi)

    # Tamamlama mesajı
    print(f"\n{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}   🎉 ANALİZ BAŞARIYLA TAMAMLANDI!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

    durumlar = []
    if excel_basari:
        durumlar.append(f"{Fore.GREEN}📊 Excel Raporu: Hazır{Style.RESET_ALL}")
    if grafik_basari:
        durumlar.append(f"{Fore.GREEN}📈 Grafik: Hazır{Style.RESET_ALL}")

    for durum in durumlar:
        print(f"   {durum}")

    print(f"\n{Fore.YELLOW}💡 İpucu: 'excel' ve 'grafik' klasörlerini kontrol edin.{Style.RESET_ALL}")

    return True

def klasorleri_ac():
    import subprocess
    import platform

    os.makedirs("excel", exist_ok=True)
    os.makedirs("grafik", exist_ok=True)

    sistem = platform.system()
    try:
        if sistem == "Windows":
            subprocess.Popen(["explorer", "excel"])
            subprocess.Popen(["explorer", "grafik"])
        elif sistem == "Darwin":  # macOS
            subprocess.Popen(["open", "excel"])
            subprocess.Popen(["open", "grafik"])
        else:  # Linux
            subprocess.Popen(["xdg-open", "excel"])
            subprocess.Popen(["xdg-open", "grafik"])
        print(f"\n{Fore.GREEN}📂 Klasörler açıldı!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}⚠️  Klasör açılamadı: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Manuel olarak 'excel' ve 'grafik' klasörlerine bakabilirsiniz.{Style.RESET_ALL}")

def ana_calistirici():
    while True:
        secim = ana_menu()

        if secim == '1':
            basari = yeni_analiz()
            if basari:
                print(f"\n{Fore.MAGENTA}🔄 Ana menüye dönmek için Enter'a basın...{Style.RESET_ALL}")
                input()
        elif secim == '2':
            klasorleri_ac()
            print(f"\n{Fore.MAGENTA}🔄 Ana menüye dönmek için Enter'a basın...{Style.RESET_ALL}")
            input()
        elif secim in ['q', 'quit', 'exit']:
            ekrani_temizle()
            print(f"""
{Fore.CYAN}    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        {Fore.GREEN}✨ Teşekkürler! Görüşmek üzere... ✨{Style.RESET_ALL}                    {Fore.CYAN}║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
            """)
            break
        else:
            print(f"\n{Fore.RED}⚠️  Geçersiz seçim! Lütfen tekrar deneyin.{Style.RESET_ALL}")
            import time
            time.sleep(1.5)
            
if __name__ == "__main__":
    try:
        ana_calistirici()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}🛑 Program kullanıcı tarafından durduruldu.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Beklenmeyen hata: {e}{Style.RESET_ALL}")
        sys.exit(1)