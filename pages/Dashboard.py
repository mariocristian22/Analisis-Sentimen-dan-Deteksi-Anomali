import streamlit as st
import pandas as pd
from utils import sentiment_from_rating, sentiment_from_text, detect_anomaly

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("Analisis Sentimen")
st.caption("by Mario Cristian Simatupang")

st.header("Analisis Sentimen dan Deteksi Anomali pada Review Steam")
st.write(
    "Halaman ini menampilkan ringkasan dataset review Steam, distribusi sentimen, "
    "distribusi rating bintang, dan jumlah review yang terindikasi anomali."
)

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

total_data = len(df)
positif  = (df["polarity"] == "positif").sum()
netral   = (df["polarity"] == "netral").sum()
negatif  = (df["polarity"] == "negatif").sum()
anomali  = (df["anomaly_status"] == "anomali").sum()
normal   = (df["anomaly_status"] == "normal").sum()

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Data", total_data)
col2.metric("Positif", positif)
col3.metric("Netral", netral)
col4.metric("Negatif", negatif)
col5.metric("Anomali", anomali)
col6.metric("Normal", normal)

st.subheader("Distribusi Rating Bintang")

b1 = (df["rating"] == 1).sum()
b2 = (df["rating"] == 2).sum()
b3 = (df["rating"] == 3).sum()
b4 = (df["rating"] == 4).sum()
b5 = (df["rating"] == 5).sum()

r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("⭐ 1", b1)
r2.metric("⭐⭐ 2", b2)
r3.metric("⭐⭐⭐ 3", b3)
r4.metric("⭐⭐⭐⭐ 4", b4)
r5.metric("⭐⭐⭐⭐⭐ 5", b5)

st.subheader("Contoh Review Anomali")
anomali_df = df[df["anomaly_status"] == "anomali"].copy()

show_cols = [c for c in [
    "review", "rating", "rating_bintang", "polarity",
    "sentiment_text", "anomaly_status"
] if c in anomali_df.columns]

if len(anomali_df) > 0:
    st.dataframe(anomali_df[show_cols].head(20), use_container_width=True, hide_index=True)
else:
    st.info("Belum ada data yang terindikasi anomali.")
