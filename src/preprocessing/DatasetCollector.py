import json
import time

from src.preprocessing.WikisourceQuerySender import WikisourceQuerySender

# add_filter = ["An Outpost of Progress", "The Machine Stops", "The Merry Men", "Rogues in the House", "Markheim",
#               "The Tower of the Elephant", "The Pool of the Black One", "The Story of Mimi-Nashi-H\u014d\u00efchi",
#               "Xuthal of the Dusk", "The Merry Men and Other Tales and Fables", "Black Colossus",
#               "Beyond the Black River", "The King of the Golden River"]
# # Files that could not have been read correctly for some reason, listed manually to exclude them from the dataset.


class DatasetCollector:

    @staticmethod
    def main(data_path, raw_query_path, filtered_path=None):
        sender = WikisourceQuerySender()
        with open(data_path, "rb") as f_data:
            data = json.load(f_data)
            titles = set([item["title"] for item in data])

        filtered_titles = {}
        if filtered_path:
            with open(filtered_path, "rb") as filtered:
                filtered_titles = set(json.load(filtered))

        with open(raw_query_path, "rb") as fq:
            book_names = json.load(fq)
            for entry in book_names:
                next_command = input()
                if next_command == "q":
                    break

                title = entry["itemLabel"]
                if title in titles:
                    print(f"{title} already loaded")
                    continue
                elif title in filtered_titles:
                    print(f"Can't load {title}")
                    continue

                entry_parsed = sender.parse(entry=entry)
                print(entry_parsed)
                if entry_parsed:
                    data.append(entry_parsed)
                else:
                    filtered_titles.add(title)

                time.sleep(1)  # so we don't DoS/get timed out by Wikisource

        with open(data_path, "w") as f_data:
            json.dump(data, f_data, indent=4)

        # Update the list of title our program was unable to read.
        with open(filtered_path, "w") as f_filtered:
            json.dump(list(filtered_titles), f_filtered, indent=1)
