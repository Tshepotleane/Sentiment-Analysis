import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def load_vader():
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        downloaded = nltk.download("vader_lexicon", quiet=True)
        if not downloaded:
            raise RuntimeError(
                "Could not download VADER's sentiment lexicon."
            )

    return SentimentIntensityAnalyzer()


sia = load_vader()


def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    return "Neutral"


def analyze_sentiment(text):
    scores = sia.polarity_scores(str(text))
    compound_score = scores["compound"]

    return classify_sentiment(compound_score), compound_score