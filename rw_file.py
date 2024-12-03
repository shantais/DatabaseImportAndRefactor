import json
import os


def rw(journal_dict):

    file_name = "journals_data3.json"
    journal_name = journal_dict['name']
    journal_dict.pop('name')

    if os.path.exists(file_name):
        # read existing file and update new data
        with open(file_name, mode="r", encoding="utf-8") as f:
            journals_loaded_dict = json.load(f)
        journals_loaded_dict.update({journal_name: journal_dict})
    else:
        journals_loaded_dict = {journal_name: journal_dict}

    with open(file_name, mode="w", encoding="utf-8") as f:
        json.dump(journals_loaded_dict, f, indent=4)