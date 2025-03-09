import torch
from transformers import pipeline
from functools import lru_cache


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """
    Creates and returns a cached sentiment analysis pipeline.
    The pipeline is cached to avoid recreating it on every call.

    Returns:
        Pipeline: A HuggingFace pipeline for multilingual sentiment analysis
    """
    sentiment_pipeline = pipeline(
        task="text-classification",
        model="tabularisai/multilingual-sentiment-analysis", 
        max_length=512,
        truncation=True,
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    return sentiment_pipeline
