import json


def create_json(journal_dict, issue_dict, article_dict, author_dict):
    journal_json = json.dumps(journal_dict, indent=4)
    issue_json = json.dumps(issue_dict, indent=4)
    article_json = json.dumps(article_dict, indent=4)
    author_json = json.dumps(author_dict, indent=4)

    # witing json to file
    with open(f"{journal_dict["abbr"]}.json", mode="w", encoding="utf-8") as outfile:
        outfile.write(journal_json)