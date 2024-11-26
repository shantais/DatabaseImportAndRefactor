import json

def create_json(journal_dict):
    journal_json = json.dumps(journal_dict, indent=4)
    print(journal_json)

    # # todo: read the file and update existing json if exists
    # with open("journals.json", mode="rw", encoding="utf-8") as file:
    #     file.write(journal_json)