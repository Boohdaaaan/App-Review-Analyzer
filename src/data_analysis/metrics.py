from fastapi import HTTPException

from src.models import Review, Sentiment


def calculate_metrics(reviews: list[Review]) -> dict:
    """Calculate metrics for a list of reviews."""
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews available")
        
    n_reviews = len(reviews)
    metrics = {
        # Basic counts and averages
        "total_reviews": n_reviews,
        "average_rating": round(sum(r.rating for r in reviews) / n_reviews, 2),
        
        # Sentiment distribution (Very Negative, Negative, Neutral, Positive, Very Positive)
        "sentiment_distribution": {
            sentiment: {
                "count": 0,
                "percentage": 0.0
            } for sentiment in Sentiment
        },

        # Rating distribution (1-5 stars)
        "rating_distribution": {
            rating: {
                "count": 0,
                "percentage": 0.0
            } for rating in range(1, 6)
        },
        
        # Country distribution (will be filled in the next step)
        "country_distribution": {}
    }
    
    for review in reviews:
        # Calculate sentiment distribution
        metrics["sentiment_distribution"][review.sentiment]["count"] += 1

        # Calculate rating distribution
        metrics["rating_distribution"][review.rating]["count"] += 1
        
        # Calculate country distribution
        if review.country not in metrics["country_distribution"]:
            metrics["country_distribution"][review.country] = {"count": 0, "percentage": 0.0}
        metrics["country_distribution"][review.country]["count"] += 1
    
    # Calculate percentages
    for sentiment in metrics["sentiment_distribution"]:
        count = metrics["sentiment_distribution"][sentiment]["count"]
        metrics["sentiment_distribution"][sentiment]["percentage"] = round((count / n_reviews) * 100, 2)
    
    for rating in metrics["rating_distribution"]:
        count = metrics["rating_distribution"][rating]["count"]
        metrics["rating_distribution"][rating]["percentage"] = round((count / n_reviews) * 100, 2)
        
    for country in metrics["country_distribution"]:
        count = metrics["country_distribution"][country]["count"]
        metrics["country_distribution"][country]["percentage"] = round((count / n_reviews) * 100, 2)
    
    return metrics
