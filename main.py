import identifier
import parse


def program():
    identifier.header()

    home_url = ('https://czasopisma.marszalek.com.pl')

    parse.get_html(home_url)


if __name__ == '__main__':
    program()
