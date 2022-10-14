import string

import requests


class WikisourceQuerySender:
    def __init__(self):
        pass

    def parse(self, name: string) -> string:
        query = f"https://en.wikisource.org/w/api.php?action=query&prop=revisions&titles={name}&format=json&rvslots=*&rvprop=content&formatversion=2"
        r = requests.get(query)
        print(r.json()['query']['pages'][0]['revisions'][0]['slots']['main']['content'])


if __name__ == "__main__":
    sender = WikisourceQuerySender()
    sender.parse('The_Last_Leaf_(Henry)')
