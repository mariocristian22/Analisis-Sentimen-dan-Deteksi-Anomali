import streamlit as st
import pandas as pd
from utils import sentiment_from_rating, sentiment_from_text, detect_anomaly, detect_indikasi_anomali

st.set_page_config(page_title="Report", page_icon="📄", layout="wide")

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

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); }
.stApp { background: var(--bg); }
[data-testid="stSidebar"] { background: var(--bg-panel); border-right: 1px solid var(--border); }

.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1a2f4a 50%, #0f172a 100%);
    border: 1px solid var(--border); border-radius: 16px;
    padding: 48px 56px; margin-bottom: 32px;
    position: relative; overflow: hidden;
}
.hero-banner::before {
    content: ''; position: absolute; top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: ''; position: absolute; bottom: -30%; left: -5%;
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
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px; font-weight: 700; color: #f1f5f9;
    line-height: 1.2; margin-bottom: 14px;
}
.hero-title span {
    background: linear-gradient(90deg, #3b82f6, #10b981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-desc { font-size: 15px; color: var(--text-dim); line-height: 1.7; max-width: 600px; margin-bottom: 28px; }
.hero-stats { display: flex; gap: 24px; flex-wrap: wrap; }
.hero-stat { display: flex; flex-direction: column; gap: 2px; }
.hero-stat-value { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #f1f5f9; }
.hero-stat-label { font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.06em; }
.hero-icon { position: absolute; right: 56px; top: 50%; transform: translateY(-50%); font-size: 96px; opacity: 0.06; user-select: none; }

.section-header { display: flex; align-items: center; gap: 10px; margin: 28px 0 16px 0; }
.section-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
.section-title { font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 600; color: #f1f5f9; }
.divider { height: 1px; background: var(--border); margin: 24px 0; }

.insight-card {
    background: var(--bg-panel); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px 24px; margin-bottom: 10px;
    display: flex; gap: 14px; align-items: flex-start;
}
.insight-num {
    background: var(--accent-soft); color: #60a5fa;
    font-family: 'Space Grotesk', sans-serif; font-weight: 700;
    font-size: 14px; min-width: 28px; height: 28px;
    border-radius: 6px; display: flex; align-items: center; justify-content: center;
}
.insight-text { font-size: 14px; color: var(--text-dim); line-height: 1.6; }
.insight-text b { color: var(--text); }

[data-testid="stMetric"] { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 10px; padding: 16px 20px; }
[data-testid="stMetricLabel"] { color: var(--text-dim) !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-family: 'Space Grotesk', sans-serif !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── STAGE TRACKER ─────────────────────────────────────────
stages = ["Crawling", "Analisis Data", "Classification", "Report", "Dashboard", "Testing"]
nodes_html = ""
for i, s in enumerate(stages):
    active = (s == "Report")
    done   = (i < stages.index("Report"))
    bc     = "#3b82f6" if (active or done) else "#1f2d45"
    bg     = "#3b82f6" if done else ("transparent" if active else "#1f2d45")
    lc     = "#60a5fa" if active else ("#94a3b8" if done else "#475569")
    glow   = "box-shadow:0 0 8px #3b82f6;" if active else ""
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
    <div class="hero-tag">📄 Laporan Hasil Analisis</div>
    <div class="hero-title">Laporan <span>Penelitian</span></div>
    <div class="hero-desc">
        Ringkasan lengkap hasil analisis sentimen dan deteksi anomali ulasan pengguna
        aplikasi Steam, mencakup distribusi sentimen, rating bintang, dan insight penelitian.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">Sentimen</div>
            <div class="hero-stat-label">Distribusi</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Anomali</div>
            <div class="hero-stat-label">Deteksi</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Insight</div>
            <div class="hero-stat-label">Temuan</div>
        </div>
    </div>
    <div class="hero-icon">📄</div>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD FILE ───────────────────────────────────────────
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"], key="report_upload")

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
        df["anomaly_status"] = df.apply(lambda row: detect_anomaly(row["review"], row["rating"]), axis=1)
    if "indikasi_anomali" not in df.columns:
        df["indikasi_anomali"] = df.apply(lambda row: detect_indikasi_anomali(row["review"], row["rating"]), axis=1)
else:
    st.warning("Silakan pilih file CSV terlebih dahulu.")
    st.stop()

st.success("Data berhasil dimuat.")

# ── RINGKASAN UTAMA ───────────────────────────────────────
total_data    = len(df)
positif       = (df["polarity"] == "positif").sum()
netral        = (df["polarity"] == "netral").sum()
negatif       = (df["polarity"] == "negatif").sum()
anomali       = (df["indikasi_anomali"] == "anomali").sum()
bukan_anomali = (df["indikasi_anomali"] == "bukan_anomali").sum()

st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Ringkasan Hasil</div></div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Data",    f"{total_data:,}")
c2.metric("Positif",       f"{positif:,}")
c3.metric("Netral",        f"{netral:,}")
c4.metric("Negatif",       f"{negatif:,}")
c5.metric("Anomali",       f"{anomali:,}")
c6.metric("Bukan Anomali", f"{bukan_anomali:,}")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── DISTRIBUSI RATING ─────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Distribusi Rating Bintang</div></div>', unsafe_allow_html=True)

rating_summary = pd.DataFrame({
    "Bintang": ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    "Rating": [1, 2, 3, 4, 5],
    "Jumlah Review": [(df["rating"] == i).sum() for i in range(1, 6)],
    "Jumlah Anomali": [((df["rating"] == i) & (df["indikasi_anomali"] == "anomali")).sum() for i in range(1, 6)]
})
st.dataframe(rating_summary, use_container_width=True, hide_index=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── GRAFIK SENTIMEN ───────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Distribusi Sentimen</div></div>', unsafe_allow_html=True)
st.bar_chart(df["polarity"].value_counts())

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── GRAFIK ANOMALI ────────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Distribusi Indikasi Anomali</div></div>', unsafe_allow_html=True)
st.bar_chart(df["indikasi_anomali"].value_counts())

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── INSIGHT PENELITIAN ────────────────────────────────────
persen_anomali = round((anomali / total_data) * 100, 2) if total_data > 0 else 0

st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Insight Penelitian</div></div>', unsafe_allow_html=True)

insights = [
    f"Total data yang dianalisis sebanyak <b>{total_data:,}</b> review.",
    f"Review positif berjumlah <b>{positif:,}</b>, netral <b>{netral:,}</b>, dan negatif <b>{negatif:,}</b>.",
    f"Review yang terindikasi anomali sebanyak <b>{anomali:,}</b> data atau sekitar <b>{persen_anomali}%</b> dari total data.",
    "Indikasi anomali ditentukan berdasarkan ketidaksesuaian antara isi komentar dan rating bintang.",
    "Contoh: komentar positif tetapi rating 1 atau 2, atau komentar negatif tetapi rating 4 atau 5.",
]

for i, insight in enumerate(insights, 1):
    st.markdown(
        f'<div class="insight-card">'
        f'<div class="insight-num">{i}</div>'
        f'<div class="insight-text">{insight}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── CONTOH DATA ANOMALI ───────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Contoh Review yang Terindikasi Anomali</div></div>', unsafe_allow_html=True)

df_anomali = df[df["indikasi_anomali"] == "anomali"].copy()

if len(df_anomali) > 0:
    show_cols = [c for c in ["review", "rating", "rating_bintang", "sentiment_text", "polarity", "anomaly_status", "indikasi_anomali"] if c in df_anomali.columns]
    st.dataframe(df_anomali[show_cols].head(20), use_container_width=True, hide_index=True)
else:
    st.info("Belum ada data yang terindikasi anomali.")
