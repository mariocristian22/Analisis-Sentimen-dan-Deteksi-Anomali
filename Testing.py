import streamlit as st
import pandas as pd
from utils import (
    sentiment_from_rating,
    sentiment_from_text,
    detect_anomaly,
    detect_buzzer
)

st.set_page_config(page_title="Testing", page_icon="🧪", layout="wide")

st.title("Testing")
st.write("Masukkan komentar dan rating untuk melihat hasil sentimen, anomali, dan indikasi buzzer.")

# Inisialisasi history
if "test_history" not in st.session_state:
    st.session_state.test_history = []

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
        buzzer = detect_buzzer(comment, rating)
        rating_bintang = "⭐" * rating

        # Penjelasan hasil
        if buzzer == "buzzer":
            alasan = (
                "Komentar terindikasi buzzer karena isi komentar tidak sesuai dengan rating. "
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
                "Komentar ini tidak terindikasi buzzer karena isi komentar masih sesuai "
                "dengan rating yang diberikan."
            )

        # Ringkasan hasil utama
        st.subheader("Hasil Analisis")

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Rating", rating)
        c2.metric("Bintang", rating_bintang)
        c3.metric("Sentimen Teks", sent_text)
        c4.metric("Sentimen Rating", sent_rating)
        c5.metric("Status Buzzer", buzzer)

        c6, c7 = st.columns(2)
        c6.metric("Status Anomali", anomaly)
        c7.metric("Jumlah Karakter", len(comment))

        # Status warna
        if buzzer == "buzzer":
            st.error(f"Hasil akhir: {buzzer.upper()}")
        elif anomaly == "perlu_tinjauan":
            st.warning("Hasil akhir: PERLU TINJAUAN")
        else:
            st.success("Hasil akhir: NON_BUZZER")

        st.subheader("Penjelasan")
        st.write(alasan)

        st.subheader("Detail Uji")
        detail_df = pd.DataFrame({
            "Komponen": [
                "Komentar",
                "Rating Angka",
                "Rating Bintang",
                "Sentimen Teks",
                "Sentimen Rating",
                "Status Anomali",
                "Status Buzzer"
            ],
            "Hasil": [
                comment,
                rating,
                rating_bintang,
                sent_text,
                sent_rating,
                anomaly,
                buzzer
            ]
        })
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

        # Simpan ke history
        st.session_state.test_history.insert(0, {
            "komentar": comment,
            "rating": rating,
            "bintang": rating_bintang,
            "sentimen_teks": sent_text,
            "sentimen_rating": sent_rating,
            "anomali": anomaly,
            "buzzer": buzzer
        })

# Riwayat pengujian
st.subheader("Riwayat Pengujian")
if len(st.session_state.test_history) > 0:
    history_df = pd.DataFrame(st.session_state.test_history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

    csv_history = history_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Riwayat Pengujian",
        data=csv_history,
        file_name="riwayat_testing_sentimen_buzzer.csv",
        mime="text/csv"
    )

    if st.button("Hapus Riwayat"):
        st.session_state.test_history = []
        st.rerun()
else:
    st.info("Belum ada riwayat pengujian.")