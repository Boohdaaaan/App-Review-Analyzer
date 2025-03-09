from src.models import Review
from src.data_analysis.hf_pipelines import get_sentiment_pipeline


def analyze_reviews_sentiment(reviews: list[Review]) -> list[Review]:
    """Analyze the sentiment of a list of reviews."""
    sentiment_pipeline = get_sentiment_pipeline()
    texts = [review.review_text for review in reviews]
    results = sentiment_pipeline(texts)

    for review, result in zip(reviews, results):
        review.sentiment = result['label']

    return reviews
