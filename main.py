import json

from TextPrerocessor import TextPreprocessor
from WikisourceQuerySender import WikisourceQuerySender

SOURCES_LIST = ['The_Last_Leaf_(Henry)', 'Beyond_Lies_the_Wub', 'The_Picture_in_the_House',
                'Amy_Foster', 'The_Street', 'Polaris', 'Ex_Oblivione', 'Poetry_and_the_Gods',
                'The_Book_of_Wonder', 'The_Gateway_of_the_Monster', 'Hop-Frog_(unsourced)',
                'Three_Sundays_in_a_Week', 'The_Business_Man', 'The_White_Ship_(Lovecraft)',
                'Lot_No._249', 'The_Red_Room', 'Transcendental_Wild_Oats', 'The_Dreams_in_the_Witch-House',
                'The_Village_That_Voted_the_Earth_Was_Flat']

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

