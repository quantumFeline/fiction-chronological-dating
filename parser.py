from wiktextract import (WiktionaryConfig, parse_wiktionary, parse_page,
                         PARTS_OF_SPEECH)
from wikitextprocessor import Wtp, ALL_LANGUAGES

config = WiktionaryConfig(
             capture_languages=["English", "Polish", "Translingual"],
             capture_translations=True,
             capture_pronunciation=False,
             capture_linkages=False,
             capture_compounds=False,
             capture_redirects=False,
             capture_examples=False,
             capture_etymologies=False)
path = "plwiktionary-20211220-pages-meta-current.xml/plwiktionary-20211220-pages-meta-current.xml"
ctx = Wtp()


def word_cb(data):
    # data is dictionary containing information for one word/redirect
    pass
    # ... do something with data


parse_wiktionary(ctx, path, config, word_cb)
