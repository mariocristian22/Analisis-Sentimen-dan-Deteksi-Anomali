import streamlit as st
import pandas as pd
from utils import sentiment_from_rating, sentiment_from_text, detect_anomaly, detect_indikasi_anomali
 
st.set_page_config(page_title="Report", page_icon="📄", layout="wide")
 
st.title("Report")
st.write("Halaman ini menampilkan ringkasan hasil analisis sentimen dan deteksi anomali.")
 
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
        df["anomaly_status"] = df.apply(
            lambda row: detect_anomaly(row["review"], row["rating"]), axis=1
        )
 
    if "indikasi_anomali" not in df.columns:
        df["indikasi_anomali"] = df.apply(
            lambda row: detect_indikasi_anomali(row["review"], row["rating"]), axis=1
        )
else:
    st.warning("Silakan pilih file CSV terlebih dahulu.")
    st.stop()
 
st.success("Data berhasil dimuat.")
 
# Ringkasan utama
total_data = len(df)
positif = (df["polarity"] == "positif").sum()
netral = (df["polarity"] == "netral").sum()
negatif = (df["polarity"] == "negatif").sum()
anomali = (df["indikasi_anomali"] == "anomali").sum()
bukan_anomali = (df["indikasi_anomali"] == "bukan_anomali").sum()
 
st.subheader("Ringkasan Hasil")
 
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Data", total_data)
c2.metric("Positif", positif)
c3.metric("Netral", netral)
c4.metric("Negatif", negatif)
c5.metric("Anomali", anomali)
c6.metric("Bukan Anomali", bukan_anomali)
 
# Distribusi rating
st.subheader("Distribusi Rating Bintang")
 
rating_summary = pd.DataFrame({
    "Bintang": ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    "Rating": [1, 2, 3, 4, 5],
    "Jumlah Review": [
        (df["rating"] == 1).sum(),
        (df["rating"] == 2).sum(),
        (df["rating"] == 3).sum(),
        (df["rating"] == 4).sum(),
        (df["rating"] == 5).sum()
    ],
    "Jumlah Anomali": [
        ((df["rating"] == 1) & (df["indikasi_anomali"] == "anomali")).sum(),
        ((df["rating"] == 2) & (df["indikasi_anomali"] == "anomali")).sum(),
        ((df["rating"] == 3) & (df["indikasi_anomali"] == "anomali")).sum(),
        ((df["rating"] == 4) & (df["indikasi_anomali"] == "anomali")).sum(),
        ((df["rating"] == 5) & (df["indikasi_anomali"] == "anomali")).sum()
    ]
})
 
st.dataframe(rating_summary, use_container_width=True, hide_index=True)
 
# Grafik sentimen
st.subheader("Distribusi Sentimen")
st.bar_chart(df["polarity"].value_counts())
 
# Grafik anomali
st.subheader("Distribusi Indikasi Anomali")
st.bar_chart(df["indikasi_anomali"].value_counts())
 
# Insight sederhana
st.subheader("Insight Penelitian")
 
persen_anomali = round((anomali / total_data) * 100, 2) if total_data > 0 else 0
 
st.write(f"1. Total data yang dianalisis sebanyak **{total_data}** review.")
st.write(f"2. Review positif berjumlah **{positif}**, netral **{netral}**, dan negatif **{negatif}**.")
st.write(f"3. Review yang terindikasi anomali sebanyak **{anomali}** data atau sekitar **{persen_anomali}%** dari total data.")
st.write("4. Indikasi anomali ditentukan berdasarkan ketidaksesuaian antara isi komentar dan rating bintang.")
st.write("5. Contoh: komentar positif tetapi rating 1 atau 2, atau komentar negatif tetapi rating 4 atau 5.")
 
# Contoh data anomali
st.subheader("Contoh Review yang Terindikasi Anomali")
 
df_anomali = df[df["indikasi_anomali"] == "anomali"].copy()
 
if len(df_anomali) > 0:
    show_cols = [c for c in [
        "review",
        "rating",
        "rating_bintang",
        "sentiment_text",
        "polarity",
        "anomaly_status",
        "indikasi_anomali"
    ] if c in df_anomali.columns]
 
    st.dataframe(
        df_anomali[show_cols].head(20),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Belum ada data yang terindikasi anomali.")
