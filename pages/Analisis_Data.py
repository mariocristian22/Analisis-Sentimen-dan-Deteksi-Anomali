import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from utils import sentiment_from_rating, sentiment_from_text, detect_anomaly

st.set_page_config(page_title="Analisis Data", page_icon="📈", layout="wide")

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
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%; left: -5%;
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
.hero-desc {
    font-size: 15px; color: var(--text-dim);
    line-height: 1.7; max-width: 600px; margin-bottom: 28px;
}
.hero-stats { display: flex; gap: 24px; flex-wrap: wrap; }
.hero-stat { display: flex; flex-direction: column; gap: 2px; }
.hero-stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px; font-weight: 700; color: #f1f5f9;
}
.hero-stat-label {
    font-size: 12px; color: var(--text-dim);
    text-transform: uppercase; letter-spacing: 0.06em;
}
.hero-icon {
    position: absolute; right: 56px; top: 50%;
    transform: translateY(-50%);
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
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ── STAGE TRACKER ─────────────────────────────────────────
stages = ["Crawling", "Analisis Data", "Classification", "Report", "Dashboard", "Testing"]
nodes_html = ""
for i, s in enumerate(stages):
    active = (s == "Analisis Data")
    done   = (i < stages.index("Analisis Data"))
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
    <div class="hero-tag">📊 Visualisasi & Eksplorasi Data</div>
    <div class="hero-title">Analisis <span>Data Ulasan</span></div>
    <div class="hero-desc">
        Eksplorasi distribusi sentimen, rating bintang, word cloud, dan confusion matrix
        dari data ulasan pengguna aplikasi Steam yang telah dikumpulkan.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">Pie Chart</div>
            <div class="hero-stat-label">Distribusi Sentimen</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Word Cloud</div>
            <div class="hero-stat-label">Kata Dominan</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Confusion Matrix</div>
            <div class="hero-stat-label">Evaluasi Model</div>
        </div>
    </div>
    <div class="hero-icon">📈</div>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD FILE ───────────────────────────────────────────
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"], key="analisis_upload")

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

    df["review"]       = df["review"].astype(str)
    df["rating"]       = pd.to_numeric(df["rating"], errors="coerce").fillna(3).astype(int)

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

# ── RINGKASAN SENTIMEN ────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Ringkasan Sentimen</div></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Positif",  f"{(df['polarity'] == 'positif').sum():,}")
c2.metric("Netral",   f"{(df['polarity'] == 'netral').sum():,}")
c3.metric("Negatif",  f"{(df['polarity'] == 'negatif').sum():,}")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── DISTRIBUSI RATING ─────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Distribusi Rating</div></div>', unsafe_allow_html=True)
r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("⭐ 1",     f"{(df['rating'] == 1).sum():,}")
r2.metric("⭐⭐ 2",   f"{(df['rating'] == 2).sum():,}")
r3.metric("⭐⭐⭐ 3", f"{(df['rating'] == 3).sum():,}")
r4.metric("⭐⭐⭐⭐ 4", f"{(df['rating'] == 4).sum():,}")
r5.metric("⭐⭐⭐⭐⭐ 5", f"{(df['rating'] == 5).sum():,}")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── PIE CHART SENTIMEN ────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Distribusi Sentimen</div></div>', unsafe_allow_html=True)

sentiment_counts = df["polarity"].value_counts()
fig1, ax1 = plt.subplots(figsize=(7, 5))
fig1.patch.set_facecolor('#111827')
ax1.set_facecolor('#111827')
colors = ['#3b82f6', '#10b981', '#f59e0b']
ax1.pie(
    sentiment_counts.values,
    labels=sentiment_counts.index.tolist(),
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.05] * len(sentiment_counts),
    colors=colors[:len(sentiment_counts)],
    textprops={'color': '#e2e8f0'}
)
ax1.set_title("Sentiment Distribution of Steam App Reviews", color='#e2e8f0', pad=16)
st.pyplot(fig1)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── CONFUSION MATRIX ──────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Confusion Matrix</div></div>', unsafe_allow_html=True)

if "polarity" in df.columns and "sentiment_text" in df.columns:
    valid_df = df[
        df["polarity"].isin(["positif", "netral", "negatif"]) &
        df["sentiment_text"].isin(["positif", "netral", "negatif"])
    ].copy()

    if len(valid_df) > 0:
        labels_cm = ["positif", "netral", "negatif"]
        cm = confusion_matrix(valid_df["polarity"], valid_df["sentiment_text"], labels=labels_cm)
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        fig2.patch.set_facecolor('#111827')
        ax2.set_facecolor('#111827')
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels_cm)
        disp.plot(ax=ax2, cmap="Blues", colorbar=True)
        ax2.set_title("Confusion Matrix of Steam App Sentiment Classification", color='#e2e8f0', pad=16)
        ax2.tick_params(colors='#e2e8f0')
        ax2.xaxis.label.set_color('#e2e8f0')
        ax2.yaxis.label.set_color('#e2e8f0')
        st.pyplot(fig2)
    else:
        st.info("Data untuk confusion matrix belum valid.")
else:
    st.info("Kolom 'polarity' dan 'sentiment_text' belum tersedia.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── WORD CLOUD ────────────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Word Cloud</div></div>', unsafe_allow_html=True)

text_source = " ".join(df["text_final"].dropna().astype(str)) if "text_final" in df.columns else " ".join(df["review"].dropna().astype(str))

if text_source.strip():
    wc = WordCloud(width=1200, height=500, background_color="#111827", colormap="Blues").generate(text_source)
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    fig3.patch.set_facecolor('#111827')
    ax3.imshow(wc, interpolation="bilinear")
    ax3.axis("off")
    ax3.set_title("Word Cloud of Steam App Reviews", color='#e2e8f0', pad=16)
    st.pyplot(fig3)
else:
    st.info("Tidak ada teks untuk word cloud.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── GRAFIK ANOMALI ────────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Distribusi Status Anomali</div></div>', unsafe_allow_html=True)
st.bar_chart(df["anomaly_status"].value_counts())

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── TABEL DATA ────────────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Tabel Data Review</div></div>', unsafe_allow_html=True)

show_cols = [c for c in ["review", "rating", "rating_bintang", "polarity", "sentiment_text", "anomaly_status"] if c in df.columns]
st.dataframe(df[show_cols].head(50), use_container_width=True, hide_index=True)
