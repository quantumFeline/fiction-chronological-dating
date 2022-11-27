import DatasetCollector
import json
import TextPreprocessor

"""
To collect data:
1) Ran a query towards Wikisource SPARQL that is written below. It will collect the story titles
that fit our requirements.
2) Save as a json file.
3) If you want to exclude some files from the set, add the to the filtered titles list file.
4) Now we need to collect the story texts themselves from the titles and the years.
Run this module to collect the data and then chunk it into smaller pieces, appropriate for
feeding into the neural network.

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

if __name__ == '__main__':
    DatasetCollector.DatasetCollector.main(DATA_PATH, RAW_QUERY_PATH, FILTERED_PATH)

    data = json.load(open(DATA_PATH, "rb"))
    preprocessor = TextPreprocessor.TextPreprocessor(data=data)
    preprocessor.chunk_all("data_chunked_full.json")
