import pandas as pd

from sentiments import analyze_sentiment


DATA_FILE = "Data/reviews.csv"


def load_data():
    """
    Load the review dataset from the Data folder.
    """

    try:
        data = pd.read_csv(DATA_FILE)

        return data

    except FileNotFoundError:

        print(f"Error: Could not find {DATA_FILE}")

        return pd.DataFrame()


def analyze_reviews(data):
    """
    Analyze every review in the dataset.
    """

    if data.empty:
        return data

    sentiments = []
    scores = []

    for review in data["review"].fillna(""):

        sentiment, score = analyze_sentiment(str(review))

        sentiments.append(sentiment)
        scores.append(score)

    data["sentiment"] = sentiments
    data["score"] = scores

    return data


def get_statistics(data):
    """
    Calculate statistics for the dashboard.
    """

    if data.empty:

        return {
            "total": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "average_score": 0
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

    average_score = round(
        data["score"].mean(),
        4
    )

    return {
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "average_score": average_score
    }


def save_analyzed_data(data):
    """
    Save the analyzed dataset into the Reports folder.
    """

    output_file = "Reports/analyzed_reviews.csv"

    data.to_csv(
        output_file,
        index=False
    )

    return output_file


if __name__ == "__main__":

    data = load_data()

    data = analyze_reviews(data)

    if not data.empty:

        statistics = get_statistics(data)

        print("\n===================================")
        print("       SENTIMENT SCOPE")
        print("===================================")

        print(
            "\nTotal reviews:",
            statistics["total"]
        )

        print(
            "Positive reviews:",
            statistics["positive"]
        )

        print(
            "Neutral reviews:",
            statistics["neutral"]
        )

        print(
            "Negative reviews:",
            statistics["negative"]
        )

        print(
            "Average sentiment score:",
            statistics["average_score"]
        )

        print("\nSentiment distribution:")

        print(
            data["sentiment"].value_counts()
        )

        save_analyzed_data(data)

        print(
            "\nAnalyzed dataset saved to:",
            "Reports/analyzed_reviews.csv"
        )