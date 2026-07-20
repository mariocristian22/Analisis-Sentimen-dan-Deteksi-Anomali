import streamlit as st
import pandas as pd
from utils import load_data, sentiment_from_text, sentiment_from_rating, detect_anomaly, detect_indikasi_anomali

st.set_page_config(page_title="Classification", page_icon="🧠", layout="wide")

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
.hero-desc {
    font-size: 15px; color: var(--text-dim);
    line-height: 1.7; max-width: 600px; margin-bottom: 28px;
}
.hero-stats { display: flex; gap: 24px; flex-wrap: wrap; }
.hero-stat { display: flex; flex-direction: column; gap: 2px; }
.hero-stat-value { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #f1f5f9; }
.hero-stat-label { font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.06em; }
.hero-icon { position: absolute; right: 56px; top: 50%; transform: translateY(-50%); font-size: 96px; opacity: 0.06; user-select: none; }

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
    padding: 10px 24px !important; font-weight: 600 !important;
    font-size: 14px !important;
}
.stButton > button:hover {
    background: #2563eb !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.4) !important;
}
.stDownloadButton > button {
    background: var(--green-soft) !important; color: var(--green) !important;
    border: 1px solid var(--green) !important; border-radius: 8px !important;
    font-weight: 600 !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
}
.stTextArea textarea {
    background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ── STAGE TRACKER ─────────────────────────────────────────
stages = ["Crawling", "Analisis Data", "Classification", "Report", "Dashboard", "Testing"]
nodes_html = ""
for i, s in enumerate(stages):
    active = (s == "Classification")
    done   = (i < stages.index("Classification"))
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
    <div class="hero-tag">🧠 Naive Bayes · TF-IDF</div>
    <div class="hero-title">Klasifikasi <span>Sentimen</span></div>
    <div class="hero-desc">
        Uji komentar secara manual atau upload file CSV untuk mengklasifikasikan
        sentimen dan mendeteksi anomali antara isi komentar dengan rating yang diberikan.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">Manual</div>
            <div class="hero-stat-label">Uji Komentar</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Batch</div>
            <div class="hero-stat-label">Upload CSV</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">Real-time</div>
            <div class="hero-stat-label">Hasil Analisis</div>
        </div>
    </div>
    <div class="hero-icon">🧠</div>
</div>
""", unsafe_allow_html=True)

# ── TAB ───────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Uji Manual", "Upload File CSV"])

with tab1:
    st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Uji Komentar Manual</div></div>', unsafe_allow_html=True)

    comment = st.text_area(
        "Masukkan komentar",
        placeholder="Contoh: aplikasi ini bagus sekali tapi rating saya kasih 1"
    )
    rating = st.selectbox("Pilih rating", [1, 2, 3, 4, 5], index=2)

    if st.button("Analisis Komentar"):
        if not comment.strip():
            st.warning("Silakan isi komentar terlebih dahulu.")
        else:
            sent_text        = sentiment_from_text(comment)
            sent_rating      = sentiment_from_rating(rating)
            anomaly          = detect_anomaly(comment, rating)
            indikasi_anomali = detect_indikasi_anomali(comment, rating)
            rating_bintang   = "⭐" * rating

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Hasil Analisis</div></div>', unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sentimen Teks",   sent_text)
            c2.metric("Sentimen Rating", sent_rating)
            c3.metric("Status Anomali",  anomaly)
            c4.metric("Indikasi",        indikasi_anomali)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Ringkasan Hasil</div></div>', unsafe_allow_html=True)

            st.write(f"**Komentar:** {comment}")
            st.write(f"**Rating:** {rating} ({rating_bintang})")

            if indikasi_anomali == "anomali":
                st.error("⚠️ Komentar ini terindikasi anomali karena isi komentar tidak sesuai dengan rating.")
            else:
                st.success("✅ Komentar ini tidak terindikasi anomali.")

with tab2:
    st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Upload File CSV</div></div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            df_upload.columns = [col.strip().lower() for col in df_upload.columns]

            if "content" in df_upload.columns and "review" not in df_upload.columns:
                df_upload = df_upload.rename(columns={"content": "review"})
            if "score" in df_upload.columns and "rating" not in df_upload.columns:
                df_upload = df_upload.rename(columns={"score": "rating"})

            if "review" not in df_upload.columns or "rating" not in df_upload.columns:
                st.error("File harus memiliki kolom 'review' dan 'rating'.")
            else:
                df_upload["review"]          = df_upload["review"].astype(str)
                df_upload["rating"]          = pd.to_numeric(df_upload["rating"], errors="coerce").fillna(3).astype(int)
                df_upload["rating_bintang"]  = df_upload["rating"].apply(lambda x: "⭐" * int(x))
                df_upload["sentiment_text"]  = df_upload["review"].apply(sentiment_from_text)
                df_upload["polarity"]        = df_upload["rating"].apply(sentiment_from_rating)
                df_upload["anomaly_status"]  = df_upload.apply(lambda row: detect_anomaly(row["review"], row["rating"]), axis=1)
                df_upload["indikasi_anomali"] = df_upload.apply(lambda row: detect_indikasi_anomali(row["review"], row["rating"]), axis=1)

                st.success("✅ File berhasil diproses.")

                st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">Preview Hasil Klasifikasi</div></div>', unsafe_allow_html=True)

                st.dataframe(
                    df_upload[["review", "rating", "rating_bintang", "sentiment_text", "polarity", "anomaly_status", "indikasi_anomali"]],
                    use_container_width=True, hide_index=True
                )

                csv_result = df_upload.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download Hasil Klasifikasi",
                    data=csv_result,
                    file_name="hasil_classification.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Gagal memproses file: {e}")
