import streamlit as st
import pandas as pd
from utils import (
    sentiment_from_rating,
    sentiment_from_text,
    detect_anomaly,
    detect_indikasi_anomali
)

st.set_page_config(page_title="Testing", page_icon="🧪", layout="wide")

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
    --red: #ef4444;
    --red-soft: rgba(239, 68, 68, 0.1);
    --amber: #f59e0b;
    --amber-soft: rgba(245, 158, 11, 0.1);
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
    position: absolute; top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute; bottom: -30%; left: -5%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--accent-soft); border: 1px solid rgba(59,130,246,0.3);
    color: #60a5fa; padding: 6px 14px; border-radius: 999px;
    font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; margin-bottom: 20px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif; font-size: 42px; font-weight: 700;
    color: #f1f5f9; line-height: 1.2; margin-bottom: 14px;
}
.hero-title span {
    background: linear-gradient(90deg, #3b82f6, #10b981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-desc {
    font-size: 15px; color: var(--text-dim); line-height: 1.7;
    max-width: 600px; margin-bottom: 28px;
}
.hero-stats { display: flex; gap: 24px; flex-wrap: wrap; }
.hero-stat { display: flex; flex-direction: column; gap: 2px; }
.hero-stat-value { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #f1f5f9; }
.hero-stat-label { font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.06em; }
.hero-icon {
    position: absolute; right: 56px; top: 50%; transform: translateY(-50%);
    font-size: 96px; opacity: 0.06; user-select: none;
}

.section-header { display: flex; align-items: center; gap: 10px; margin: 28px 0 16px 0; }
.section-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
.section-title { font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 600; color: #f1f5f9; }
.divider { height: 1px; background: var(--border); margin: 24px 0; }

[data-testid="stMetric"] {
    background: var(--bg-panel); border: 1px solid var(--border);
    border-radius: 10px; padding: 16px 20px;
}
[data-testid="stMetricLabel"] { color: var(--text-dim) !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-family: 'Space Grotesk', sans-serif !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }

.stButton > button {
    background: var(--accent) !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    padding: 10px 24px !important; font-weight: 600 !important; font-size: 14px !important;
}
.stButton > button:hover {
    background: #2563eb !important; box-shadow: 0 4px 12px rgba(59,130,246,0.4) !important;
}
.stDownloadButton > button {
    background: var(--green-soft) !important; color: var(--green) !important;
    border: 1px solid var(--green) !important; border-radius: 8px !important; font-weight: 600 !important;
}
.stTextArea textarea {
    background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ── STAGE TRACKER ─────────────────────────────────────────
stages = ["Crawling", "Analisis Data", "Classification", "Report", "Dashboard", "Testing"]
current_index = stages.index("Testing")
nodes_html = ""
for i, s in enumerate(stages):
    active = (i == current_index)
    done = (i < current_index)
    bc = "#3b82f6" if (active or done) else "#1f2d45"
    bg = "#3b82f6" if done else ("transparent" if active else "#1f2d45")
    lc = "#60a5fa" if active else ("#94a3b8" if done else "#475569")
    glow = "box-shadow:0 0 8px #3b82f6;" if active else ""
    nodes_html += (
        f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:0;">'
        f'<div style="width:12px;height:12px;border-radius:50%;border:2px solid {bc};background:{bg};{glow}"></div>'
        f'<div style="font-size:10px;color:{lc};margin-top:6px;text-align:center;font-weight:{"600" if active else "400"};white-space:nowrap;">{i+1}. {s}</div>'
        f'</div>'
    )
    if i < len(stages) - 1:
        lc2 = "#3b82f6" if done else "#1f2d45"
        nodes_html += f'<div style="flex:0.6;height:1px;background:{lc2};margin-top:6px;"></div>'

st.markdown(
    f'<div style="background:#111827;border:1px solid #1f2d45;border-radius:12px;padding:14px 24px;'
    f'margin-bottom:24px;display:flex;align-items:flex-start;">{nodes_html}</div>',
    unsafe_allow_html=True
)

# ── HERO BANNER ───────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">🧪 Uji Coba Manual</div>
    <div class="hero-title">Testing <span>Sentimen &amp; Anomali</span></div>
    <div class="hero-desc">
        Masukkan komentar dan rating untuk melihat hasil sentimen, status anomali,
        dan indikasi anomali secara langsung. Setiap pengujian akan tersimpan
        di riwayat pengujian.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">Real-time</div>
            <div class="hero-stat-label">Hasil Analisis</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Otomatis</div>
            <div class="hero-stat-label">Tersimpan di Riwayat</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">CSV</div>
            <div class="hero-stat-label">Ekspor Riwayat</div>
        </div>
    </div>
    <div class="hero-icon">🧪</div>
</div>
""", unsafe_allow_html=True)

# Inisialisasi history
if "test_history" not in st.session_state:
    st.session_state.test_history = []

st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Uji Komentar</div></div>', unsafe_allow_html=True)

comment = st.text_area(
    "Masukkan kalimat / komentar:",
    placeholder="Contoh: aplikasi ini bagus banget tapi saya kasih bintang 1"
)

rating = st.selectbox("Pilih rating", [1, 2, 3, 4, 5], index=2)

if st.button("Uji Sentimen"):
    if not comment.strip():
        st.warning("Silakan isi komentar terlebih dahulu.")
    else:
        sent_text = sentiment_from_text(comment)
        sent_rating = sentiment_from_rating(rating)
        anomaly = detect_anomaly(comment, rating)
        indikasi_anomali = detect_indikasi_anomali(comment, rating)
        rating_bintang = "⭐" * rating

        if indikasi_anomali == "anomali":
            alasan = (
                "Komentar terindikasi anomali karena isi komentar tidak sesuai dengan rating. "
                "Contohnya komentar positif tetapi diberi rating rendah, atau komentar negatif "
                "tetapi diberi rating tinggi."
            )
        elif anomaly == "perlu_tinjauan":
            alasan = (
                "Komentar ini masih perlu ditinjau karena sentimennya cenderung netral "
                "atau belum cukup kuat untuk dinilai anomali."
            )
        else:
            alasan = (
                "Komentar ini tidak terindikasi anomali karena isi komentar masih sesuai "
                "dengan rating yang diberikan."
            )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Hasil Analisis</div></div>', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Rating", rating)
        c2.metric("Bintang", rating_bintang)
        c3.metric("Sentimen Teks", sent_text)
        c4.metric("Sentimen Rating", sent_rating)
        c5.metric("Indikasi Anomali", indikasi_anomali)

        c6, c7 = st.columns(2)
        c6.metric("Status Anomali", anomaly)
        c7.metric("Jumlah Karakter", len(comment))

        if indikasi_anomali == "anomali":
            st.error(f"Hasil akhir: {indikasi_anomali.upper()}")
        elif anomaly == "perlu_tinjauan":
            st.warning("Hasil akhir: PERLU TINJAUAN")
        else:
            st.success("Hasil akhir: BUKAN_ANOMALI")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Penjelasan</div></div>', unsafe_allow_html=True)
        st.write(alasan)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Detail Uji</div></div>', unsafe_allow_html=True)
        detail_df = pd.DataFrame({
            "Komponen": [
                "Komentar",
                "Rating Angka",
                "Rating Bintang",
                "Sentimen Teks",
                "Sentimen Rating",
                "Status Anomali",
                "Indikasi Anomali"
            ],
            "Hasil": [
                comment,
                rating,
                rating_bintang,
                sent_text,
                sent_rating,
                anomaly,
                indikasi_anomali
            ]
        })
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

        st.session_state.test_history.insert(0, {
            "komentar": comment,
            "rating": rating,
            "bintang": rating_bintang,
            "sentimen_teks": sent_text,
            "sentimen_rating": sent_rating,
            "anomali": anomaly,
            "indikasi_anomali": indikasi_anomali
        })

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Riwayat Pengujian</div></div>', unsafe_allow_html=True)

if len(st.session_state.test_history) > 0:
    history_df = pd.DataFrame(st.session_state.test_history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

    csv_history = history_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Riwayat Pengujian",
        data=csv_history,
        file_name="riwayat_testing_sentimen_anomali.csv",
        mime="text/csv"
    )

    if st.button("Hapus Riwayat"):
        st.session_state.test_history = []
        st.rerun()
else:
    st.info("Belum ada riwayat pengujian.")
