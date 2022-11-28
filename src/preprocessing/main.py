import spacy
import random
import json
from tqdm import tqdm
from spacy.tokens import DocBin

import DatasetCollector
import TextPreprocessor

"""
To collect data:
1) Ran a query towards Wikisource SPARQL that is written below. It will collect the story titles
that fit our requirements.
2) Save as a json file.
3) If you want to exclude some files from the set, add the to the filtered titles list file.
4) Now we need to collect the story texts themselves from the titles and the years.
Run this module to collect the data and then chunk it into smaller pieces, appropriate for
feeding into the neural network, and then convert them into Spacy-readable format.

All done!
"""

"""
Query:

SELECT DISTINCT ?item ?itemLabel ?authorLabel ?P577_0 ?wikisourceSitelink WHERE {
  ?wikisourceSitelink schema:isPartOf <https://en.wikisource.org/>;
                      schema:about ?item.
  ?item p:P577 [psv:P577 [wikibase:timeValue ?P577_0]].
  ?item p:P50 [(ps:P50/(wdt:P279*)) ?author].
  ?item p:P6216 [(ps:P6216/(wdt:P279*)) wd:Q19652].
  ?item p:P407 [(ps:P407/(wdt:P279*)) wd:Q1860].
  # ?item p:P1957 [(ps:P1957) ?source].
  ?item p:P31 [(ps:P31) wd:Q7725634].
  ?item p:P7937 [(ps:P7937/(wdt:P279*)) wd:Q49084].
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}
Add SKIP and LIMIT as appropriate if the query times out.
"""

RAW_QUERY_PATH = "../../corpus/query2.json"
DATA_PATH = "../../data/data.json"
FILTERED_PATH = "../../data/cannot_load.json"


def category(year):
    if year < 1900:
        return {"<1900": True, "1900-1930": False, ">1930": False}
    elif year < 1930:
        return {"<1900": False, "1900-1930": True, ">1930": False}
    else:
        return {"<1900": False, "1900-1930": False, ">1930": True}


def make_docs(data):
    """
    this will take a list of texts and labels  and transform them in spacy documents
    data: list(tuple(text, label))
    returns: List(spacy.Doc.doc)
    """

    docs = []
    # nlp.pipe([texts]) is way faster than running
    # nlp(text) for each text
    # as_tuples allows us to pass in a tuple,
    # the first one is treated as text
    # the second one will get returned as it is.

    data_tuples = [(text["text"], text) for text in data]

    for text, context in tqdm(nlp.pipe(data_tuples, as_tuples=True), total=len(data_tuples)):
        # we need to set the (text)cat(egory) for each document
        text.cats = category(context["year"])
        # put them into a nice list
        docs.append(text)
        print(context["title"], "processed")

    # print(docs[:5])
    return docs


def input_yn(prompt: str):
    ans = ""
    while ans != "y" and ans != "n":
        ans = input(prompt + " (y/n) ")
    return ans == "y"


if __name__ == '__main__':

    collect = input_yn("Collect data by query?")
    if collect:
        DatasetCollector.DatasetCollector.main(DATA_PATH, RAW_QUERY_PATH, FILTERED_PATH)

    chunk = input_yn("Chunk data?")
    if chunk:
        data = json.load(open(DATA_PATH, "rb"))
        preprocessor = TextPreprocessor.TextPreprocessor(data=data)
        preprocessor.chunk_all("data_chunked_full.json")

    prep_spacy = input_yn("Prepare data for Spacy?")
    if prep_spacy:
        nlp = spacy.load("en_core_web_sm")
        data = json.load(open("../../data/data_chunked_full.json", "rb"))
        random.shuffle(data)
        n_text = 900  # 1098
        train_docs = make_docs(data[:n_text])
        # then we save it in a binary file to disc
        doc = DocBin(docs=train_docs)
        doc.to_disk("../../data/train.spacy")  # repeat for validation data
        test_docs = make_docs(data[n_text:])
        doc = DocBin(docs=test_docs)
        doc.to_disk("../../data/test.spacy")
