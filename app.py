import streamlit as st
import streamlit.components.v1 as components
 
st.set_page_config(
    page_title="Analisis Sentimen dan Deteksi Anomali",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
dashboard_page = st.Page("pages/Dashboard.py", title="Dashboard", icon="📊")
analisis_page = st.Page("pages/Analisis_Data.py", title="Analisis Data", icon="📈")
classification_page = st.Page("pages/Classification.py", title="Classification", icon="🧠")
report_page = st.Page("pages/Report.py", title="Report", icon="📄")
testing_page = st.Page("pages/Testing.py", title="Testing", icon="🧪")
 
pg = st.navigation(
    [
        dashboard_page,
        analisis_page,
        classification_page,
        report_page,
        testing_page,
    ],
    position="sidebar"
)
 
if "started" not in st.session_state:
    st.session_state.started = False
 
# Tombol "Mulai Sekarang" di dalam hero (HTML) akan menambahkan
# ?started=true ke URL, lalu kita baca lewat query params di sini.
if st.query_params.get("started") == "true":
    st.session_state.started = True
 
if not st.session_state.started:
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
 
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
 
    iframe {
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
 
    landing_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html, body {
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #0f3460, #16537e, #1f6aa5);
        min-height: 100vh;
    }
 
    .topbar {
        background: rgba(0,0,0,0.18);
        padding: 18px 30px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 700;
        font-size: 20px;
    }
 
    .hero {
        padding: 55px 40px 55px 40px;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
 
    @keyframes floatUpDown {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-12px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
 
    @keyframes glowPulse {
        0% { opacity: 0.10; transform: scale(1); }
        50% { opacity: 0.20; transform: scale(1.08); }
        100% { opacity: 0.10; transform: scale(1); }
    }
 
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(28px); }
        to { opacity: 1; transform: translateY(0); }
    }
 
    .hero-center {
        text-align: center;
        position: relative;
        z-index: 2;
        animation: fadeInUp 1s ease-out;
        padding: 0 12px;
    }
 
    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.14);
        color: #ffffff;
        padding: 10px 24px;
        border-radius: 999px;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 18px;
    }
 
    .hero-title {
        font-size: 64px;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.12;
        margin-bottom: 12px;
    }
 
    .hero-subtitle {
        font-size: 26px;
        font-weight: 700;
        color: #dbeeff;
        margin-bottom: 18px;
    }
 
    .hero-desc {
        max-width: 980px;
        margin: 0 auto 18px auto;
        font-size: 20px;
        color: #eef7ff;
        line-height: 1.9;
    }
 
    .hero-desc-2 {
        max-width: 980px;
        margin: 0 auto 30px auto;
        font-size: 18px;
        color: #d8ecff;
        line-height: 1.8;
    }
 
    .cta-button {
        display: inline-block;
        background: #ffffff;
        color: #1b4f82;
        border: none;
        border-radius: 16px;
        padding: 14px 40px;
        font-size: 20px;
        font-family: Arial, sans-serif;
        font-weight: 800;
        text-decoration: none;
        box-shadow: 0 10px 25px rgba(0,0,0,0.20);
        transition: background 0.15s ease, transform 0.1s ease;
        cursor: pointer;
        outline: none;
    }
 
    .cta-button:hover {
        background: #dfefff;
        color: #163a63;
        transform: translateY(-2px);
    }
 
    .steam-left, .steam-right, .steam-small-1, .steam-small-2 {
        position: absolute;
        z-index: 1;
        user-select: none;
        pointer-events: none;
    }
 
    .steam-left {
        left: 55px; top: 145px;
        font-size: 120px; opacity: 0.10;
        animation: floatUpDown 5s ease-in-out infinite;
    }
 
    .steam-right {
        right: 55px; bottom: 85px;
        font-size: 130px; opacity: 0.10;
        animation: floatUpDown 6s ease-in-out infinite;
    }
 
    .steam-small-1 {
        left: 165px; bottom: 70px;
        font-size: 55px; opacity: 0.14;
        animation: glowPulse 4.2s ease-in-out infinite;
    }
 
    .steam-small-2 {
        right: 165px; top: 130px;
        font-size: 55px; opacity: 0.14;
        animation: glowPulse 4.8s ease-in-out infinite;
    }
 
    .circle-1, .circle-2 {
        position: absolute;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        z-index: 1;
        animation: glowPulse 5s ease-in-out infinite;
    }
 
    .circle-1 { width: 220px; height: 220px; top: -60px; left: -50px; }
    .circle-2 { width: 280px; height: 280px; right: -80px; bottom: -90px; }
 
    /* Responsive: layar sedang (tablet) */
    @media (max-width: 1024px) {
        .hero-title { font-size: 46px; }
        .hero-subtitle { font-size: 22px; }
        .hero-desc { font-size: 17px; line-height: 1.7; }
        .hero-desc-2 { font-size: 15px; line-height: 1.6; margin-bottom: 20px; }
        .hero { padding: 40px 24px; }
    }
 
    /* Responsive: HP */
    @media (max-width: 600px) {
        .topbar { font-size: 15px; padding: 12px 18px; }
        .badge { font-size: 13px; padding: 7px 16px; }
        .hero-title { font-size: 28px; line-height: 1.2; }
        .hero-subtitle { font-size: 15px; margin-bottom: 12px; }
        .hero-desc { font-size: 13px; line-height: 1.6; margin-bottom: 10px; }
        .hero-desc-2 { font-size: 12px; line-height: 1.5; margin-bottom: 18px; }
        .hero { padding: 24px 16px; }
        .cta-button { padding: 12px 30px; font-size: 16px; }
        .steam-left, .steam-right, .steam-small-1, .steam-small-2 { display: none; }
    }
    </style>
    </head>
    <body>
        <div class="topbar">
            <div>🎮 Steam Review Analyzer</div>
            <div>🔵</div>
        </div>
 
        <div class="hero">
            <div class="circle-1"></div>
            <div class="circle-2"></div>
            <div class="steam-left">🎮</div>
            <div class="steam-right">🎮</div>
            <div class="steam-small-1">🎮</div>
            <div class="steam-small-2">🎮</div>
 
            <div class="hero-center">
                <div class="badge">Steam Review Intelligence</div>
                <div class="hero-title">Analisis Sentimen dan<br>Deteksi Anomali</div>
                <div class="hero-subtitle">Pada Aplikasi Steam</div>
                <div class="hero-desc">
                    Sistem ini dirancang untuk menganalisis sentimen ulasan pengguna pada aplikasi Steam
                    serta mendeteksi anomali berdasarkan ketidaksesuaian antara isi komentar
                    dengan rating bintang yang diberikan.
                </div>
                <div class="hero-desc-2">
                    Melalui aplikasi ini, pengguna dapat melihat distribusi sentimen, distribusi rating,
                    hasil deteksi anomali, melakukan pengujian komentar secara manual, serta membaca
                    ringkasan hasil analisis dalam bentuk dashboard dan visualisasi data yang interaktif.
                </div>
                <button type="button" class="cta-button" onclick="
                    try {
                        var topLoc = window.top.location;
                        topLoc.href = topLoc.origin + topLoc.pathname + '?started=true';
                    } catch (e) {
                        window.location.href = '?started=true';
                    }
                ">Mulai Sekarang</button>
            </div>
        </div>
    </body>
    </html>
    """
 
    components.html(landing_html, height=760, scrolling=False)
 
else:
    pg.run()