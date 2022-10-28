import json

from TextPrerocessor import TextPreprocessor
from WikisourceQuerySender import WikisourceQuerySender

SOURCES_LIST = ['The_Last_Leaf_(Henry)']

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

