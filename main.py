import identifier
import json_formatting
import make_dictionary
import request_html
import parse
import choice


def program():
    identifier.header()

    home_url = "https://czasopisma.marszalek.com.pl"

    # getting home page html
    home_html = request_html.get_html(home_url)

    # parsing home html
    home_spooned = parse.html_spoon(home_html)
    # print(home_spooned)  # prints it cleaned in text format
    home_data = parse.home_database(home_spooned) # has selected bits and pieces from the html soup
    # print(home_data)

    choice.helper(home_data)  # prints what's in the home data

    # starting the choice loop
    chosen_journal_number = choice.event(home_data)

    # getting html from the chosen journal URL
    journal_html = request_html.get_html(home_data[chosen_journal_number][1])
    journal_spooned = parse.html_spoon(journal_html)
    # print(journal_spooned)

    # parsing the journal html into a dictionary
    journal_data, issue_data = parse.journal_data_pieced(home_url, journal_spooned)
    # print(journal_data)
    # print(issue_data)

    journal_dict = parse.journal_dict_parsing(journal_spooned, home_data[chosen_journal_number])
    # print(journal_dict)

    # parse all the article info and get their htmls
    # update journal dict by issues and volumes
    article_htmls, journal_dict = parse.get_article_htmls(journal_data, issue_data, journal_dict)
    # print(article_htmls)
    # print(journal_dict)

    # parse article info and get data
    journal_dict = parse.get_articles_data(article_htmls, journal_dict)
    # print(journal_dict)
    print("\n")

    # creating json file
    json_formatting.create_json(journal_dict)

    # create_db(basic_journal_info, basic_issue_data, article_data)


if __name__ == '__main__':
    program()
