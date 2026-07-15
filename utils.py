import pandas as pd
from pathlib import Path

positive_words = {
    "good", "great", "love", "best", "nice", "amazing", "helpful", "easy",
    "awesome", "excellent", "fantastic", "perfect", "wonderful", "super",
    "recommended", "recommend", "satisfied", "smooth", "fast", "stable",
    "cool", "beautiful", "useful", "friendly", "impressive", "outstanding",
    "bagus", "baik", "mantap", "keren", "suka", "memuaskan", "hebat",
    "cepat", "lancar", "stabil", "berguna", "membantu", "mudah",
    "nyaman", "cocok", "terbaik", "istimewa", "luar biasa", "praktis",
    "rapi", "oke", "ok", "aman", "senang", "puas", "top", "jos",
    "sip", "favorit", "berhasil", "bermanfaat", "supportive"
}

negative_words = {
    "bad", "worst", "hate", "bug", "error", "problem", "slow", "broken",
    "awful", "terrible", "horrible", "useless", "disappointed", "annoying",
    "lag", "laggy", "crash", "failed", "failure", "hard", "difficult",
    "confusing", "scam", "fake", "waste", "poor", "unstable", "freeze",
    "jelek", "buruk", "parah", "kecewa", "rusak", "gagal", "lemot",
    "lambat", "eror", "susah", "sulit", "ribet", "membingungkan",
    "mengecewakan", "sampah", "payah", "bohong", "penipu",
    "tidak berguna", "gangguan", "crash terus", "sering error", "bermasalah",
    "ngelag", "gak jelas", "tidak bagus", "ga bagus", "tidak suka",
    "benci", "kesal", "marah", "parah banget", "fatal", "drop", "hancur",
    "trash", "garbage", "nonsense"
}

neutral_words = {
    "okay", "ok", "average", "normal", "standard", "biasa", "lumayan",
    "cukup", "sedang", "so so", "not bad", "b aja", "biasa saja",
    "standar", "netral", "medium", "common", "fine", "moderate"
}

insult_words = {
    "anjing", "babi", "monyet", "bangsat", "kampret", "keledai",
    "asu", "goblok", "tolol", "idiot", "dungu", "bebal",
    "tai", "sialan", "brengsek", "setan", "laknat",
    "dog", "pig", "monkey", "donkey", "stupid", "dumb"
}

def sentiment_from_rating(rating):
    if rating >= 4:
        return "positif"
    elif rating == 3:
        return "netral"
    else:
        return "negatif"

def sentiment_from_text(text):
    text = str(text).lower()
    words = text.split()

    pos_count = sum(1 for word in words if word in positive_words)
    neg_count = sum(1 for word in words if word in negative_words or word in insult_words)
    neu_count = sum(1 for word in words if word in neutral_words)

    if pos_count > neg_count and pos_count >= neu_count:
        return "positif"
    elif neg_count > pos_count and neg_count >= neu_count:
        return "negatif"
    else:
        return "netral"

def detect_anomaly(text, rating):
    sent_text = sentiment_from_text(text)

    if sent_text == "positif" and rating in [1, 2]:
        return "anomali"
    elif sent_text == "negatif" and rating in [4, 5]:
        return "anomali"
    elif sent_text == "netral" and rating == 3:
        return "normal"
    elif sent_text == sentiment_from_rating(rating):
        return "normal"
    else:
        return "perlu_tinjauan"

def detect_buzzer(text, rating):
    sent_text = sentiment_from_text(text)

    if sent_text == "positif" and rating in [1, 2]:
        return "buzzer"
    elif sent_text == "negatif" and rating in [4, 5]:
        return "buzzer"
    else:
        return "non_buzzer"

def load_data(csv_path):
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {csv_path}")

    df = pd.read_csv(path)
    df.columns = [col.strip().lower() for col in df.columns]

    rename_map = {}

    if "content" in df.columns and "review" not in df.columns:
        rename_map["content"] = "review"

    if "score" in df.columns and "rating" not in df.columns:
        rename_map["score"] = "rating"

    df = df.rename(columns=rename_map)

    if "review" not in df.columns:
        raise ValueError("Kolom 'review' tidak ditemukan di file CSV.")

    if "rating" not in df.columns:
        raise ValueError("Kolom 'rating' tidak ditemukan di file CSV.")

    df["review"] = df["review"].astype(str)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(3).astype(int)

    df["rating_bintang"] = df["rating"].apply(
        lambda x: "⭐" * int(x) if pd.notnull(x) and 1 <= int(x) <= 5 else ""
    )

    if "polarity" not in df.columns:
        df["polarity"] = df["rating"].apply(sentiment_from_rating)

    if "sentiment_text" not in df.columns:
        df["sentiment_text"] = df["review"].apply(sentiment_from_text)

    if "anomaly_status" not in df.columns:
        df["anomaly_status"] = df.apply(
            lambda row: detect_anomaly(row["review"], row["rating"]),
            axis=1
        )

    if "buzzer_status" not in df.columns:
        df["buzzer_status"] = df.apply(
            lambda row: detect_buzzer(row["review"], row["rating"]),
            axis=1
        )

    return df