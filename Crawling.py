import streamlit as st
import pandas as pd
import time
from google_play_scraper import reviews, Sort

st.set_page_config(page_title="Crawling", page_icon="🔍", layout="wide")

st.title("Crawling Data")
st.write("Halaman ini digunakan untuk mengambil data ulasan aplikasi Steam langsung dari Google Play Store.")

APP_ID = 'com.valvesoftware.android.steam.community'

st.subheader("Konfigurasi Crawling")

col1, col2 = st.columns(2)

with col1:
    jumlah_data = st.selectbox(
        "Jumlah data yang ingin diambil",
        [100, 500, 1000, 2000, 5000],
        index=1
    )

with col2:
    urutan = st.selectbox(
        "Urutkan berdasarkan",
        ["Terbaru", "Relevansi"],
        index=0
    )

negara_options = {
    "Indonesia": ("id", "id"),
    "Amerika Serikat": ("en", "us"),
    "Inggris": ("en", "gb"),
    "Rusia": ("ru", "ru"),
    "Brasil": ("pt", "br"),
    "Jerman": ("de", "de"),
    "Prancis": ("fr", "fr"),
    "Jepang": ("ja", "jp"),
    "Korea Selatan": ("ko", "kr"),
    "China": ("zh", "cn"),
}

negara_pilihan = st.selectbox(
    "Pilih negara",
    list(negara_options.keys()),
    index=0
)

lang, country = negara_options[negara_pilihan]
sort_order = Sort.NEWEST if urutan == "Terbaru" else Sort.MOST_RELEVANT

if st.button("🚀 Mulai Crawling"):
    with st.spinner(f"Sedang mengambil {jumlah_data} data dari {negara_pilihan}..."):
        try:
            hasil, _ = reviews(
                APP_ID,
                lang=lang,
                country=country,
                sort=sort_order,
                count=jumlah_data
            )

            df_crawl = pd.DataFrame(hasil)[['reviewId', 'content', 'score', 'at']].copy()
            df_crawl.columns = ['review_id', 'review', 'rating', 'date']
            df_crawl = df_crawl.dropna(subset=['review'])
            df_crawl = df_crawl.drop_duplicates(subset=['review_id'])
            df_crawl['rating_bintang'] = df_crawl['rating'].apply(lambda x: "⭐" * int(x))
            df_crawl['negara'] = negara_pilihan
            df_crawl = df_crawl.reset_index(drop=True)

            st.success(f"✅ Berhasil mengambil {len(df_crawl):,} data dari {negara_pilihan}!")

            st.subheader("Preview Data")
            st.dataframe(
                df_crawl[['review', 'rating', 'rating_bintang', 'date', 'negara']].head(20),
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Ringkasan")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Data", len(df_crawl))
            col2.metric("Rating 1-2 ⭐", ((df_crawl['rating'] <= 2).sum()))
            col3.metric("Rating 3 ⭐", ((df_crawl['rating'] == 3).sum()))
            col4.metric("Rating 4-5 ⭐", ((df_crawl['rating'] >= 4).sum()))

            # Simpan ke session state supaya bisa dipakai halaman lain
            st.session_state['df_crawl'] = df_crawl

            # Download CSV
            csv = df_crawl.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Hasil Crawling (CSV)",
                data=csv,
                file_name=f"steam_reviews_{negara_pilihan.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Gagal melakukan crawling: {e}")