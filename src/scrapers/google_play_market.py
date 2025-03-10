import logging
from google_play_scraper import Sort, reviews, app

from src.models import Review

logger = logging.getLogger(__name__)


def fetch_app_reviews(app_name: str, app_id: str, country: str = "us", num_reviews: int = 100) -> list[Review]:
    """
    Fetch reviews from Google Play Store.
    
    Args:
        app_name: Name of the app
        app_id: Package name/ID of the app on Google Play Store
        country: Country code for the store (default: "us")
        num_reviews: Number of reviews to fetch (default: 100)
    
    Returns:
        list[Review]
    """
    try:
        package_name = str(app_id)
        result, _ = reviews(
            package_name,
            lang=country,
            country=country,
            sort=Sort.NEWEST,
            count=num_reviews
        )

        fetched_reviews = [
            Review(
                review_id=review["reviewId"],
                source="google_play_market",
                user_name=review["userName"],
                country=country,
                rating=review["score"],
                review_text=review["content"],
                date=review["at"],
            )
            for review in result
        ]

        return fetched_reviews

    except Exception as e:
        logger.error(f"Error fetching Google Play reviews: {e}")
        return []


def fetch_app_description(app_id: str, country: str = "us") -> str | None:
    """
    Fetch the description of an app from the Google Play Store.
    
    Args:
        app_id: Package name/ID of the app on Google Play Store
        country: Country code for the store (default: "us")
    
    Returns:
        str: App description text. Returns empty string if description cannot be fetched.
    """
    try:
        result = app(
            app_id=app_id,
            lang="en",
            country=country,
        )
    except Exception as e:
        logger.error(f"Error fetching Google Play description: {e}")
        return None

    return result["description"]
