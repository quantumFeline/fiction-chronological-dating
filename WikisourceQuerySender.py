import re
import string

import requests


class WikisourceQuerySender:
    def __init__(self):
        pass

    def parse(self, name: string) -> dict:
        query = f"https://en.wikisource.org/w/api.php?action=query&prop=extracts&titles={name}" \
                "&explaintext&format=json&rvslots=*&rvprop=content&formatversion=2"
        query_categories = "https://en.wikisource.org/w/api.php?action=query&prop=categories" \
                           f"&titles={name}&formatversion=2&format=json"
        r = requests.get(query)
        categories = str(requests.get(query_categories).json()['query']['pages'][0]['categories'])
        # FIXME: Hack. Probably better to use wikidata SPARQL query
        # (or use dumps which might be better for large amounts of data)
        # print(categories)
        year = int(re.search("(?<=(Category:))[0-9]+(?=( works))", categories).group(0))
        doc = r.json()['query']['pages'][0]
        title = doc['title']
        text = doc['extract']
        # print(title)
        # print(year)
        return {"title": title, "text": text, "year": year}


if __name__ == "__main__":
    sender = WikisourceQuerySender()
    sender.parse('The_Last_Leaf_(Henry)')
