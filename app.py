import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def format_tr(value, decimals=0):
    if decimals == 0:
        return f"{value:,.0f}".replace(",", ".")
    else:
        return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="FaydaLab Simülatörü", page_icon="📊", layout="wide")
st.title("📊 FaydaLab: Entegre Ticari Operasyon ve Büyüme Simülatörü")

# --- SOL MENÜ: MEVCUT OPERASYON GİRDİLERİ ---
st.sidebar.header("🚛 Mevcut Saha Dinamikleri")
arac_sayisi = st.sidebar.number_input("Araç Sayısı", min_value=1, value=10, step=1)
arac_basi_nokta = st.sidebar.number_input("Araç Başı Nokta (Aylık)", min_value=1, value=150, step=10)
arac_basi_ciro = st.sidebar.number_input("Araç Başı Aylık Ciro (TL)", min_value=0, value=400000, step=10000)
st.sidebar.caption(f"💰 Değer: **{format_tr(arac_basi_ciro)} TL**")

st.sidebar.markdown("**Aylık Giderler**")
arac_amortisman = st.sidebar.number_input("Araç Başı Amortisman (TL)", min_value=0, value=15000, step=1000)
st.sidebar.caption(f"📉 Değer: **{format_tr(arac_amortisman)} TL**")

arac_yakit = st.sidebar.number_input("Araç Başı Yakıt (TL)", min_value=0, value=25000, step=1000)
st.sidebar.caption(f"⛽ Değer: **{format_tr(arac_yakit)} TL**")

toplam_eleman_maliyet = st.sidebar.number_input("Toplam Satış Ekibi Maliyeti (TL)", min_value=0, value=500000, step=10000)
st.sidebar.caption(f"👥 Değer: **{format_tr(toplam_eleman_maliyet)} TL**")

aylik_ziyaret = st.sidebar.number_input("Toplam Aylık Fiziksel Ziyaret", min_value=1, value=3000, step=100)
urun_karliligi = st.sidebar.slider("Ürün Kârlılığı (Brüt %)", min_value=1, max_value=100, value=20, step=1)

# --- MATEMATİKSEL HESAPLAMALAR (MEVCUT DURUM) ---
toplam_ciro = arac_sayisi * arac_basi_ciro
toplam_nokta = arac_sayisi * arac_basi_nokta
nokta_basi_ciro = toplam_ciro / toplam_nokta if toplam_nokta > 0 else 0

toplam_yakit = arac_yakit * arac_sayisi
toplam_amortisman = arac_amortisman * arac_sayisi
toplam_saha_maliyeti = toplam_eleman_maliyet + toplam_yakit + toplam_amortisman

ziyaret_basi_maliyet = toplam_saha_maliyeti / aylik_ziyaret if aylik_ziyaret > 0 else 0
ziyaret_maliyet_yuzdesi = (toplam_saha_maliyeti / toplam_ciro) * 100 if toplam_ciro > 0 else 0
basabas_ciro = ziyaret_basi_maliyet / (urun_karliligi / 100) if urun_karliligi > 0 else 0

# --- SOL MENÜ: FAYDALAB YENİ AĞ BÜYÜME GİRDİLERİ ---
st.sidebar.header("🚀 FaydaLab Dış Ağ Genişlemesi")
sehir_secimi = st.sidebar.selectbox("Genişleme Bölgesi (Şehir)", ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Türkiye Geneli"])
yeni_nokta_sayisi = st.sidebar.number_input(f"{sehir_secimi} - Tahmini Ek Nokta", min_value=0, value=1000, step=100)
faydalab_yeni_ag_komisyon = st.sidebar.number_input("Dış Ağ Komisyonu (%)", min_value=1, value=5, step=1)

faydalab_nokta_ciro = nokta_basi_ciro * 0.50 
faydalab_ek_ciro = yeni_nokta_sayisi * faydalab_nokta_ciro
faydalab_komisyon_gideri = faydalab_ek_ciro * (faydalab_yeni_ag_komisyon / 100)
faydalab_net_kar = (faydalab_ek_ciro * (urun_karliligi / 100)) - faydalab_komisyon_gideri

# --- SEKME (TAB) YAPISI ---
tab1, tab2, tab3 = st.tabs(["📉 Mevcut Operasyon MR'ı", "🚀 Dış Ağ Büyümesi", "⚙️ Mevcut Saha Optimizasyonu"])

with tab1:
    st.markdown("### Mevcut Saha Birim Maliyetleri")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Toplam Aylık Ciro", f"{format_tr(toplam_ciro)} TL")
    col2.metric("Nokta Başı Aylık Ciro", f"{format_tr(nokta_basi_ciro)} TL")
    col3.metric("Ziyaret Başı Maliyet", f"{format_tr(ziyaret_basi_maliyet, 1)} TL", "Araç+Yakıt+Personel", delta_color="inverse")
    col4.metric("Başa Baş Noktası (Ciro)", f"{format_tr(basabas_ciro, 1)} TL", "Zarar etmemek için şart", delta_color="inverse")
    
    fig1 = go.Figure(data=[go.Pie(labels=['Toplam Eleman', 'Toplam Yakıt', 'Toplam Amortisman'], 
                                  values=[toplam_eleman_maliyet, toplam_yakit, toplam_amortisman], 
                                  hole=.4)])
    fig1.update_layout(title_text="Mevcut Saha Maliyetlerinin Kırılımı", margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.markdown(f"### {sehir_secimi} Bölgesi Yayılım Analizi (FaydaLab Ağı)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Yaratılan Ek Ciro (Aylık)", f"+{format_tr(faydalab_ek_ciro)} TL", f"{format_tr(yeni_nokta_sayisi)} Yeni Nokta")
    c2.metric("Operasyon/Dağıtım Maliyeti", "0 TL", "Sıfır Sabit Gider")
    c3.metric("Kalan Ek Net Kâr", f"+{format_tr(faydalab_net_kar)} TL", f"Komisyon düşüldükten sonra")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name='Kendi Ekibinizle Yapılsaydı',
        x=['Dağıtım Maliyeti', 'Kalan Kâr'],
        y=[faydalab_ek_ciro * (ziyaret_maliyet_yuzdesi/100), (faydalab_ek_ciro * (urun_karliligi/100)) - (faydalab_ek_ciro * (ziyaret_maliyet_yuzdesi/100))],
        marker_color='#ff9999'
    ))
    fig2.add_trace(go.Bar(
        name='FaydaLab Ağı ile',
        x=['Dağıtım Maliyeti', 'Kalan Kâr'],
        y=[faydalab_komisyon_gideri, faydalab_net_kar],
        marker_color='#00cc96'
    ))
    fig2.update_layout(barmode='group', title_text=f"Maliyet/Kâr Kıyaslaması", margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("### 🎯 Ticari Operasyon ve Performans Optimizasyonu")
    st.markdown("FaydaLab danışmanlığı ile mevcut ekibinizin rut planlaması, prim sistemi (kademe bazlı hakediş) ve ticari pazarlama (çapraz satış/teşhir) dinamikleri yeniden kurgulandığında oluşacak verimlilik artışı:")
    
    # Varsayılan mevcut metriklerin tersine mühendisliği
    mevcut_strike_rate_varsayilan = 40
    mevcut_siparis_sayisi = aylik_ziyaret * (mevcut_strike_rate_varsayilan / 100)
    mevcut_drop_size = toplam_ciro / mevcut_siparis_sayisi if mevcut_siparis_sayisi > 0 else 0

    st.info(f"📍 **Mevcut Durum Analizi:** {format_tr(aylik_ziyaret)} ziyaretin ortalama **%{mevcut_strike_rate_varsayilan}**'ı siparişe dönüşmekte ve faturaya yansıyan ortalama sipariş tutarı (Drop Size) **{format_tr(mevcut_drop_size)} TL** seviyesindedir.")

    # Optimizasyon Girdileri
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        hedef_strike_rate = st.slider("Hedef Başarılı Ziyaret Oranı (%)", min_value=10, max_value=90, value=55, step=5)
        st.caption("Rut optimizasyonu ve teşviklerle artırılan sipariş kapatma oranı.")
    with sc2:
        sepet_buyume = st.slider("Hedef Çapraz Satış Büyümesi (%)", min_value=0, max_value=50, value=15, step=1)
        st.caption("Tanzim/Teşhir ve Ticari Pazarlama kampanyaları ile faturadaki kalem artışı.")
    with sc3:
        prim_butcesi = st.slider("Ekibe Dağıtılacak Başarı Primi (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
        st.caption("Sadece yaratılan *ek ciro* üzerinden sahaya ödenecek prim.")

    # Yeni Durum Hesaplamaları
    yeni_siparis_sayisi = aylik_ziyaret * (hedef_strike_rate / 100)
    yeni_drop_size = mevcut_drop_size * (1 + (sepet_buyume / 100))
    yeni_toplam_ciro = yeni_siparis_sayisi * yeni_drop_size
    
    yaratilan_ek_ciro = yeni_toplam_ciro - toplam_ciro
    ek_brut_kar = yaratilan_ek_ciro * (urun_karliligi / 100)
    
    # Yeni Gider Kalemleri (Sadece Ek Ciro Üzerinden)
    dagitilan_prim = yaratilan_ek_ciro * (prim_butcesi / 100)
    ticari_pazarlama_gideri = yeni_toplam_ciro * 0.01  # Tüm cironun %1'i ticari pazarlamaya ayrılır
    faydalab_yonetim_komisyonu = yaratilan_ek_ciro * 0.03 # Ek ciro üzerinden %3 başarı primi
    
    sirkete_kalan_net_kar = ek_brut_kar - (dagitilan_prim + ticari_pazarlama_gideri + faydalab_yonetim_komisyonu)

    st.markdown("---")
    kc1, kc2, kc3, kc4 = st.columns(4)
    kc1.metric("Yeni Aylık Ciro", f"{format_tr(yeni_toplam_ciro)} TL", f"+{format_tr(yaratilan_ek_ciro)} TL Büyüme")
    kc2.metric("Sahaya Ödenen Prim", f"{format_tr(dagitilan_prim)} TL", f"Personel Motivasyonu", delta_color="off")
    kc3.metric("FaydaLab Başarı Bedeli", f"{format_tr(faydalab_yonetim_komisyonu)} TL", "Performansa Dayalı", delta_color="off")
    kc4.metric("Şirkete Kalan Net Kâr Artışı", f"+{format_tr(sirkete_kalan_net_kar)} TL", "Tüm giderler düşüldükten sonra")

    # Şelale (Waterfall) Grafiği ile Ek Ciro Dağılımı
    fig3 = go.Figure(go.Waterfall(
        name="Ek Kâr Dağılımı",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Yaratılan Ek Brüt Kâr", "Saha Ekibi Başarı Primi", "Ticari Paz. & Sadakat Bütçesi", "FaydaLab Yönetim Komisyonu", "Şirkete Kalan Net Kâr"],
        textposition="outside",
        text=[f"+{format_tr(ek_brut_kar)}", f"-{format_tr(dagitilan_prim)}", f"-{format_tr(ticari_pazarlama_gideri)}", f"-{format_tr(faydalab_yonetim_komisyonu)}", f"{format_tr(sirkete_kalan_net_kar)}"],
        y=[ek_brut_kar, -dagitilan_prim, -ticari_pazarlama_gideri, -faydalab_yonetim_komisyonu, sirkete_kalan_net_kar],
        connector={"line":{"color":"rgb(63, 63, 63)"}}
    ))
    fig3.update_layout(title="Yaratılan Ek Kârlılığın Bütçe Dağılımı (Şelale Analizi)", showlegend=False, margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig3, use_container_width=True)
