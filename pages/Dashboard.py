 import streamlit as st
import pandas as pd
from utils import sentiment_from_rating, sentiment_from_text, detect_anomaly

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

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
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
}
[data-testid="stFileUploader"] {
    background: var(--bg-panel); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── STAGE TRACKER ─────────────────────────────────────────
stages = ["Crawling", "Analisis Data", "Classification", "Report", "Dashboard", "Testing"]
nodes_html = ""
current_index = stages.index("Dashboard")
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
    <div class="hero-tag">📊 Ringkasan Data</div>
    <div class="hero-title">Dashboard <span>Analisis Sentimen</span></div>
    <div class="hero-desc">
        Analisis Sentimen dan Deteksi Anomali pada Review Steam. Halaman ini menampilkan
        ringkasan dataset review Steam, distribusi sentimen, distribusi rating bintang,
        dan jumlah review yang terindikasi anomali.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">Sentimen</div>
            <div class="hero-stat-label">Ringkasan</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Rating</div>
            <div class="hero-stat-label">Distribusi</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Anomali</div>
            <div class="hero-stat-label">Deteksi</div>
        </div>
    </div>
    <div class="hero-icon">📊</div>
</div>
""", unsafe_allow_html=True)

st.caption("by Mario Cristian Simatupang")

uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = [col.strip().lower() for col in df.columns]

    if "content" in df.columns and "review" not in df.columns:
        df = df.rename(columns={"content": "review"})
    if "score" in df.columns and "rating" not in df.columns:
        df = df.rename(columns={"score": "rating"})

    if "review" not in df.columns or "rating" not in df.columns:
        st.error("File harus memiliki kolom 'review' dan 'rating'.")
        st.stop()

    df["review"] = df["review"].astype(str)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(3).astype(int)

    if "rating_bintang" not in df.columns:
        df["rating_bintang"] = df["rating"].apply(lambda x: "⭐" * int(x))

    if "polarity" not in df.columns:
        df["polarity"] = df["rating"].apply(sentiment_from_rating)

    if "sentiment_text" not in df.columns:
        df["sentiment_text"] = df["review"].apply(sentiment_from_text)

    if "anomaly_status" not in df.columns:
        df["anomaly_status"] = df.apply(
            lambda row: detect_anomaly(row["review"], row["rating"]), axis=1
        )

else:
    st.warning("Silakan pilih file CSV terlebih dahulu.")
    st.stop()

st.success("Data berhasil dimuat.")

total_data = len(df)
positif  = (df["polarity"] == "positif").sum()
netral   = (df["polarity"] == "netral").sum()
negatif  = (df["polarity"] == "negatif").sum()
anomali  = (df["anomaly_status"] == "anomali").sum()
normal   = (df["anomaly_status"] == "normal").sum()

st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Ringkasan Data</div></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Data", f"{total_data:,}")
col2.metric("Positif", f"{positif:,}")
col3.metric("Netral", f"{netral:,}")
col4.metric("Negatif", f"{negatif:,}")
col5.metric("Anomali", f"{anomali:,}")
col6.metric("Normal", f"{normal:,}")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Distribusi Rating Bintang</div></div>', unsafe_allow_html=True)

b1 = (df["rating"] == 1).sum()
b2 = (df["rating"] == 2).sum()
b3 = (df["rating"] == 3).sum()
b4 = (df["rating"] == 4).sum()
b5 = (df["rating"] == 5).sum()

r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("⭐ 1", f"{b1:,}")
r2.metric("⭐⭐ 2", f"{b2:,}")
r3.metric("⭐⭐⭐ 3", f"{b3:,}")
r4.metric("⭐⭐⭐⭐ 4", f"{b4:,}")
r5.metric("⭐⭐⭐⭐⭐ 5", f"{b5:,}")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Contoh Review Anomali</div></div>', unsafe_allow_html=True)

anomali_df = df[df["anomaly_status"] == "anomali"].copy()

show_cols = [c for c in [
    "review", "rating", "rating_bintang", "polarity",
    "sentiment_text", "anomaly_status"
] if c in anomali_df.columns]

if len(anomali_df) > 0:
    st.dataframe(anomali_df[show_cols].head(20), use_container_width=True, hide_index=True)
else:
    st.info("Belum ada data yang terindikasi anomali.")
