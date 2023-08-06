#! /usr/bin/env python3

import sys
import argparse
from pathlib import Path
from .clean import clean
from .converttomarkdown import convert_to_markdown

import requests
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str)
    parser.add_argument('--file', type=str)
    parser.add_argument('--cache', action="store_true")

    return parser.parse_args()

def get_html_string(file: str or Path = None, url: str = None, cache: bool = False):
    """Returns a string, hopefully of <html></html>. Will return in order of precedence:
    `file`'s contents, `the response.text of a response object if `url` is provided, or `stdin`
    """
    if file:
        return Path(file).read_text()
    if url:
        r = requests.get(url)
        if cache:
            Path("r-html.html").write_text(r.text)
        return r.text
    return "".join(sys.stdin.readlines())

def load(url, cache=False):
    html_string = get_html_string(url=url, cache=cache)
    clean_and_convert_to_markdown(html_string)

def clean_and_convert_to_markdown(html_string: str):
    html = BeautifulSoup(html_string, features="html.parser")
    try:
        body = clean(html.body)
        print(convert_to_markdown(body))
    except TypeError:
        print("Unable to find <body> tag.")

def main():
    args = parse_args()
    html_string = get_html_string(args.file, args.url, args.cache)
    clean_and_convert_to_markdown(html_string)
    
if __name__ == "__main__":
    main()