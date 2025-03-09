from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from enum import StrEnum


class Sentiment(StrEnum):
    VERY_NEGATIVE = "Very Negative"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    POSITIVE = "Positive"
    VERY_POSITIVE = "Very Positive"


class Review(BaseModel):
    review_id: str | None = None
    source: Literal["app_store", "google_play_market"]
    user_name: str
    country: str
    rating: int = Field(..., ge=1, le=5)
    sentiment: Sentiment | None = None
    review_text: str
    date: datetime
