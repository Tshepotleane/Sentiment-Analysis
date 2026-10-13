from pathlib import Path

import pandas as pd

from sentiments import analyze_sentiment


# ==========================================
# FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "Data" / "reviews.csv"

REPORT_FILE = BASE_DIR / "Reports" / "analyzed_reviews.csv"


# ==========================================
# LOAD DATA
# ==========================================

def load_data():
    """
    Load customer reviews from the CSV dataset.
    """

    try:
        data = pd.read_csv(DATA_FILE)

        if "review" not in data.columns:
            print("Error: Dataset must contain a 'review' column.")
            return pd.DataFrame()

        return data

    except FileNotFoundError:
        print(f"Error: Could not find {DATA_FILE}")
        return pd.DataFrame()

    except pd.errors.EmptyDataError:
        print("Error: The review dataset is empty.")
        return pd.DataFrame()

    except pd.errors.ParserError:
        print("Error: Could not read the CSV file.")
        return pd.DataFrame()


# ==========================================
# ANALYZE REVIEWS
# ==========================================

def analyze_reviews(data):
    """
    Analyze every review and add sentiment
    classifications and compound scores.
    """

    if data.empty or "review" not in data.columns:
        return data.copy()

    data = data.copy()

    sentiments = []
    scores = []

    for review in data["review"].fillna(""):

        sentiment, score = analyze_sentiment(str(review))

        sentiments.append(sentiment)
        scores.append(score)

    data["sentiment"] = sentiments
    data["score"] = scores

    # Convert ratings to numbers where possible.
    if "rating" in data.columns:
        data["rating"] = pd.to_numeric(
            data["rating"],
            errors="coerce"
        )

    return data


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def get_statistics(data):
    """
    Calculate the main dashboard metrics.
    """

    if data.empty:
        return {
            "total": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "positive_percentage": 0,
            "average_score": 0,
            "average_rating": None
        }

    total = len(data)

    positive = int(
        (data["sentiment"] == "Positive").sum()
    )

    neutral = int(
        (data["sentiment"] == "Neutral").sum()
    )

    negative = int(
        (data["sentiment"] == "Negative").sum()
    )

    positive_percentage = round(
        (positive / total) * 100,
        1
    ) if total else 0

    average_score = round(
        data["score"].mean(),
        4
    )

    average_rating = None

    if "rating" in data.columns:
        ratings = pd.to_numeric(
            data["rating"],
            errors="coerce"
        ).dropna()

        if not ratings.empty:
            average_rating = round(
                ratings.mean(),
                2
            )

    return {
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "positive_percentage": positive_percentage,
        "average_score": average_score,
        "average_rating": average_rating
    }


# ==========================================
# SENTIMENT CHART DATA
# ==========================================

def get_sentiment_distribution(data):
    """
    Return sentiment totals in a consistent order
    for the dashboard charts.
    """

    labels = ["Positive", "Neutral", "Negative"]

    if data.empty:
        return [
            {"label": label, "count": 0}
            for label in labels
        ]

    counts = data["sentiment"].value_counts()

    return [
        {
            "label": label,
            "count": int(counts.get(label, 0))
        }
        for label in labels
    ]


# ==========================================
# RATING CHART DATA
# ==========================================

def get_rating_distribution(data):
    """
    Count customer ratings from 1 to 5 stars.
    """

    if data.empty or "rating" not in data.columns:
        return [
            {"rating": rating, "count": 0}
            for rating in range(1, 6)
        ]

    ratings = pd.to_numeric(
        data["rating"],
        errors="coerce"
    )

    return [
        {
            "rating": rating,
            "count": int((ratings == rating).sum())
        }
        for rating in range(1, 6)
    ]


# ==========================================
# SENTIMENT TREND DATA
# ==========================================

def get_sentiment_trend(data):
    """
    Calculate daily sentiment counts when the
    dataset contains a usable date column.
    """

    if data.empty or "date" not in data.columns:
        return []

    trend_data = data.copy()

    trend_data["date"] = pd.to_datetime(
        trend_data["date"],
        errors="coerce"
    )

    trend_data = trend_data.dropna(
        subset=["date"]
    )

    if trend_data.empty:
        return []

    trend_data["date"] = (
        trend_data["date"].dt.strftime("%Y-%m-%d")
    )

    grouped = (
        trend_data.groupby(["date", "sentiment"])
        .size()
        .unstack(fill_value=0)
    )

    for sentiment in ["Positive", "Neutral", "Negative"]:
        if sentiment not in grouped.columns:
            grouped[sentiment] = 0

    grouped = grouped.sort_index()

    return [
        {
            "date": date,
            "positive": int(row["Positive"]),
            "neutral": int(row["Neutral"]),
            "negative": int(row["Negative"])
        }
        for date, row in grouped.iterrows()
    ]


# ==========================================
# EXPORT ANALYZED DATA
# ==========================================

def save_analyzed_data(data):
    """
    Save analyzed reviews into the Reports folder.
    """

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        REPORT_FILE,
        index=False
    )

    return str(REPORT_FILE)


# ==========================================
# RUN ANALYSIS DIRECTLY
# ==========================================

if __name__ == "__main__":

    data = load_data()

    data = analyze_reviews(data)

    if not data.empty:

        statistics = get_statistics(data)

        print("\n===================================")
        print("          SENTIMENT SCOPE")
        print("===================================")

        print("Total reviews:", statistics["total"])
        print("Positive reviews:", statistics["positive"])
        print("Neutral reviews:", statistics["neutral"])
        print("Negative reviews:", statistics["negative"])

        print(
            "Positive sentiment rate:",
            f'{statistics["positive_percentage"]}%'
        )

        print(
            "Average sentiment score:",
            statistics["average_score"]
        )

        print(
            "Average rating:",
            statistics["average_rating"]
        )

        report = save_analyzed_data(data)

        print("\nAnalyzed dataset saved to:", report)

    else:
        print("No reviews available to analyze.")


