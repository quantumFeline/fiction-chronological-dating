import json

from TextPrerocessor import TextPreprocessor
from WikisourceQuerySender import WikisourceQuerySender

SOURCES_LIST = ['The_Last_Leaf_(Henry)', 'Beyond_Lies_the_Wub', 'The_Picture_in_the_House',
                'Amy_Foster', 'The_Street', 'Polaris', 'Ex_Oblivione', 'Poetry_and_the_Gods',
                'The_Book_of_Wonder', 'The_Gateway_of_the_Monster', 'Hop-Frog_(unsourced)',
                'Three_Sundays_in_a_Week', 'The_Business_Man', 'The_White_Ship_(Lovecraft)',
                'Lot_No._249', 'The_Red_Room', 'Transcendental_Wild_Oats', 'The_Dreams_in_the_Witch-House',
                'The_Village_That_Voted_the_Earth_Was_Flat']
'''
Wiki query:

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
LIMIT 500

'''

if __name__ == '__main__':

    data = []
    for source in SOURCES_LIST:
        sender = WikisourceQuerySender()
        data.append(sender.parse(source))

    f = open("data.json", "w")
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

    preprocessor = TextPreprocessor("data.json")
    chunks = preprocessor.process()

    f_chunk = open("data_chunked.json", "w")
    json.dump(chunks, f_chunk, ensure_ascii=False, indent=4)
    f_chunk.close()

