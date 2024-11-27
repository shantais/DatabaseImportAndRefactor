import json_formatting


def rw(journal_dict):

    # creating json file
    journal_json = json_formatting.create_json(journal_dict)

    # todo: read the file and update existing json if exists
    with open("journals.json", mode="rw", encoding="utf-8") as file:
        file.write(journal_json)