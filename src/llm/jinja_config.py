from jinja2.sandbox import SandboxedEnvironment
from langchain_core.prompts.string import DEFAULT_FORMATTER_MAPPING

ENV = SandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)


def my_jinja2_formatter(template: str, **kwargs) -> str:
    return ENV.from_string(template).render(**kwargs)


def recursive_jinja2_formatter(template: str, **kwargs) -> str:
    MAX_DEPTH = 5
    res = template

    for _ in range(MAX_DEPTH):
        res = my_jinja2_formatter(res, **kwargs)
        if "{{" not in res and "{%" not in res:
            break

    return res


DEFAULT_FORMATTER_MAPPING["jinja2"] = recursive_jinja2_formatter
