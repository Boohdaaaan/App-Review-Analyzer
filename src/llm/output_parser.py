import re
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser


class XMLToMarkdownParser(BaseOutputParser):
    """Parser that converts XML-style tags to markdown headers."""

    def parse(self, text: str) -> str:
        try:
            pattern = r'<(\w+)>(.*?)</\1>'

            def replace_match(match):
                tag = match.group(1)
                content = match.group(2).strip()
                header = tag.replace('_', ' ').title()

                return f"**{header}**:\n{content}\n\n"

            result = re.sub(pattern, replace_match, text, flags=re.DOTALL)
            result = re.sub(r'\n{3,}', '\n\n', result)

            return result.strip()
            
        except Exception as e:
            raise OutputParserException(f"XMLToMarkdownParser failed to parse XML tags to markdown: {str(e)}")

    @property
    def _type(self) -> str:
        return "xml_to_markdown_parser"