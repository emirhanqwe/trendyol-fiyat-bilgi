import pandas as pd
from colorama import Fore, Style

def fiyatlari_segmentlere_ayir(df):
    if df.empty or "Fiyat (TL)" not in df.columns:
        print(f"{Fore.RED}⚠️  Veri seti boş veya fiyat sütunu bulunamadı!{Style.RESET_ALL}")
        return df, {}, pd.DataFrame()

    min_fiyat = df["Fiyat (TL)"].min()
    max_fiyat = df["Fiyat (TL)"].max()
    ortalama_fiyat = df["Fiyat (TL)"].mean()
    medyan_fiyat = df["Fiyat (TL)"].median()
    std_fiyat = df["Fiyat (TL)"].std()

    istatistikler = {
        "min_fiyat": min_fiyat,
        "max_fiyat": max_fiyat,
        "ortalama_fiyat": ortalama_fiyat,
        "medyan_fiyat": medyan_fiyat,
        "std_fiyat": std_fiyat
    }

    q33 = df["Fiyat (TL)"].quantile(0.33)
    q66 = df["Fiyat (TL)"].quantile(0.66)

    def segment_belirle(fiyat):
        if fiyat <= q33:
            return "1. Giriş Segmenti"
        elif fiyat <= q66:
            return "2. Orta Segment"
        else:
            return "3. Üst Segment"

    df["Segment"] = df["Fiyat (TL)"].apply(segment_belirle)

    segment_ozet = df.groupby("Segment").agg(
        Urun_Sayisi=('Fiyat (TL)', 'count'),
        Ortalama_Fiyat=('Fiyat (TL)', 'mean'),
        Min_Fiyat=('Fiyat (TL)', 'min'),
        Max_Fiyat=('Fiyat (TL)', 'max'),
        Ortalama_Puan=('Puan', 'mean'),
        Ortalama_Yorum=('Yorum Sayısı', 'mean')
    ).reset_index()

    # Segment sınırlarını da ekle
    segment_ozet["Segment_Siniri"] = segment_ozet["Segment"].map({
        "1. Giriş Segmenti": f"≤ {q33:,.0f} TL",
        "2. Orta Segment": f"{q33:,.0f} - {q66:,.0f} TL",
        "3. Üst Segment": f"> {q66:,.0f} TL"
    })

    # Renkli konsol çıktısı
    print(f"\n{Fore.CYAN}📊  PİYASA İSTATİSTİKLERİ{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ╔{'═' * 48}╗{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ║{Style.RESET_ALL} {Fore.WHITE}En Düşük Fiyat  {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} {Fore.GREEN}{min_fiyat:>10,.2f} TL{Style.RESET_ALL}          {Fore.LIGHTBLACK_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ║{Style.RESET_ALL} {Fore.WHITE}Ortalama Fiyat  {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} {Fore.CYAN}{ortalama_fiyat:>10,.2f} TL{Style.RESET_ALL}          {Fore.LIGHTBLACK_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ║{Style.RESET_ALL} {Fore.WHITE}Medyan Fiyat    {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} {Fore.CYAN}{medyan_fiyat:>10,.2f} TL{Style.RESET_ALL}          {Fore.LIGHTBLACK_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ║{Style.RESET_ALL} {Fore.WHITE}En Yüksek Fiyat {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} {Fore.MAGENTA}{max_fiyat:>10,.2f} TL{Style.RESET_ALL}          {Fore.LIGHTBLACK_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ║{Style.RESET_ALL} {Fore.WHITE}Standart Sapma  {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} {Fore.YELLOW}{std_fiyat:>10,.2f} TL{Style.RESET_ALL}          {Fore.LIGHTBLACK_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ╚{'═' * 48}╝{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}🏷️   SEGMENT SINIRLARI{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ┌{'─' * 46}┐{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   │{Style.RESET_ALL} {Fore.GREEN}🟢 Giriş Segmenti{Style.RESET_ALL}  ≤ {q33:,.0f} TL               {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   │{Style.RESET_ALL} {Fore.YELLOW}🟡 Orta Segment{Style.RESET_ALL}    {q33:,.0f} - {q66:,.0f} TL        {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   │{Style.RESET_ALL} {Fore.MAGENTA}🔴 Üst Segment{Style.RESET_ALL}     > {q66:,.0f} TL               {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   └{'─' * 46}┘{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}📋  SEGMENT DAĞILIMI{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   ┌{'─' * 46}┐{Style.RESET_ALL}")
    for _, row in segment_ozet.iterrows():
        seg_renk = Fore.GREEN if "Giriş" in row["Segment"] else (Fore.YELLOW if "Orta" in row["Segment"] else Fore.MAGENTA)
        bar_len = int((row["Urun_Sayisi"] / len(df)) * 30) if len(df) > 0 else 0
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"{Fore.LIGHTBLACK_EX}   │{Style.RESET_ALL} {seg_renk}{row['Segment']:<18}{Style.RESET_ALL} {bar} {row['Urun_Sayisi']:>3} adet {Fore.LIGHTBLACK_EX}│{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}   └{'─' * 46}┘{Style.RESET_ALL}")

    return df, istatistikler, segment_ozet