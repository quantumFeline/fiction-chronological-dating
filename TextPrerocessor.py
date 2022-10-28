import json
import string
import io
import tempfile

import spacy
from spacy.lang.en import English  # updated
from numpy import random as nrandom


class TextPreprocessor:

    def __init__(self, filename: string = "input.txt", data: object = None):
        self.filename = filename
        if data:
            self.data = data
        else:
            with open(self.filename) as datafile:
                self.data = json.load(datafile)

    def chunk_item(self, item: dict, chunk_size: int = 1000, n_chunks: int = 10) -> list:
        print(item)
        title, text, year = item["title"], item["text"], item["year"]
        # We do not cut the text into perfect non-overlapping pieces; they may overlap.
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        sentences = list(doc.sents)
        print(sentences)
        print(sentences[0].sent)
        rands = nrandom.randint(0, len(sentences), n_chunks)
        chunks = []
        for i in rands:
            chunk = ""
            for k in range(i, len(sentences)):
                if len(chunk) + len(sentences[k]) + 1 > chunk_size:
                    break
                chunk += " " + str(sentences[k])
            chunks.append({"title": title, "text": chunk, "year": year})
        return chunks

    def process(self):
        items = self.chunk_item(self.data[0])
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(items[0]["text"])
        for token in doc:
            print(token.text, token.pos_, token.dep_, token.lemma_, token.tag_,
                  token.shape_, token.is_alpha, token.is_stop, token.has_vector, token.vector_norm, token.is_oov)

        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

        return items


if __name__ == "__main__":
    with tempfile.NamedTemporaryFile() as f:
        data = [{"title": "", "text": "Short text. Second sentence in the text.", "year": 1000}]
        preprocessor = TextPreprocessor(data=data)
        preprocessor.process()
