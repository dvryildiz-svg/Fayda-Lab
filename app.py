import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sayılar için Türk tipi formatlama fonksiyonu (Binlik ayracı nokta, ondalık ayracı virgül)
def format_tr(value, decimals=0):
    if decimals == 0:
        return f"{value:,.0f}".replace(",", ".")
    else:
        return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="FaydaLab Simülatörü", page_icon="📊", layout="wide")
st.title("📊 FaydaLab: Saha Operasyonu ve Büyüme Simülatörü")

# --- SOL MENÜ: MEVCUT OPERASYON GİRDİLERİ ---
st.sidebar.header("🚛 Mevcut Saha Dinamikleri")
arac_sayisi = st.sidebar.number_input("Araç Sayısı", min_value=1, value=10, step=1)
arac_basi_nokta = st.sidebar.number_input("Araç Başı Nokta", min_value=1, value=150, step=10)

arac_basi_ciro = st.sidebar.number_input("Araç Başı Aylık Ciro (TL)", min_value=0, value=400000, step=10000)
st.sidebar.caption(f"💰 Değer: **{format_tr(arac_basi_ciro)} TL**")

st.sidebar.markdown("**Aylık Giderler**")
arac_amortisman = st.sidebar.number_input("Araç Başı Amortisman (TL)", min_value=0, value=15000, step=1000)
st.sidebar.caption(f"📉 Değer: **{format_tr(arac_amortisman)} TL**")

arac_yakit = st.sidebar.number_input("Araç Başı Yakıt (TL)", min_value=0, value=25000, step=1000)
st.sidebar.caption(f"⛽ Değer: **{format_tr(arac_yakit)} TL**")

toplam_eleman_maliyet = st.sidebar.number_input("Toplam Satış Ekibi Maliyeti (TL)", min_value=0, value=500000, step=10000)
st.sidebar.caption(f"👥 Değer: **{format_tr(toplam_eleman_maliyet)} TL**")

aylik_ziyaret = st.sidebar.number_input("Toplam Aylık Ziyaret Sayısı", min_value=1, value=3000, step=100)
urun_karliligi = st.sidebar.slider("Ürün Kârlılığı (%)", min_value=1, max_value=100, value=20, step=1)

# --- MATEMATİKSEL HESAPLAMALAR (MEVCUT) ---
toplam_ciro = arac_sayisi * arac_basi_ciro
toplam_nokta = arac_sayisi * arac_basi_nokta
nokta_basi_ciro = toplam_ciro / toplam_nokta if toplam_nokta > 0 else 0

toplam_yakit = arac_yakit * arac_sayisi
toplam_amortisman = arac_amortisman * arac_sayisi
toplam_saha_maliyeti = toplam_eleman_maliyet + toplam_yakit + toplam_amortisman

ziyaret_basi_maliyet = toplam_saha_maliyeti / aylik_ziyaret if aylik_ziyaret > 0 else 0
ziyaret_maliyet_yuzdesi = (toplam_saha_maliyeti / toplam_ciro) * 100 if toplam_ciro > 0 else 0
basabas_ciro = ziyaret_basi_maliyet / (urun_karliligi / 100) if urun_karliligi > 0 else 0

# --- SOL MENÜ: FAYDALAB BÜYÜME GİRDİLERİ ---
st.sidebar.header("🚀 FaydaLab Büyüme Hedefleri")
sehir_secimi = st.sidebar.selectbox("Genişleme Bölgesi (Şehir)", ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Türkiye Geneli"])
yeni_nokta_sayisi = st.sidebar.number_input(f"{sehir_secimi} - Tahmini Ek Nokta", min_value=0, value=1000, step=100)
faydalab_komisyon = st.sidebar.number_input("FaydaLab Komisyonu (%)", min_value=1, value=5, step=1)

# --- MATEMATİKSEL HESAPLAMALAR (FAYDALAB) ---
faydalab_nokta_ciro = nokta_basi_ciro * 0.50  # %50 Performans varsayımı
faydalab_ek_ciro = yeni_nokta_sayisi * faydalab_nokta_ciro
faydalab_komisyon_gideri = faydalab_ek_ciro * (faydalab_komisyon / 100)
faydalab_net_kar = (faydalab_ek_ciro * (urun_karliligi / 100)) - faydalab_komisyon_gideri

# --- ANA EKRAN: YÖNETİCİ ÖZETİ ---
with st.expander("📖 Dinamik Yönetici Özeti ve Fayda Analizi", expanded=True):
    st.markdown(f"""
    **1. Mevcut Sahadaki Gizli Tehlike (Birim Maliyetler):**
    Şu anki yapınızda kasanıza giren toplam {format_tr(toplam_ciro)} TL ciro için, sahada her ay **{format_tr(toplam_saha_maliyeti)} TL** operasyon (araç, yakıt, personel) maliyeti katlanıyorsunuz. Cironuzun doğrudan **%{format_tr(ziyaret_maliyet_yuzdesi, 1)}'i** sadece kapıyı çalma maliyetine gidiyor.
    
    Daha çarpıcı olanı; ekibinizin yaptığı **her bir ziyaretin şirketinize maliyeti {format_tr(ziyaret_basi_maliyet, 1)} TL'dir.** %{urun_karliligi} kâr marjıyla çalıştığınız için, ziyaret edilen bir bakkalın o gün size sadece "zarar ettirmemesi" (başa baş noktası) için minimum **{format_tr(basabas_ciro, 1)} TL** sipariş vermesi şarttır. 
    
    **2. FaydaLab ile Risksiz Büyüme ({sehir_secimi} Örneği):**
    Aynı hacmi kendi filonuzla büyütmek yerine, FaydaLab'ın o bölgedeki hazır dağıtım ağına ürününüzü entegre ettiğimizde:
    * **{format_tr(yeni_nokta_sayisi)}** yeni noktaya sıfır araç, sıfır yakıt ve sıfır personel maliyetiyle girersiniz.
    * Bu noktaların mevcut noktalarınızın sadece **yarısı (%50)** kadar performans göstereceğini (nokta başı {format_tr(faydalab_nokta_ciro)} TL) en muhafazakâr senaryoda bile varsaysak, aylık **{format_tr(faydalab_ek_ciro)} TL** ek ciro yaratılır.
    * Üstelik bu ciro için yapacağınız tek ödeme, satış gerçekleştikçe ödenecek {format_tr(faydalab_komisyon_gideri)} TL başarı primidir. Kasada kalan net ek kârınız **{format_tr(faydalab_net_kar)} TL** olacaktır.
    """)

# --- SEKME (TAB) YAPISI ---
tab1, tab2 = st.tabs(["📉 Mevcut Operasyon MR'ı", "🚀 FaydaLab Büyüme Simülasyonu"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Toplam Aylık Ciro", f"{format_tr(toplam_ciro)} TL")
    col2.metric("Nokta Başı Aylık Ciro", f"{format_tr(nokta_basi_ciro)} TL")
    col3.metric("Ziyaret Başı Maliyet", f"{format_tr(ziyaret_basi_maliyet, 1)} TL", "Araç+Yakıt+Personel", delta_color="inverse")
    col4.metric("Başa Baş Noktası (Ciro)", f"{format_tr(basabas_ciro, 1)} TL", "Zarar etmemek için şart", delta_color="inverse")
    
    st.markdown("---")
    fig1 = go.Figure(data=[go.Pie(labels=['Toplam Eleman', 'Toplam Yakıt', 'Toplam Amortisman'], 
                                  values=[toplam_eleman_maliyet, toplam_yakit, toplam_amortisman], 
                                  hole=.4)])
    fig1.update_layout(title_text="Mevcut Saha Maliyetlerinin Kırılımı")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.markdown(f"### {sehir_secimi} Bölgesi Yayılım Analizi")
    c1, c2, c3 = st.columns(3)
    c1.metric("FaydaLab Ek Ciro (Aylık)", f"+{format_tr(faydalab_ek_ciro)} TL", f"{format_tr(yeni_nokta_sayisi)} Yeni Nokta")
    c2.metric("Operasyon/Dağıtım Maliyeti", "0 TL", "Sıfır Sabit Gider")
    c3.metric("Yaratılan Ek Net Kâr", f"+{format_tr(faydalab_net_kar)} TL", f"Komisyon düşüldükten sonra")
    
    st.markdown("---")
    # Kıyaslama Grafiği
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name='Kendi Ekibinizle Yapılsaydı (Tahmini Maliyet)',
        x=['Dağıtım Maliyeti', 'Kalan Kâr'],
        y=[faydalab_ek_ciro * (ziyaret_maliyet_yuzdesi/100), (faydalab_ek_ciro * (urun_karliligi/100)) - (faydalab_ek_ciro * (ziyaret_maliyet_yuzdesi/100))],
        marker_color='#ff9999'
    ))
    fig2.add_trace(go.Bar(
        name='FaydaLab ile (Gerçekleşen)',
        x=['Dağıtım Maliyeti', 'Kalan Kâr'],
        y=[faydalab_komisyon_gideri, faydalab_net_kar],
        marker_color='#00cc96'
    ))
    fig2.update_layout(barmode='group', title_text=f"{format_tr(faydalab_ek_ciro)} TL'lik Ek Ciro İçin Maliyet/Kâr Kıyaslaması")
    st.plotly_chart(fig2, use_container_width=True)
