from nltk.sentiment import SentimentIntensityAnalyzer


# Create the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()


def classify_sentiment(score):
    """
    Convert a compound sentiment score into
    Positive, Neutral, or Negative.
    """

    if score >= 0.05:
        return "Positive"

    elif score <= -0.05:
        return "Negative"

    else:
        return "Neutral"


def analyze_sentiment(text):
    """
    Analyze a piece of text and return
    the sentiment and sentiment score.
    """

    scores = sia.polarity_scores(text)

    compound_score = scores["compound"]

    sentiment = classify_sentiment(compound_score)

    return sentiment, compound_score