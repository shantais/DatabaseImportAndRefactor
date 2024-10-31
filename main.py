import identifier
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

    # parsing the journal html
    journal_data = parse.journal_database(home_url, journal_spooned)
    print(journal_data)
    basic_journal_info = parse.journal_basic_info_get(journal_spooned) # todo: use later for journal db content

    # parse all the article info and get their htmls
    issue_htmls = parse.get_article_htmls(journal_data)
    # print(issue_htmls)

    # parse article info and get data
    # article_data = (
    parse.get_articles_data(issue_htmls) # )


    # todo: put the info in a database format to file


if __name__ == '__main__':
    program()
