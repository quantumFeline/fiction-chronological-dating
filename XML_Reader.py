import xml.sax as sax
import xml.etree.ElementTree as ET


def read_xml():
    parser = ET.XMLPullParser(['start', 'end'])
    i = 0
    with open('enwikisource-20221020-pages-articles-multistream.xml', "rb") as f:
        while True:
            line = f.readline()
            print("Line:", line.replace("\n".encode('utf-8'), "\\n".encode('utf-8')))
            parser.feed(line)
            for event, elem in parser.read_events():
                print(event, elem.text)
                #print(elem.tag, 'text=', elem.text)
                print("\n\n")
            i += 1
            if i > 1000:
                return
    # context = ET.iterparse('enwikisource-20221020-pages-articles-multistream.xml', events=("start", "end"))
    #
    # for index, (event, elem) in enumerate(context):
    #     print(index, event, elem)
    #     if elem.tag == "text":
    #         print("Text!")
    #     # # Get the root element.
    #     # if index == 0:
    #     #     root = elem
    #     #     print(root)
    #     # if event == "end" and elem.tag == "record":
    #     #     # ... process record elements ...
    #     #     root.clear()


if __name__ == "__main__":
    read_xml()
