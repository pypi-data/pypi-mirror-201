import re

from markdownify import markdownify as md
from bs4.element import Tag


def convert_to_markdown(cleaned_body: Tag) -> str:
    body_str = str(cleaned_body)
    markdown = md(body_str)
    
    # Keep at most 2 adjacent newlines
    markdown = markdown.replace("\r\n","\n")
    markdown = re.sub("\n{2,}", "\n\n", markdown)
    
    return markdown