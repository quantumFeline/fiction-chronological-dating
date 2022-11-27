import json
import string
import time

import requests


class WikisourceQuerySender:
    def __init__(self):
        self.last_query_result = None
        pass

    def composeQuery(self, name) -> string:
        return f"https://en.wikisource.org/w/api.php?action=query&prop=extracts&titles={name}" \
                "&explaintext&format=json&formatversion=2"

    def parse(self, entry: dict) -> dict:
        title = entry["itemLabel"]
        query_title = entry["wikisourceSitelink"].split("wiki/")[1]  # take only the article name
        year = int(entry["P577_0"][:4])  # First four digit in the time format used are the year.
        # We do not need the exact day of publication
        # author = entry["authorLabel"]
        text = self.getText(query_title)
        if text == '':
            self.last_query_result = None
        else:
            self.last_query_result = {"title": title, "text": text, "year": year}
        return self.last_query_result

    def is_version_page(self, name) -> bool:
        query_categories = "https://en.wikisource.org/w/api.php?action=query&prop=categories" \
                          f"&titles={name}&formatversion=2&format=json"
        try:
            categories = str(requests.get(query_categories).json()['query']['pages'][0]['categories'])
        except KeyError:  # No categories, then it's the text page, we can use it
            return False
        return categories.count("Category:Versions pages") != 0

    def getText(self, name: string) -> string:
        if self.is_version_page(name):
            return ''
        r = requests.get(self.composeQuery(name))
        doc = r.json()['query']['pages'][0]
        text = doc['extract']
        return text
