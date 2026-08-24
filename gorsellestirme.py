import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def segment_grafigi_ciz(segment_ozet, urun_adi, kayit_yolu):
    if segment_ozet.empty:
        print("Grafik çizmek için özet veri bulunamadı.")
        return

    # Modern tema ayarları
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.facecolor'] = '#f8f9fa'
    plt.rcParams['figure.facecolor'] = '#ffffff'
    plt.rcParams['axes.edgecolor'] = '#dee2e6'
    plt.rcParams['axes.labelcolor'] = '#495057'
    plt.rcParams['xtick.color'] = '#495057'
    plt.rcParams['ytick.color'] = '#495057'
    plt.rcParams['text.color'] = '#212529'

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Modern renk paleti (gradient tonları)
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    edge_colors = ['#27ae60', '#e67e22', '#c0392b']

    # Segment sıralamasını koru
    segment_order = ["1. Giriş Segmenti", "2. Orta Segment", "3. Üst Segment"]
    segment_ozet = segment_ozet.set_index('Segment').reindex(segment_order).reset_index()

    bars = ax1.bar(
        segment_ozet['Segment'], 
        segment_ozet['Urun_Sayisi'],
        color=colors,
        edgecolor=edge_colors,
        linewidth=2.5,
        width=0.6,
        alpha=0.9,
        zorder=3
    )

    # Y ekseni ayarları
    ax1.set_ylabel('Ürün Sayısı', fontsize=13, fontweight='bold', color='#495057', labelpad=15)
    ax1.set_ylim(0, max(segment_ozet['Urun_Sayisi']) * 1.25)
    ax1.tick_params(axis='y', labelsize=11, colors='#495057')
    ax1.tick_params(axis='x', labelsize=12, colors='#495057')

    # X ekseni etiketlerini kısalt
    ax1.set_xticks(range(len(segment_ozet)))
    ax1.set_xticklabels(['Giriş\nSegmenti', 'Orta\nSegment', 'Üst\nSegment'], fontsize=11)
    ax1.set_xlabel('')

    # Grid ayarları
    ax1.yaxis.grid(True, linestyle='--', alpha=0.4, color='#adb5bd', zorder=0)
    ax1.set_axisbelow(True)

    # Bar üzerine değer yazıları
    for i, (bar, (_, row)) in enumerate(zip(bars, segment_ozet.iterrows())):
        yukseklik = bar.get_height()
        ort_fiyat = row["Ortalama_Fiyat"]
        yuzde = (yukseklik / segment_ozet['Urun_Sayisi'].sum()) * 100

        # Ana değer (ürün sayısı)
        ax1.text(
            bar.get_x() + bar.get_width() / 2.,
            yukseklik + max(segment_ozet['Urun_Sayisi']) * 0.03,
            f'{int(yukseklik)} adet',
            ha='center', va='bottom',
            fontsize=12, fontweight='bold', color=edge_colors[i]
        )

        # İç ortalama fiyat
        ax1.text(
            bar.get_x() + bar.get_width() / 2.,
            yukseklik / 2,
            f'Ort. Fiyat\n{ort_fiyat:,.0f} TL',
            ha='center', va='center',
            fontsize=10, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=edge_colors[i], alpha=0.8, edgecolor='none')
        )

        # Yüzde değeri barın altına
        ax1.text(
            bar.get_x() + bar.get_width() / 2.,
            -max(segment_ozet['Urun_Sayisi']) * 0.08,
            f'%{yuzde:.1f}',
            ha='center', va='top',
            fontsize=10, color=colors[i], fontweight='bold'
        )

    # Başlık ve alt başlık
    ax1.set_title(
        f"'{urun_adi.upper()}' Piyasa Segment Analizi",
        fontsize=16, fontweight="bold", color='#212529', pad=20
    )
    ax1.text(
        0.5, 1.02, 
        f"Toplam {segment_ozet['Urun_Sayisi'].sum()} ürün analiz edildi",
        transform=ax1.transAxes,
        ha='center', va='bottom',
        fontsize=10, color='#6c757d', style='italic'
    )

    # Sağ üst köşe bilgi kutusu
    info_text = f"""Segment Sınırları:
• Giriş: {segment_ozet.iloc[0]['Segment_Siniri'] if 'Segment_Siniri' in segment_ozet.columns else 'N/A'}
• Orta: {segment_ozet.iloc[1]['Segment_Siniri'] if 'Segment_Siniri' in segment_ozet.columns else 'N/A'}
• Üst: {segment_ozet.iloc[2]['Segment_Siniri'] if 'Segment_Siniri' in segment_ozet.columns else 'N/A'}"""

    ax1.text(
        0.98, 0.98, info_text,
        transform=ax1.transAxes,
        ha='right', va='top',
        fontsize=9, color='#495057',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#e9ecef', alpha=0.9, edgecolor='#dee2e6')
    )

    # Alt bilgi çubuğu
    fig.text(
        0.5, 0.02,
        'Trendyol Piyasa Analiz Motoru │ Segmentler fiyat bazlı tercil (33% - 66%) ile belirlenmiştir',
        ha='center', va='bottom',
        fontsize=8, color='#adb5bd', style='italic'
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)
    plt.savefig(kayit_yolu, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()