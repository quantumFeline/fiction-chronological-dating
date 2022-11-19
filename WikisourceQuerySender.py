import json
import re
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


RAW_QUERY_PATH = "query2.json"
DATA_PATH = "data.json"
FILTERED_PATH = "cannot_load.json"
add_filter = ["An Outpost of Progress", "The Machine Stops", "The Merry Men", "Rogues in the House", "Markheim",
              "The Tower of the Elephant", "The Pool of the Black One", "The Story of Mimi-Nashi-H\u014d\u00efchi",
              "Xuthal of the Dusk", "The Merry Men and Other Tales and Fables", "Black Colossus",
              "Beyond the Black River", "The King of the Golden River"]

if __name__ == "__main__":
    sender = WikisourceQuerySender()
    with open(DATA_PATH, "rb") as f_data:
        data = json.load(f_data)
        titles = set([item["title"] for item in data])
    with open(FILTERED_PATH, "rb") as filtered:
        filtered_titles = set(json.load(filtered) + add_filter)

    with open(RAW_QUERY_PATH, "rb") as fq:
        book_names = json.load(fq)
        for entry in book_names:
            next_command = input()
            if next_command == "q":
                break

            title = entry["itemLabel"]
            if title in titles:
                print(f"{title} already loaded")
                continue
            elif title in filtered_titles:
                print(f"Can't load {title}")
                continue

            entry_parsed = sender.parse(entry=entry)
            print(entry_parsed)
            if entry_parsed:
                data.append(entry_parsed)
            else:
                filtered_titles.add(title)
            time.sleep(1)
    with open(DATA_PATH, "w") as f_data:
        json.dump(data, f_data, indent=4)
    with open(FILTERED_PATH, "w") as f_filtered:
        json.dump(list(filtered_titles), f_filtered, indent=1)


# UNUSED
# query_categories = "https://en.wikisource.org/w/api.php?action=query&prop=categories" \
#                   f"&titles={name}&formatversion=2&format=json"
# categories = str(requests.get(query_categories).json()['query']['pages'][0]['categories'])
# (or use dumps which might be better for large amounts of data)
# print(categories)
# try:
#     year = int(re.search("(?<=(Category:))[0-9]+(?=( works))", categories).group(0))
# except RuntimeError: # No category found
#     year = 0