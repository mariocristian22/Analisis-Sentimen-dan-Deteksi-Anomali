import streamlit as st
import pandas as pd
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
    "Kanada": ("en", "ca"),
    "Meksiko": ("es", "mx"),
    "Brasil": ("pt", "br"),
    "Argentina": ("es", "ar"),
    "Chile": ("es", "cl"),
    "Kolombia": ("es", "co"),
    "Peru": ("es", "pe"),
    "Venezuela": ("es", "ve"),
    "Ekuador": ("es", "ec"),
    "Bolivia": ("es", "bo"),
    "Paraguay": ("es", "py"),
    "Uruguay": ("es", "uy"),
    "Jamaika": ("en", "jm"),
    "Trinidad dan Tobago": ("en", "tt"),
    "Barbados": ("en", "bb"),
    "Bahama": ("en", "bs"),
    "Belize": ("en", "bz"),
    "Kosta Rika": ("es", "cr"),
    "Panama": ("es", "pa"),
    "Guatemala": ("es", "gt"),
    "Honduras": ("es", "hn"),
    "El Salvador": ("es", "sv"),
    "Nicaragua": ("es", "ni"),
    "Republik Dominika": ("es", "do"),
    "Haiti": ("fr", "ht"),
    "Kuba": ("es", "cu"),
    "Puerto Riko": ("es", "pr"),
    "Inggris": ("en", "gb"),
    "Irlandia": ("en", "ie"),
    "Prancis": ("fr", "fr"),
    "Jerman": ("de", "de"),
    "Italia": ("it", "it"),
    "Spanyol": ("es", "es"),
    "Portugal": ("pt", "pt"),
    "Belanda": ("nl", "nl"),
    "Belgia": ("fr", "be"),
    "Swiss": ("de", "ch"),
    "Austria": ("de", "at"),
    "Polandia": ("pl", "pl"),
    "Rusia": ("ru", "ru"),
    "Ukraina": ("uk", "ua"),
    "Turki": ("tr", "tr"),
    "Ceko": ("cs", "cz"),
    "Rumania": ("ro", "ro"),
    "Hungaria": ("hu", "hu"),
    "Yunani": ("el", "gr"),
    "Swedia": ("sv", "se"),
    "Norwegia": ("no", "no"),
    "Denmark": ("da", "dk"),
    "Finlandia": ("fi", "fi"),
    "Slovakia": ("sk", "sk"),
    "Slovenia": ("sl", "si"),
    "Bulgaria": ("bg", "bg"),
    "Serbia": ("sr", "rs"),
    "Kroasia": ("hr", "hr"),
    "Bosnia dan Herzegovina": ("bs", "ba"),
    "Makedonia Utara": ("mk", "mk"),
    "Albania": ("sq", "al"),
    "Montenegro": ("sr", "me"),
    "Latvia": ("lv", "lv"),
    "Lituania": ("lt", "lt"),
    "Estonia": ("et", "ee"),
    "Islandia": ("is", "is"),
    "Malta": ("mt", "mt"),
    "Luksemburg": ("fr", "lu"),
    "Belarus": ("be", "by"),
    "Moldova": ("ro", "md"),
    "Siprus": ("el", "cy"),
    "San Marino": ("it", "sm"),
    "Monako": ("fr", "mc"),
    "Liechtenstein": ("de", "li"),
    "Andorra": ("ca", "ad"),
    "Vatikan": ("it", "va"),
    "Jepang": ("ja", "jp"),
    "Korea Selatan": ("ko", "kr"),
    "China": ("zh", "cn"),
    "Taiwan": ("zh", "tw"),
    "Hong Kong": ("zh", "hk"),
    "Malaysia": ("ms", "my"),
    "Thailand": ("th", "th"),
    "Vietnam": ("vi", "vn"),
    "Singapura": ("en", "sg"),
    "Filipina": ("tl", "ph"),
    "India": ("hi", "in"),
    "Pakistan": ("ur", "pk"),
    "Bangladesh": ("bn", "bd"),
    "Kamboja": ("km", "kh"),
    "Laos": ("lo", "la"),
    "Myanmar": ("my", "mm"),
    "Sri Lanka": ("si", "lk"),
    "Nepal": ("ne", "np"),
    "Kazakhstan": ("kk", "kz"),
    "Uzbekistan": ("uz", "uz"),
    "Kirgizstan": ("ky", "kg"),
    "Tajikistan": ("tg", "tj"),
    "Turkmenistan": ("tk", "tm"),
    "Azerbaijan": ("az", "az"),
    "Armenia": ("hy", "am"),
    "Georgia": ("ka", "ge"),
    "Mongolia": ("mn", "mn"),
    "Makau": ("zh", "mo"),
    "Brunei": ("ms", "bn"),
    "Timor-Leste": ("pt", "tl"),
    "Bhutan": ("dz", "bt"),
    "Maladewa": ("dv", "mv"),
    "Afghanistan": ("fa", "af"),
    "Arab Saudi": ("ar", "sa"),
    "Uni Emirat Arab": ("ar", "ae"),
    "Mesir": ("ar", "eg"),
    "Israel": ("he", "il"),
    "Iran": ("fa", "ir"),
    "Irak": ("ar", "iq"),
    "Yordania": ("ar", "jo"),
    "Lebanon": ("ar", "lb"),
    "Kuwait": ("ar", "kw"),
    "Qatar": ("ar", "qa"),
    "Oman": ("ar", "om"),
    "Bahrain": ("ar", "bh"),
    "Suriah": ("ar", "sy"),
    "Yaman": ("ar", "ye"),
    "Palestina": ("ar", "ps"),
    "Afrika Selatan": ("en", "za"),
    "Nigeria": ("en", "ng"),
    "Kenya": ("sw", "ke"),
    "Tanzania": ("sw", "tz"),
    "Ghana": ("en", "gh"),
    "Kamerun": ("fr", "cm"),
    "Senegal": ("fr", "sn"),
    "Pantai Gading": ("fr", "ci"),
    "Etiopia": ("am", "et"),
    "Uganda": ("sw", "ug"),
    "Mozambik": ("pt", "mz"),
    "Angola": ("pt", "ao"),
    "Zambia": ("en", "zm"),
    "Zimbabwe": ("en", "zw"),
    "Rwanda": ("fr", "rw"),
    "Botswana": ("en", "bw"),
    "Namibia": ("en", "na"),
    "Malawi": ("en", "mw"),
    "Mauritius": ("en", "mu"),
    "Tunisia": ("fr", "tn"),
    "Maroko": ("ar", "ma"),
    "Aljazair": ("ar", "dz"),
    "Libya": ("ar", "ly"),
    "Sudan": ("ar", "sd"),
    "Burkina Faso": ("fr", "bf"),
    "Mali": ("fr", "ml"),
    "Niger": ("fr", "ne"),
    "Togo": ("fr", "tg"),
    "Benin": ("fr", "bj"),
    "Gabon": ("fr", "ga"),
    "Republik Demokratik Kongo": ("fr", "cd"),
    "Republik Kongo": ("fr", "cg"),
    "Somalia": ("so", "so"),
    "Djibouti": ("fr", "dj"),
    "Eritrea": ("ti", "er"),
    "Madagaskar": ("fr", "mg"),
    "Komoro": ("ar", "km"),
    "Seychelles": ("fr", "sc"),
    "Tanjung Verde": ("pt", "cv"),
    "Guinea": ("fr", "gn"),
    "Guinea-Bissau": ("pt", "gw"),
    "Guinea Khatulistiwa": ("es", "gq"),
    "Sierra Leone": ("en", "sl"),
    "Liberia": ("en", "lr"),
    "Gambia": ("en", "gm"),
    "Sao Tome dan Principe": ("pt", "st"),
    "Afrika Tengah": ("fr", "cf"),
    "Chad": ("fr", "td"),
    "Sudan Selatan": ("en", "ss"),
    "Burundi": ("fr", "bi"),
    "Lesotho": ("en", "ls"),
    "Eswatini": ("en", "sz"),
    "Australia": ("en", "au"),
    "Selandia Baru": ("en", "nz"),
    "Papua Nugini": ("en", "pg"),
    "Fiji": ("en", "fj"),
    "Kepulauan Solomon": ("en", "sb"),
    "Vanuatu": ("fr", "vu"),
    "Samoa": ("en", "ws"),
    "Tonga": ("en", "to"),
    "Kiribati": ("en", "ki"),
    "Nauru": ("en", "nr"),
    "Tuvalu": ("en", "tv"),
    "Palau": ("en", "pw"),
    "Mikronesia": ("en", "fm"),
    "Kepulauan Marshall": ("en", "mh"),
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
            col2.metric("Rating 1-2 ⭐", (df_crawl['rating'] <= 2).sum())
            col3.metric("Rating 3 ⭐", (df_crawl['rating'] == 3).sum())
            col4.metric("Rating 4-5 ⭐", (df_crawl['rating'] >= 4).sum())

            st.session_state['df_crawl'] = df_crawl

            csv = df_crawl.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Hasil Crawling (CSV)",
                data=csv,
                file_name=f"steam_reviews_{negara_pilihan.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Gagal melakukan crawling: {e}")