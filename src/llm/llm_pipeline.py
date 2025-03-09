import os
import logging
from fastapi import HTTPException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSerializable

from src.models import Review
from src.llm.prompts import OVERVIEW_PROMPT
from src.llm.chat_models import get_anthropic_llm

logger = logging.getLogger(__name__)


def _get_lcel_pipeline(llm) -> RunnableSerializable[list[Review], str]:
    bs = int(os.getenv("LLM_BATCH_SIZE", 50))
    split_reviews_chain = RunnableLambda(lambda x: [x[i:i + bs] for i in range(0, len(x), bs)])
    single_analyze_chain: RunnableSerializable = OVERVIEW_PROMPT | llm | StrOutputParser()

    def loop_func(reviews_batches):
        summary = ""
        for batch in reviews_batches:
            summary = single_analyze_chain.invoke({"reviews": batch, "summary": summary})

        return summary

    lcel_pipeline = (
        split_reviews_chain
        | loop_func
    )
    
    return lcel_pipeline


def generate_summary(reviews: list[Review]) -> str:
    try:
        llm = get_anthropic_llm()
        chain = _get_lcel_pipeline(llm)
        return chain.invoke(reviews)
    except Exception as e:
        logger.error(f"Error generating overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))
