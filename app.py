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


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def index():

    # Load the dataset
    data = load_data()

    # Analyze the dataset
    data = analyze_reviews(data)

    # Get dashboard statistics
    statistics = get_statistics(data)

    # Default values for manual analysis
    analyzed_review = None
    analyzed_sentiment = None
    analyzed_score = None

    # ==========================================
    # MANUAL REVIEW ANALYSIS
    # ==========================================

    if request.method == "POST":

        review = request.form.get(
            "review",
            ""
        ).strip()

        if review:

            analyzed_sentiment, analyzed_score = (
                analyze_sentiment(review)
            )

            analyzed_review = review

    # ==========================================
    # RECENT REVIEWS
    # ==========================================

    if not data.empty:

        recent_reviews = (
            data.head(10)
            .to_dict("records")
        )

    else:

        recent_reviews = []

    # ==========================================
    # SEND DATA TO HTML
    # ==========================================

    return render_template(
        "index.html",

        statistics=statistics,

        recent_reviews=recent_reviews,

        analyzed_review=analyzed_review,

        analyzed_sentiment=analyzed_sentiment,

        analyzed_score=analyzed_score
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )