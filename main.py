import identifier
import make_dictionary
import request_html
import parse
import choice
import db_formatting
from db_formatting import create_db


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

    # parsing the journal html
    journal_data, issue_data = parse.journal_database(home_url, journal_spooned)
    # print(journal_data)
    # print(issue_data)
    basic_journal_info = parse.journal_basic_info_get(journal_spooned, home_data[chosen_journal_number])
    journal_dict = make_dictionary.journal(basic_journal_info)
    print(journal_dict)

    # parse all the article info and get their htmls
    article_htmls, basic_issue_data = parse.get_article_htmls_and_basic_issue_data(journal_data, issue_data)
    # print(article_htmls)
    # print(basic_issue_data)

    issue_dict = make_dictionary.issue(basic_issue_data, basic_journal_info)
    print(issue_dict)

    # parse article info and get data
    article_data = (parse.get_articles_data(article_htmls))
    # print(article_data)

    article_dict, author_dict = make_dictionary.article_and_author(article_data)
    print(article_dict)
    print(author_dict)

    # create_db(basic_journal_info, basic_issue_data, article_data)


if __name__ == '__main__':
    program()
