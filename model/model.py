import spacy

from tqdm.auto import tqdm

train = "../data/train.spacy"
test = "../data/test.spacy"

nlp = spacy.load("en_core_web_sm")
