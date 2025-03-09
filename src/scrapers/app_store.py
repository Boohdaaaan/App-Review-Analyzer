import logging
from app_store_scraper import AppStore

from src.models import Review

logger = logging.getLogger(__name__)


def fetch_app_reviews(app_name: str, app_id: int, country: str = "us", num_reviews: int = 100) -> list[Review]:
    """
    Fetch reviews from Apple App Store.
    
    Args:
        app_name: Name of the app
        app_id: Numeric ID of the app on App Store
        country: Country code for the store (default: "us")
        num_reviews: Number of reviews to fetch (default: 100)
    
    Returns:
        list[Review]
    """
    try:
        app = AppStore(country=country, app_name=app_name, app_id=app_id)
        app.review(how_many=num_reviews)

        fetched_reviews = [
            Review(
                review_id=None, # App Store does not provide review IDs
                source="app_store",
                user_name=review["userName"],
                country=country,
                rating=review["rating"],
                review_text=review["review"],
                date=review["date"],
            )
            for review in app.reviews
        ]

        return fetched_reviews
        
    except Exception as e:
        logger.error(f"Error fetching App Store reviews: {e}")
        return []
