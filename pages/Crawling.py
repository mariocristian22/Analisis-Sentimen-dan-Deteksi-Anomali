import textwrap
import streamlit as st
import pandas as pd
from google_play_scraper import reviews, Sort

st.set_page_config(page_title="Crawling", page_icon="🔍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

:root {
    --bg: #0a0e1a;
    --bg-panel: #111827;
    --border: #1f2d45;
    --text: #e2e8f0;
    --text-dim: #94a3b8;
    --accent: #3b82f6;
    --accent-soft: rgba(59, 130, 246, 0.1);
    --green: #10b981;
    --green-soft: rgba(16, 185, 129, 0.1);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
}

.stApp { background: var(--bg); }

[data-testid="stSidebar"] {
    background: var(--bg-panel);
    border-right: 1px solid var(--border);
}

/* HERO BANNER */
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 48px 56px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    pointer-events: none;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
    pointer-events: none;
}

.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--accent-soft);
    border: 1px solid rgba(59,130,246,0.3);
    color: #60a5fa;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.2;
    margin-bottom: 14px;
}

.hero-title span {
    background: linear-gradient(90deg, #3b82f6, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-desc {
    font-size: 15px;
    color: var(--text-dim);
    line-height: 1.7;
    max-width: 600px;
    margin-bottom: 28px;
}

.hero-stats {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
}

.hero-stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.hero-stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #f1f5f9;
}

.hero-stat-label {
    font-size: 12px;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.hero-icon {
    position: absolute;
    right: 56px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 96px;
    opacity: 0.06;
    user-select: none;
}

/* STAGE TRACKER */
.stage-wrap {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 24px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 0;
}

/* SECTION HEADER */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 16px 0;
}

.section-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: #f1f5f9;
}

/* CARD */
.config-card {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}

/* METRIC */
[data-testid="stMetric"] {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
}

[data-testid="stMetricLabel"] { color: var(--text-dim) !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-family: 'Space Grotesk', sans-serif !important; }

/* BUTTON */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #2563eb !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59,130,246,0.4) !important;
}

.stDownloadButton > button {
    background: var(--green-soft) !important;
    color: var(--green) !important;
    border: 1px solid var(--green) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* SELECT */
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

/* DIVIDER */
.divider {
    height: 1px;
    background: var(--border);
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# ── STAGE TRACKER ─────────────────────────────────────────
stages = ["Crawling", "Analisis Data", "Classification", "Report", "Dashboard", "Testing"]
nodes_html = ""
for i, s in enumerate(stages):
    active = (s == "Crawling")
    done = False
    bc = "#3b82f6" if active else ("#1f2d45" if not done else "#3b82f6")
    bg = "transparent" if active else ("#1f2d45")
    lc = "#60a5fa" if active else "#475569"
    glow = "box-shadow:0 0 8px #3b82f6;" if active else ""
    nodes_html += (
        f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:0;">'
        f'<div style="width:12px;height:12px;border-radius:50%;border:2px solid {bc};background:{bg};{glow}"></div>'
        f'<div style="font-size:10px;color:{lc};margin-top:6px;text-align:center;font-weight:{"600" if active else "400"};white-space:nowrap;">{i+1}. {s}</div>'
        f'</div>'
    )
    if i < len(stages) - 1:
        nodes_html += f'<div style="flex:0.6;height:1px;background:#1f2d45;margin-top:6px;"></div>'

st.markdown(
    f'<div style="background:#111827;border:1px solid #1f2d45;border-radius:12px;padding:14px 24px;'
    f'margin-bottom:24px;display:flex;align-items:flex-start;">{nodes_html}</div>',
    unsafe_allow_html=True
)

# ── HERO BANNER ───────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">📡 Google Play Store · Steam Mobile</div>
    <div class="hero-title">Crawling <span>Data Ulasan</span></div>
    <div class="hero-desc">
        Ambil data ulasan pengguna aplikasi Steam secara langsung dari Google Play Store.
        Pilih negara dan jumlah data, lalu unduh hasilnya dalam format CSV untuk dianalisis lebih lanjut.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">189</div>
            <div class="hero-stat-label">Negara Tersedia</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Real-time</div>
            <div class="hero-stat-label">Sumber Data</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">CSV</div>
            <div class="hero-stat-label">Format Output</div>
        </div>
    </div>
    <div class="hero-icon">🎮</div>
</div>
""", unsafe_allow_html=True)

# ── KONFIGURASI ───────────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Konfigurasi Crawling</div></div>', unsafe_allow_html=True)

APP_ID = 'com.valvesoftware.android.steam.community'

col1, col2 = st.columns(2)
with col1:
    urutan = st.selectbox("Urutkan berdasarkan", ["Terbaru", "Relevansi"], index=0)
with col2:
    negara_options = {
        "Indonesia": ("id", "id"), "Amerika Serikat": ("en", "us"), "Kanada": ("en", "ca"),
        "Meksiko": ("es", "mx"), "Brasil": ("pt", "br"), "Argentina": ("es", "ar"),
        "Chile": ("es", "cl"), "Kolombia": ("es", "co"), "Peru": ("es", "pe"),
        "Venezuela": ("es", "ve"), "Ekuador": ("es", "ec"), "Bolivia": ("es", "bo"),
        "Paraguay": ("es", "py"), "Uruguay": ("es", "uy"), "Jamaika": ("en", "jm"),
        "Trinidad dan Tobago": ("en", "tt"), "Barbados": ("en", "bb"), "Bahama": ("en", "bs"),
        "Belize": ("en", "bz"), "Kosta Rika": ("es", "cr"), "Panama": ("es", "pa"),
        "Guatemala": ("es", "gt"), "Honduras": ("es", "hn"), "El Salvador": ("es", "sv"),
        "Nicaragua": ("es", "ni"), "Republik Dominika": ("es", "do"), "Haiti": ("fr", "ht"),
        "Kuba": ("es", "cu"), "Puerto Riko": ("es", "pr"), "Inggris": ("en", "gb"),
        "Irlandia": ("en", "ie"), "Prancis": ("fr", "fr"), "Jerman": ("de", "de"),
        "Italia": ("it", "it"), "Spanyol": ("es", "es"), "Portugal": ("pt", "pt"),
        "Belanda": ("nl", "nl"), "Belgia": ("fr", "be"), "Swiss": ("de", "ch"),
        "Austria": ("de", "at"), "Polandia": ("pl", "pl"), "Rusia": ("ru", "ru"),
        "Ukraina": ("uk", "ua"), "Turki": ("tr", "tr"), "Ceko": ("cs", "cz"),
        "Rumania": ("ro", "ro"), "Hungaria": ("hu", "hu"), "Yunani": ("el", "gr"),
        "Swedia": ("sv", "se"), "Norwegia": ("no", "no"), "Denmark": ("da", "dk"),
        "Finlandia": ("fi", "fi"), "Slovakia": ("sk", "sk"), "Slovenia": ("sl", "si"),
        "Bulgaria": ("bg", "bg"), "Serbia": ("sr", "rs"), "Kroasia": ("hr", "hr"),
        "Bosnia dan Herzegovina": ("bs", "ba"), "Makedonia Utara": ("mk", "mk"), "Albania": ("sq", "al"),
        "Montenegro": ("sr", "me"), "Latvia": ("lv", "lv"), "Lituania": ("lt", "lt"),
        "Estonia": ("et", "ee"), "Islandia": ("is", "is"), "Malta": ("mt", "mt"),
        "Luksemburg": ("fr", "lu"), "Belarus": ("be", "by"), "Moldova": ("ro", "md"),
        "Siprus": ("el", "cy"), "San Marino": ("it", "sm"), "Monako": ("fr", "mc"),
        "Liechtenstein": ("de", "li"), "Andorra": ("ca", "ad"), "Vatikan": ("it", "va"),
        "Jepang": ("ja", "jp"), "Korea Selatan": ("ko", "kr"), "China": ("zh", "cn"),
        "Taiwan": ("zh", "tw"), "Hong Kong": ("zh", "hk"), "Malaysia": ("ms", "my"),
        "Thailand": ("th", "th"), "Vietnam": ("vi", "vn"), "Singapura": ("en", "sg"),
        "Filipina": ("tl", "ph"), "India": ("hi", "in"), "Pakistan": ("ur", "pk"),
        "Bangladesh": ("bn", "bd"), "Kamboja": ("km", "kh"), "Laos": ("lo", "la"),
        "Myanmar": ("my", "mm"), "Sri Lanka": ("si", "lk"), "Nepal": ("ne", "np"),
        "Kazakhstan": ("kk", "kz"), "Uzbekistan": ("uz", "uz"), "Kirgizstan": ("ky", "kg"),
        "Tajikistan": ("tg", "tj"), "Turkmenistan": ("tk", "tm"), "Azerbaijan": ("az", "az"),
        "Armenia": ("hy", "am"), "Georgia": ("ka", "ge"), "Mongolia": ("mn", "mn"),
        "Makau": ("zh", "mo"), "Brunei": ("ms", "bn"), "Timor-Leste": ("pt", "tl"),
        "Bhutan": ("dz", "bt"), "Maladewa": ("dv", "mv"), "Afghanistan": ("fa", "af"),
        "Arab Saudi": ("ar", "sa"), "Uni Emirat Arab": ("ar", "ae"), "Mesir": ("ar", "eg"),
        "Israel": ("he", "il"), "Iran": ("fa", "ir"), "Irak": ("ar", "iq"),
        "Yordania": ("ar", "jo"), "Lebanon": ("ar", "lb"), "Kuwait": ("ar", "kw"),
        "Qatar": ("ar", "qa"), "Oman": ("ar", "om"), "Bahrain": ("ar", "bh"),
        "Suriah": ("ar", "sy"), "Yaman": ("ar", "ye"), "Palestina": ("ar", "ps"),
        "Afrika Selatan": ("en", "za"), "Nigeria": ("en", "ng"), "Kenya": ("sw", "ke"),
        "Tanzania": ("sw", "tz"), "Ghana": ("en", "gh"), "Kamerun": ("fr", "cm"),
        "Senegal": ("fr", "sn"), "Pantai Gading": ("fr", "ci"), "Etiopia": ("am", "et"),
        "Uganda": ("sw", "ug"), "Mozambik": ("pt", "mz"), "Angola": ("pt", "ao"),
        "Zambia": ("en", "zm"), "Zimbabwe": ("en", "zw"), "Rwanda": ("fr", "rw"),
        "Botswana": ("en", "bw"), "Namibia": ("en", "na"), "Malawi": ("en", "mw"),
        "Mauritius": ("en", "mu"), "Tunisia": ("fr", "tn"), "Maroko": ("ar", "ma"),
        "Aljazair": ("ar", "dz"), "Libya": ("ar", "ly"), "Sudan": ("ar", "sd"),
        "Burkina Faso": ("fr", "bf"), "Mali": ("fr", "ml"), "Niger": ("fr", "ne"),
        "Togo": ("fr", "tg"), "Benin": ("fr", "bj"), "Gabon": ("fr", "ga"),
        "Republik Demokratik Kongo": ("fr", "cd"), "Republik Kongo": ("fr", "cg"), "Somalia": ("so", "so"),
        "Djibouti": ("fr", "dj"), "Eritrea": ("ti", "er"), "Madagaskar": ("fr", "mg"),
        "Komoro": ("ar", "km"), "Seychelles": ("fr", "sc"), "Tanjung Verde": ("pt", "cv"),
        "Guinea": ("fr", "gn"), "Guinea-Bissau": ("pt", "gw"), "Guinea Khatulistiwa": ("es", "gq"),
        "Sierra Leone": ("en", "sl"), "Liberia": ("en", "lr"), "Gambia": ("en", "gm"),
        "Sao Tome dan Principe": ("pt", "st"), "Afrika Tengah": ("fr", "cf"), "Chad": ("fr", "td"),
        "Sudan Selatan": ("en", "ss"), "Burundi": ("fr", "bi"), "Lesotho": ("en", "ls"),
        "Eswatini": ("en", "sz"), "Australia": ("en", "au"), "Selandia Baru": ("en", "nz"),
        "Papua Nugini": ("en", "pg"), "Fiji": ("en", "fj"), "Kepulauan Solomon": ("en", "sb"),
        "Vanuatu": ("fr", "vu"), "Samoa": ("en", "ws"), "Tonga": ("en", "to"),
        "Kiribati": ("en", "ki"), "Nauru": ("en", "nr"), "Tuvalu": ("en", "tv"),
        "Palau": ("en", "pw"), "Mikronesia": ("en", "fm"), "Kepulauan Marshall": ("en", "mh"),
    }
    negara_pilihan = st.selectbox("Pilih negara", list(negara_options.keys()), index=0)

lang, country = negara_options[negara_pilihan]
sort_order = Sort.NEWEST if urutan == "Terbaru" else Sort.MOST_RELEVANT

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if st.button("🚀 Mulai Crawling"):
    status_placeholder = st.empty()
    all_reviews = []
    continuation_token = None
    batch_size = 200

    try:
        with st.spinner(f"Sedang mengambil data dari {negara_pilihan}..."):
            while True:
                hasil, continuation_token = reviews(
                    APP_ID, lang=lang, country=country, sort=sort_order,
                    count=batch_size, continuation_token=continuation_token
                )
                if not hasil:
                    break
                all_reviews.extend(hasil)
                status_placeholder.info(f"Sudah terkumpul {len(all_reviews):,} data...")
                if continuation_token is None:
                    break

        status_placeholder.empty()

        if not all_reviews:
            st.warning("Tidak ada data ulasan yang ditemukan untuk negara ini.")
        else:
            df_crawl = pd.DataFrame(all_reviews)[['reviewId', 'content', 'score', 'at']].copy()
            df_crawl.columns = ['review_id', 'review', 'rating', 'date']
            df_crawl = df_crawl.dropna(subset=['review'])
            df_crawl = df_crawl.drop_duplicates(subset=['review_id'])
            df_crawl['rating_bintang'] = df_crawl['rating'].apply(lambda x: "⭐" * int(x))
            df_crawl['negara'] = negara_pilihan
            df_crawl = df_crawl.reset_index(drop=True)

            st.success(f"✅ Berhasil mengambil {len(df_crawl):,} data dari {negara_pilihan}!")

            st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Ringkasan Hasil</div></div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Data", f"{len(df_crawl):,}")
            col2.metric("Rating 1-2 ⭐", f"{(df_crawl['rating'] <= 2).sum():,}")
            col3.metric("Rating 3 ⭐", f"{(df_crawl['rating'] == 3).sum():,}")
            col4.metric("Rating 4-5 ⭐", f"{(df_crawl['rating'] >= 4).sum():,}")

            st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Preview Data (20 Teratas)</div></div>', unsafe_allow_html=True)

            st.dataframe(
                df_crawl[['review', 'rating', 'rating_bintang', 'date', 'negara']].head(20),
                use_container_width=True, hide_index=True
            )

            st.session_state['df_crawl'] = df_crawl

            csv = df_crawl.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Hasil Crawling (CSV)", data=csv,
                file_name=f"steam_reviews_{negara_pilihan.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Gagal melakukan crawling: {e}")
