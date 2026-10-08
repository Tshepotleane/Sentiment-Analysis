# SentimentScope

A Python and Flask sentiment analysis platform that analyzes customer reviews, classifies sentiment, and presents review insights through a web dashboard.

## Overview

**SentimentScope** is a web-based sentiment analysis application built with Python and Flask.

The application uses **VADER Sentiment Analysis**, a rule-based NLP tool designed for analyzing sentiment in text. Customer reviews are classified as:

* Positive
* Neutral
* Negative

Each review also receives a compound sentiment score ranging from approximately **-1 to +1**.

SentimentScope can analyze both an existing CSV dataset and individual reviews entered directly through the web interface.

## Features

* Analyze individual customer reviews
* Positive, Neutral, and Negative sentiment classification
* Compound sentiment scoring
* CSV dataset processing
* Automated analysis of dataset reviews
* Total, Positive, Neutral, and Negative review statistics
* Average sentiment score
* Recent review analysis table
* Generated analyzed dataset
* Responsive web interface
* Flask-powered backend
* Pandas-based data processing

## Technologies

* **Python** — application and data-processing logic
* **Flask** — web application framework
* **Pandas** — dataset processing and analysis
* **NLTK** — natural language processing library
* **VADER** — sentiment analysis
* **HTML** — application structure
* **CSS** — interface design
* **CSV** — review dataset storage
* **Git & GitHub** — version control and project hosting

## How It Works

The application follows this process:

```text
Customer Reviews
       ↓
   Pandas loads
    the dataset
       ↓
   VADER analyzes
     each review
       ↓
 Sentiment + Score
       ↓
Positive / Neutral / Negative
       ↓
Flask Dashboard
```

Users can also enter an individual review through the web interface.

The review is sent to the Flask backend, analyzed by VADER, and the sentiment classification and score are returned to the dashboard.

## Sentiment Classification

SentimentScope uses the VADER compound score to classify reviews:

| Compound Score         | Classification |
| ---------------------- | -------------- |
| 0.05 or higher         | Positive       |
| Between -0.05 and 0.05 | Neutral        |
| -0.05 or lower         | Negative       |

## Project Structure

```text
SentimentScope/
│
├── Data/
│   └── reviews.csv
│
├── Reports/
│   └── analyzed_reviews.csv
│
├── Static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── analysis.py
├── app.py
├── sentiments.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository and navigate into the project:

```bash
git clone https://github.com/Tshepotleane/SentimentScope.git
cd SentimentScope
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open the local application in your browser at:

```text
http://127.0.0.1:5000
```

## Dataset Analysis

The project includes a customer review dataset stored in:

```text
Data/reviews.csv
```

The dataset is processed using Pandas and each review is analyzed using VADER.

The analyzed results can be saved to:

```text
Reports/analyzed_reviews.csv
```

## Example

Input:

```text
I absolutely love this product! The quality is amazing.
```

Possible result:

```text
Sentiment: Positive
Score: 0.6989
```

A strongly negative review will produce a negative compound score and be classified as **Negative**.

## Future Improvements

Potential future improvements include:

* Interactive sentiment charts
* Sentiment distribution visualization
* Filtering reviews by sentiment
* Filtering by rating and date
* Larger datasets
* Exportable analysis reports
* Database integration
* Improved NLP models
* Deployment to a cloud platform

## Purpose

SentimentScope was developed as a practical project to demonstrate skills in:

* Python programming
* Flask web development
* Data analysis with Pandas
* Natural Language Processing
* Sentiment analysis
* HTML and CSS
* Data-driven application development
* Git and GitHub

---

**Built with Python, Flask, Pandas, NLTK and VADER.**
