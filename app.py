import logging
from pydantic import BaseModel
from typing import Literal
from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv

from src.scrapers import (
    google_play_market as google_play_market_scraper,
    app_store as app_store_scraper,
)
from src.data_analysis.metrics import calculate_metrics
from src.data_analysis.plots import generate_plots
from src.data_analysis.sentiment_analysis import analyze_reviews_sentiment
from src.llm.llm_pipeline import generate_overview

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()


@app.get("/health")
async def healthcheck():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


class ReviewResponse(BaseModel):
    llm_overview: str | None = None
    metrics: dict | None = None
    plots: dict | None = None
    raw_data: dict| None = None


@app.get("/app-reviews/", response_model=ReviewResponse)
async def get_app_reviews(
    app_name: str,
    app_id: int | str,
    country: str = "us",
    num_reviews: int = Query(default=100, ge=1, le=1000),
    reviews_source: Literal["app_store", "google_play_market"] = "app_store",
    include_llm_overview: bool = True,
    include_metrics: bool = True,
    include_plots: bool = True,
    include_raw_data: bool = True,
) -> ReviewResponse:
    """Fetch and analyze app reviews with specified return data types."""
    logger.info(
        f"Fetching reviews for app '{app_name}' (ID: {app_id}) from {reviews_source}",
        extra={
            "app_name": app_name,
            "app_id": app_id,
            "country": country,
            "num_reviews": num_reviews,
            "reviews_source": reviews_source
        }
    )
    
    try:
        if reviews_source == "app_store":
            reviews = app_store_scraper.fetch_app_reviews(app_name, app_id, country, num_reviews)
        elif reviews_source == "google_play_market":
            reviews = google_play_market_scraper.fetch_app_reviews(app_name, app_id, country, num_reviews)
        else:
            logger.error(f"Invalid reviews source provided: {reviews_source}")
            raise HTTPException(status_code=400, detail="Invalid reviews source")
        
        if not reviews:
            logger.warning(f"No reviews found for app '{app_name}' (ID: {app_id})")
            raise HTTPException(status_code=404, detail="No reviews found")
        
        logger.info(f"Successfully fetched {len(reviews)} reviews")
        
        response = ReviewResponse()
        reviews = analyze_reviews_sentiment(reviews)
        logger.debug("Sentiment analysis completed")

        if include_llm_overview:
            response.llm_overview = generate_overview(reviews)
            logger.debug("LLM overview generation completed") 

        if include_metrics or include_plots:
            metrics = calculate_metrics(reviews)
            logger.debug("Metrics calculation completed")

        if include_metrics:
            response.metrics = metrics

        if include_plots:
            response.plots = generate_plots(metrics, app_name=app_name)
            logger.debug("Plots generation completed")

        if include_raw_data:
            response.raw_data = {"reviews": [review.model_dump() for review in reviews]}
            logger.debug("Raw data prepared")
        
        logger.info("Successfully processed all requested data")
        return response
        
    except Exception as e:
        logger.error(f"Error processing reviews: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
