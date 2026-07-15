import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from utils import sentiment_from_rating, sentiment_from_text, detect_anomaly, detect_indikasi_anomali

st.set_page_config(page_title="Analisis Data", page_icon="📈", layout="wide")

st.title("Analisis Data")
st.write("Halaman ini digunakan untuk melihat distribusi sentimen, rating, word cloud, confusion matrix, dan tabel data review.")

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

# =========================
# RINGKASAN SENTIMEN
# =========================
st.subheader("Ringkasan Sentimen")
c1, c2, c3 = st.columns(3)
c1.metric("Positif", (df["polarity"] == "positif").sum())
c2.metric("Netral", (df["polarity"] == "netral").sum())
c3.metric("Negatif", (df["polarity"] == "negatif").sum())

# =========================
# DISTRIBUSI RATING
# =========================
st.subheader("Distribusi Rating")
r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("⭐ 1", (df["rating"] == 1).sum())
r2.metric("⭐⭐ 2", (df["rating"] == 2).sum())
r3.metric("⭐⭐⭐ 3", (df["rating"] == 3).sum())
r4.metric("⭐⭐⭐⭐ 4", (df["rating"] == 4).sum())
r5.metric("⭐⭐⭐⭐⭐ 5", (df["rating"] == 5).sum())

# =========================
# PIE CHART SENTIMEN
# =========================
st.subheader("Sentiment Distribution of Steam App Reviews")

sentiment_counts = df["polarity"].value_counts()
labels = sentiment_counts.index.tolist()
sizes = sentiment_counts.values

fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.05] * len(labels)
)
ax1.set_title("Sentiment Distribution of Steam App Reviews")
st.pyplot(fig1)

# =========================
# CONFUSION MATRIX
# =========================
st.subheader("Confusion Matrix of Steam App Sentiment Classification")

# confusion matrix hanya bisa dibuat kalau ada dua kolom label:
# - label aktual
# - label prediksi
#
# Di sini kita coba pakai:
# polarity = aktual
# sentiment_text = prediksi
#
# Kalau mau dibalik juga bisa, tapi ini yang paling masuk akal dari data kamu sekarang.

if "polarity" in df.columns and "sentiment_text" in df.columns:
    valid_df = df[
        df["polarity"].isin(["positif", "netral", "negatif"]) &
        df["sentiment_text"].isin(["positif", "netral", "negatif"])
    ].copy()

    if len(valid_df) > 0:
        labels_cm = ["positif", "netral", "negatif"]
        cm = confusion_matrix(
            valid_df["polarity"],
            valid_df["sentiment_text"],
            labels=labels_cm
        )

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels_cm)
        disp.plot(ax=ax2, cmap="Blues", colorbar=True)
        ax2.set_title("Confusion Matrix of Steam App Sentiment Classification")
        st.pyplot(fig2)
    else:
        st.info("Data untuk confusion matrix belum valid.")
else:
    st.info("Kolom 'polarity' dan 'sentiment_text' belum tersedia untuk confusion matrix.")

# =========================
# WORD CLOUD
# =========================
st.subheader("Word Cloud of Steam App Reviews")

text_source = ""
if "text_final" in df.columns:
    text_source = " ".join(df["text_final"].dropna().astype(str))
else:
    text_source = " ".join(df["review"].dropna().astype(str))

if text_source.strip():
    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white"
    ).generate(text_source)

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.imshow(wc, interpolation="bilinear")
    ax3.axis("off")
    ax3.set_title("Word Cloud of Steam App Reviews")
    st.pyplot(fig3)
else:
    st.info("Tidak ada teks yang bisa digunakan untuk word cloud.")

# =========================
# GRAFIK INDIKASI ANOMALI
# =========================
st.subheader("Grafik Distribusi Indikasi Anomali")
st.bar_chart(df["indikasi_anomali"].value_counts())

# =========================
# TABEL DATA
# =========================
st.subheader("Tabel Data Review")
show_cols = [c for c in [
    "review",
    "rating",
    "rating_bintang",
    "polarity",
    "sentiment_text",
    "anomaly_status",
    "indikasi_anomali"
] if c in df.columns]

st.dataframe(df[show_cols].head(50), use_container_width=True, hide_index=True)