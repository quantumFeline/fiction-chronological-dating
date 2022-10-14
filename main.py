import json

SLAVIC_LANGUAGES = ["Belarusian", "Bulgarian", "Czech",  "Macedonian", "Old Church Slavonic", "Polish", "Russian",
                    "Serbo-Croatian", "Slovak", "Slovene", "Ukrainian"]

if __name__ == '__main__':
    output = open("translations.txt", "w")
    with open('raw-wiktextract-data.json', 'r') as f:
        data = []
        for i in range(100000):
            obj = json.loads(f.readline())
            # print(json.dumps(obj, indent=2, sort_keys=True))
            if 'lang' in obj:
                if obj['lang'] != "Translingual":
                    data.append(obj)
                else:
                    pass
                    # print(obj['word'], "no lang")
        for obj in data:
            # print(json.dumps(obj, indent=2))
            if 'translations' in obj:
                print(obj["word"], file=output)
                for tr in obj['translations']:
                    try:
                        if tr["lang"] in SLAVIC_LANGUAGES:
                            print("\t", tr["lang"], tr["word"], file=output)
                    except KeyError:
                        print("Error. ", tr, file=output)
