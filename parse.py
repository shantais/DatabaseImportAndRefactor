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