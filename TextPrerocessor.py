import json
import string
import io
import tempfile

import spacy


class TextPreprocessor:

    def __init__(self, filename: string = "input.txt", data: object = None):
        self.filename = filename
        if data:
            self.data = data
        else:
            with open(self.filename) as datafile:
                self.data = json.load(datafile)

    def process(self):
        item = self.data[0]
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(item["text"])
        for token in doc:
            print(token.text, token.pos_, token.dep_, token.lemma_, token.tag_,
                  token.shape_, token.is_alpha, token.is_stop, token.has_vector, token.vector_norm, token.is_oov)

        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)


if __name__ == "__main__":
    with tempfile.NamedTemporaryFile() as f:
        data = [{"title": "", "text": "Short text. Second sentence in the text.", "year": 1000}]
        preprocessor = TextPreprocessor(data=data)
        preprocessor.process()
