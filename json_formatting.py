import json

def create_json(journal_dict):
    journal_json = json.dumps(journal_dict, indent=4)
    return journal_json
