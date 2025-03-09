from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

from src.llm.jinja_config import DEFAULT_FORMATTER_MAPPING  # noqa: F401


with (
    Path(__file__).parent.joinpath("system.jinja2").open("r") as f_system,
    Path(__file__).parent.joinpath("human.jinja2").open("r") as f_human,
):
    OVERVIEW_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(f_system.read().strip(), template_format="jinja2"),
            HumanMessagePromptTemplate.from_template(f_human.read().strip(), template_format="jinja2"),
        ]
    )
