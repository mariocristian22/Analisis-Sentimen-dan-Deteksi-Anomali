import streamlit as st
import pandas as pd
from utils import load_data, sentiment_from_text, sentiment_from_rating, detect_anomaly, detect_indikasi_anomali
 
st.set_page_config(page_title="Classification", page_icon="🧠", layout="wide")
 
st.title("Classification")
st.write("Halaman ini digunakan untuk menguji komentar secara manual atau melalui upload file.")
 
tab1, tab2 = st.tabs(["Uji Manual", "Upload File CSV"])
 
with tab1:
    st.subheader("Uji Komentar Manual")
 
    comment = st.text_area(
        "Masukkan komentar",
        placeholder="Contoh: aplikasi ini bagus sekali tapi rating saya kasih 1"
    )
 
    rating = st.selectbox("Pilih rating", [1, 2, 3, 4, 5], index=2)
 
    if st.button("Analisis Komentar"):
        if not comment.strip():
            st.warning("Silakan isi komentar terlebih dahulu.")
        else:
            sent_text = sentiment_from_text(comment)
            sent_rating = sentiment_from_rating(rating)
            anomaly = detect_anomaly(comment, rating)
            indikasi_anomali = detect_indikasi_anomali(comment, rating)
            rating_bintang = "⭐" * rating
 
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sentimen Teks", sent_text)
            c2.metric("Sentimen Rating", sent_rating)
            c3.metric("Anomali", anomaly)
            c4.metric("Indikasi Anomali", indikasi_anomali)
 
            st.subheader("Ringkasan Hasil")
            st.write(f"Komentar: {comment}")
            st.write(f"Rating: {rating} ({rating_bintang})")
 
            if indikasi_anomali == "anomali":
                st.error("Komentar ini terindikasi anomali karena isi komentar tidak sesuai dengan rating.")
            else:
                st.success("Komentar ini tidak terindikasi anomali.")
 
with tab2:
    st.subheader("Upload File CSV")
 
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
                df_upload["review"] = df_upload["review"].astype(str)
                df_upload["rating"] = pd.to_numeric(df_upload["rating"], errors="coerce").fillna(3).astype(int)
                df_upload["rating_bintang"] = df_upload["rating"].apply(lambda x: "⭐" * int(x))
                df_upload["sentiment_text"] = df_upload["review"].apply(sentiment_from_text)
                df_upload["polarity"] = df_upload["rating"].apply(sentiment_from_rating)
                df_upload["anomaly_status"] = df_upload.apply(
                    lambda row: detect_anomaly(row["review"], row["rating"]), axis=1
                )
                df_upload["indikasi_anomali"] = df_upload.apply(
                    lambda row: detect_indikasi_anomali(row["review"], row["rating"]), axis=1
                )
 
                st.success("File berhasil diproses.")
 
                st.subheader("Preview Hasil Klasifikasi")
                st.dataframe(
                    df_upload[[
                        "review",
                        "rating",
                        "rating_bintang",
                        "sentiment_text",
                        "polarity",
                        "anomaly_status",
                        "indikasi_anomali"
                    ]],
                    use_container_width=True,
                    hide_index=True
                )
 
                csv_result = df_upload.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Hasil Klasifikasi",
                    data=csv_result,
                    file_name="hasil_classification.csv",
                    mime="text/csv"
                )
 
        except Exception as e:
            st.error(f"Gagal memproses file: {e}")
