import os
from langchain_anthropic import ChatAnthropic
from functools import lru_cache


@lru_cache(maxsize=1)
def get_anthropic_llm() -> ChatAnthropic:
    """
    Creates and returns a cached LangChain chat model.
    The model is cached to avoid recreating it on every call.

    Returns:
        ChatAnthropic: A LangChain chat model.
    """
    llm = ChatAnthropic(
        model=os.getenv("ANTHROPIC_MODEL"),
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        streaming=False,
        temperature=os.getenv("ANTHROPIC_TEMPERATURE"),
        max_retries=3,
    )
    return llm
