from bs4.element import Tag
import json

class Link:
    def __init__(self, tag: Tag):
        result_title = tag.select_one('.result__title')
        if result_title:
            self.title = result_title.text.strip()

        result_snippet = tag.select_one('.result__snippet')
        if result_snippet:
            self.href = result_snippet.attrs.get('href').strip()
            self.description = result_snippet.text.strip()

    def __repr__(self) -> str:
        return f"{self.title}\n{self.description}"


class LinkEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Link):
            return {
                "title": obj.title,
                "href": obj.href,
                "description": obj.description
            }
        return json.JSONEncoder.default(self, obj)