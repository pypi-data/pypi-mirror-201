#! /usr/bin/env python3

import argparse
import json
import urllib.parse
from typing import List

import requests
from bs4 import BeautifulSoup

from .models import Link, LinkEncoder

BASE_URL = "https://html.duckduckgo.com/html/?q="


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('-H', '--headers-only', action="store_true")
    parser.add_argument('-j', '--json-output', action="store_true")
    return parser.parse_args()

def _url_encode_query(query: str) -> str:
    return urllib.parse.quote_plus(query)


def _request(query):
    url = f"{BASE_URL}{query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    r = requests.get(url=url, headers=headers)
    return r.text

def _extract_links(result_html: str) -> List[Link]:
    soup = BeautifulSoup(result_html, features="html.parser")

    links = soup.select('.links_main.links_deep.result__body')
    links = [Link(link) for link in links]
    return links

def search(query: str) -> List[Link]:
    """Given `query`, search duck-duck-go and return a list of `Link` objects."""
    query = _url_encode_query(query)
    result_html = _request(query)
    
    return _extract_links(result_html)

def cheap_markdownify(link: Link):
    return f"## [{link.title}]({link.href})\n\n{link.description}"

def main():
    args = _parse_args()
   
    links = search(args.query)

    json_str = json.dumps(links, cls=LinkEncoder, indent=2)

    # TODO consider losing this functionality
    if args.json_output:
        print(json_str)

    elif args.headers_only:
        for l in links:
            print(l.title.lower().strip())
    else:
        print("\n\n".join([cheap_markdownify(l) for l in links]))





if __name__ == "__main__":
    main()