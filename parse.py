import bs4
import string

def html_spoon(html_home):
    html_soup = bs4.BeautifulSoup(html_home, 'html.parser')
    return html_soup


def home_database(html_soup):
    data = []
    print('')
    for idx, item in enumerate(html_soup.find_all('a', class_="uk-link-reset")):
        # print(item)
        line = [str(idx+1), item['href'], item.get_text()]
        data.append(line)
    return data

def journal_database(home_url, journal_soup):
    data = []
    ul_class = journal_soup.find_all('h3', class_='page-header item-title')
    for idx, item in enumerate(ul_class):
        if not item.find('span'):
            details = item.find('a')
            line = [idx, home_url + details['href'], details.get_text().strip()]
            data.append(line)
    return data

def issn_get(journal_soup):
    mop = []
    shit = journal_soup.find('form', class_='magazineData mceNonEditable')
    # print(shit)

    for item in shit.children:
        # print(item)
        mop.append(item['value'])
    # print(mop)
    issn = mop[2]
    return issn

def journal_basic_info_get(journal_soup):
    find_info = journal_soup.find("form", class_="magazineData mceNonEditable")
    # print(find_info)
    input_values = [input_tag.get('value', '') for input_tag in find_info.find_all('input')]
    # print(input_values)
    return input_values

