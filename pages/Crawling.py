import streamlit as st
import pandas as pd
from google_play_scraper import reviews, Sort

st.set_page_config(page_title="Crawling", page_icon="🔍", layout="wide")

# ============ TEMA "STEAM CONSOLE" (inline, tanpa import file lain) ============

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css');

    :root {
        --bg: #0d1117;
        --bg-panel: #161b22;
        --border: #2a3441;
        --text: #e6edf3;
        --text-dim: #8b98a5;
        --accent: #66c0f4;
        --accent-soft: rgba(102, 192, 244, 0.12);
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: var(--bg); color: var(--text); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
    [data-testid="stSidebar"] { background: var(--bg-panel); border-right: 1px solid var(--border); }
    [data-testid="stSidebarNav"] a { border-radius: 6px; margin: 2px 8px; color: var(--text-dim) !important; }
    [data-testid="stSidebarNav"] a:hover { background: var(--accent-soft); color: var(--text) !important; }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: var(--accent-soft); border-left: 3px solid var(--accent);
        color: var(--accent) !important; font-weight: 600;
    }
    .stButton > button, .stDownloadButton > button {
        background: transparent; border: 1px solid var(--accent); color: var(--accent);
        border-radius: 6px; font-weight: 600;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: var(--accent); color: var(--bg);
    }
    [data-testid="stMetric"] {
        background: var(--bg-panel); border: 1px solid var(--border);
        border-radius: 8px; padding: 14px 16px;
    }
    [data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
        color: var(--text) !important; border-radius: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def stage_tracker(current_stage: str):
    stages = ["Crawling", "Classification", "Testing", "Analisis Data", "Report", "Dashboard"]
    current_index = stages.index(current_stage) if current_stage in stages else 0
    nodes_html = ""
    for i, stage in enumerate(stages):
        if i < current_index:
            border_color, dot_bg, label_color, glow = "var(--accent)", "var(--accent)", "var(--text-dim)", ""
        elif i == current_index:
            border_color, dot_bg, label_color = "var(--accent)", "transparent", "var(--accent)"
            glow = "box-shadow: 0 0 10px var(--accent);"
        else:
            border_color, dot_bg, label_color, glow = "var(--border)", "var(--bg-panel)", "var(--text-dim)", ""
        nodes_html += f"""
        <div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:0;">
            <div style="width:14px;height:14px;border-radius:50%;border:2px solid {border_color};background:{dot_bg};{glow}"></div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.05em;text-transform:uppercase;color:{label_color};margin-top:6px;text-align:center;white-space:nowrap;">{i+1}. {stage}</div>
        </div>
        """
        if i < len(stages) - 1:
            line_color = "var(--accent)" if i < current_index else "var(--border)"
            nodes_html += f'<div style="flex:0.6;height:2px;background:{line_color};margin-top:7px;"></div>'
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;background:var(--bg-panel);border:1px solid var(--border);border-radius:10px;padding:16px 20px 12px 20px;margin-bottom:24px;">
        {nodes_html}
    </div>
    """, unsafe_allow_html=True)


def pixel_banner(eyebrow, title_html, badge, icon_class="ti-brand-steam", accent_icon="ti-search"):
    dots = "".join(f'<span class="pbdot d{(i % 4) + 1}"></span>' for i in range(32))
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    @keyframes pb-spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    @keyframes pb-blink {{ 0%, 100% {{ opacity: 0.55; }} 50% {{ opacity: 1; }} }}
    .pb-wrap {{
        background: #1c1440; border-radius: 0; padding: 40px 3rem; position: relative;
        overflow: hidden; margin: -6rem -1rem 24px -1rem; width: calc(100% + 2rem);
    }}
    .pb-dotgrid {{ position: absolute; top: 16px; left: 16px; display: grid; grid-template-columns: repeat(8, 10px); gap: 6px; }}
    .pbdot {{ width: 5px; height: 5px; border-radius: 50%; background: #8be89a; animation: pb-blink 2s ease-in-out infinite; }}
    .pbdot.d1 {{ animation-delay: 0s; }} .pbdot.d2 {{ animation-delay: 0.4s; }}
    .pbdot.d3 {{ animation-delay: 0.8s; }} .pbdot.d4 {{ animation-delay: 1.2s; }}
    .pb-stripe {{ display: inline-block; background: repeating-linear-gradient(45deg, #3fb6ad, #3fb6ad 4px, #1c1440 4px, #1c1440 8px); height: 10px; width: 150px; border-radius: 4px; margin-bottom: 14px; }}
    .pb-eyebrow {{ font-size: 13px; letter-spacing: 0.1em; color: #6fd1e8; text-transform: uppercase; margin-bottom: 6px; font-family: 'Inter', sans-serif; }}
    .pb-title {{ font-family: 'Press Start 2P', monospace; font-size: 28px; line-height: 1.5; color: #8be89a; text-shadow: 2px 2px 0 #12102c; }}
    .pb-badge {{ display: inline-block; margin-top: 18px; border: 2px solid #8be89a; color: #8be89a; font-family: 'Press Start 2P', monospace; font-size: 12px; padding: 8px 16px; border-radius: 2px; }}
    .pb-icon-main {{ position: absolute; right: 44px; top: 28px; font-size: 64px; color: #3b2f7a; animation: pb-spin 7s linear infinite; }}
    .pb-icon-accent {{ position: absolute; right: 158px; bottom: 34px; font-size: 32px; color: #3fb6ad; }}
    </style>
    <div class="pb-wrap">
        <div class="pb-dotgrid">{dots}</div>
        <div style="position:relative;z-index:2;">
            <div class="pb-stripe"></div>
            <div class="pb-eyebrow">{eyebrow}</div>
            <div class="pb-title">{title_html}</div>
            <div class="pb-badge">{badge}</div>
        </div>
        <i class="ti {icon_class} pb-icon-main"></i>
        <i class="ti {accent_icon} pb-icon-accent"></i>
    </div>
    """, unsafe_allow_html=True)


# ============ HALAMAN CRAWLING ============

apply_theme()
stage_tracker("Crawling")
pixel_banner(
    eyebrow="Kumpulkan data ulasan",
    title_html="Crawling<br>Data",
    badge="Mulai crawling !",
    icon_class="ti-brand-steam",
    accent_icon="ti-search",
)

st.write("Halaman ini digunakan untuk mengambil data ulasan aplikasi Steam langsung dari Google Play Store.")

APP_ID = 'com.valvesoftware.android.steam.community'

st.subheader("Konfigurasi Crawling")

urutan = st.selectbox("Urutkan berdasarkan", ["Terbaru", "Relevansi"], index=0)

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

if st.button("🚀 Mulai Crawling"):
    status_placeholder = st.empty()
    all_reviews = []
    continuation_token = None
    batch_size = 200

    try:
        with st.spinner(f"Sedang mengambil data sebanyak-banyaknya dari {negara_pilihan}..."):
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

            st.success(f"✅ Berhasil mengambil {len(df_crawl):,} data dari {negara_pilihan} (seluruh data yang tersedia)!")

            st.subheader("Preview Data")
            st.dataframe(
                df_crawl[['review', 'rating', 'rating_bintang', 'date', 'negara']].head(20),
                use_container_width=True, hide_index=True
            )

            st.subheader("Ringkasan")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Data", len(df_crawl))
            col2.metric("Rating 1-2 ⭐", (df_crawl['rating'] <= 2).sum())
            col3.metric("Rating 3 ⭐", (df_crawl['rating'] == 3).sum())
            col4.metric("Rating 4-5 ⭐", (df_crawl['rating'] >= 4).sum())

            st.session_state['df_crawl'] = df_crawl

            csv = df_crawl.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Hasil Crawling (CSV)", data=csv,
                file_name=f"steam_reviews_{negara_pilihan.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Gagal melakukan crawling: {e}")