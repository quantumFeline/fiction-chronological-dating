import tempfile

import spacy


def find_terminology(item, nlp):
    title, text, year = item["title"], item["text"], item["year"]
    doc = nlp(text)
    print("Named entities:")
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
    print("")
    pass


if __name__ == "__main__":
    with tempfile.NamedTemporaryFile() as f:
        data = [{"title": "", "text": "Short text. Second sentence in the text.", "year": 1000}]
        nlp = spacy.load("en_core_web_sm")
        for item in data:
            find_terminology(item, nlp)
