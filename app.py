
from flask import Flask, render_template, request

from analysis import (
    load_data,
    analyze_reviews,
    get_statistics
)

from sentiments import analyze_sentiment


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="Static"
)


@app.route("/", methods=["GET", "POST"])
def index():

    # Load and analyse the existing dataset.
    data = load_data()
    analyzed_data = analyze_reviews(data)
    stats = get_statistics(analyzed_data)

    # Prepare the rating breakdown.
    rating_counts = {
        str(rating): 0
        for rating in range(1, 6)
    }

    reviews = []

    if analyzed_data is not None and not analyzed_data.empty:

        reviews = analyzed_data.to_dict(orient="records")

        if "rating" in analyzed_data.columns:

            counts = analyzed_data["rating"].value_counts()

            for rating in range(1, 6):
                rating_counts[str(rating)] = int(
                    counts.get(rating, counts.get(str(rating), 0))
                )

    # Values used by the Review Analyzer.
    analyzed_review = None
    analyzed_sentiment = None
    analyzed_score = None
    error_message = None

    if request.method == "POST":

        review_text = request.form.get("review", "").strip()

        if not review_text:
            error_message = "Please enter a review before analysing."

        else:
            try:
                result = analyze_sentiment(review_text)

                # Support the existing function's return format.
                if isinstance(result, dict):
                    analyzed_sentiment = result.get(
                        "sentiment",
                        result.get("label")
                    )
                    analyzed_score = result.get(
                        "score",
                        result.get("compound")
                    )

                elif isinstance(result, (tuple, list)):
                    analyzed_sentiment = result[0]
                    analyzed_score = result[1] if len(result) > 1 else None

                else:
                    analyzed_sentiment = str(result)

                analyzed_review = review_text

            except Exception as error:
                app.logger.exception("Review analysis failed")
                error_message = (
                    "The review could not be analysed. "
                    "Please check the sentiment function."
                )

    return render_template(
        "index.html",
        reviews=reviews,
        stats=stats,
        statistics=stats,
        rating_counts=rating_counts,
        analyzed_review=analyzed_review,
        analyzed_sentiment=analyzed_sentiment,
        analyzed_score=analyzed_score,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)
