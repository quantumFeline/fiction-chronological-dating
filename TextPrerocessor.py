import string
import io

import spacy


class TextPreprocessor:

    def __init__(self, file: object = None, filename: string = "input.txt"):
        if file:
            self.file = file
        else:
            self.file = open(filename, "r")

    def __del__(self):
        self.file.close()

    def process(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.file.read())
        for token in doc:
            print(token.text, token.pos_, token.dep_)


if __name__ == "__main__":
    with io.StringIO() as f:
        f.write("Short text. Second sentence in the text.")
        f.seek(0)
        preprocessor = TextPreprocessor(f)
        preprocessor.process()
