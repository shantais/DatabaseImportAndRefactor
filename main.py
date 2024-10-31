import identifier
import request_html
import parse


def program():
    identifier.header()

    home_url = "https://czasopisma.marszalek.com.pl"

    # getting home page html
    home_html = request_html.get_html(home_url)

    # parsing home html
    home_spooned = parse.html_spoon(home_html)
    # print(home_spooned)  # prints it cleaned in text format
    home_data = parse.home_database(home_spooned)
    print(home_data)  # has selected bits and pieces from the html soup

if __name__ == '__main__':
    program()
