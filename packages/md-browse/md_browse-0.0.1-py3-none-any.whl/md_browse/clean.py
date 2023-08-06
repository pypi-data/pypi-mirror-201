from bs4 import Comment
from  bs4.element import Tag
from typing import Iterable


def clean(body: Tag) -> Tag:
    """Clean an HTML element by:
    1. Removing <head>, <script>, <style> and <noscript> elements and their contents.
    2. Replacing <span> elements with their contents. 
    3. Removing all attributes except 'src', 'alt', 'href' and 'srcset' from all elements except <a> and <img>."""
    
    TAGS_THAT_CAN_KEEP_THEIR_ATTRS = ["a", "img"]
    ATTRIBUTES_ALLOWED_TO_KEEP = ["src", "alt", "href", "srcset"]
    BLOCKED_TAGS = ["style", "script", "noscript", "head"]
    REPLACED_TAGS = ["span"]

    return _clean(body, 
                 blocked_tags=BLOCKED_TAGS, 
                 replaced_tags=REPLACED_TAGS, 
                 tags_that_can_keep_their_attrs =TAGS_THAT_CAN_KEEP_THEIR_ATTRS,
                 allowed_attrs = ATTRIBUTES_ALLOWED_TO_KEEP)


def _clean(tag: Tag, *, blocked_tags: Iterable[str], replaced_tags: Iterable[str], tags_that_can_keep_their_attrs: Iterable[str], allowed_attrs: Iterable[str]) -> Tag:
    for element in tag(text=lambda text: isinstance(text, Comment)):
        element.extract()
    for t in tag.find_all(blocked_tags):
        t.decompose()
    for t in tag.find_all(replaced_tags):
        t.unwrap()

    for t in tag.find_all():
        if t.name not in tags_that_can_keep_their_attrs:
            t.attrs.clear()
        else:
            t.attrs = {k:v for k, v in t.attrs.items() if k in allowed_attrs}
    return tag