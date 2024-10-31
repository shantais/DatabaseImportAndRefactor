import bs4
import request_html


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
    print(ul_class)
    for idx, item in enumerate(ul_class):
        if not item.find('span'):
            details = item.find('a')
            line = [idx, home_url + details['href'], details.get_text().strip()]
            data.append(line)
    return data


def journal_basic_info_get(journal_soup):
    find_info = journal_soup.find("form", class_="magazineData mceNonEditable")
    # print(find_info)
    input_values = [input_tag.get("value", '') for input_tag in find_info.find_all('input')]
    # print(input_values)
    return input_values

def get_article_htmls(journal_data):
    all_htmls = []
    for issue in journal_data:
        html = html_spoon(request_html.get_html(issue[1]))
        # print(html)
        article_class = html.find_all("article", class_='uk-article')
        # print(article_class)
        for article in article_class:
            all_htmls.append(article.get("data-permalink", ''))

    return all_htmls


            # title = article.find('a').get_text().strip()
            # print(title)
            #
            # year = article.find("li", class_="field-entry year yearField").find("span", class_="field-value").get_text().strip()
            # print(year)
            #
            # pages = article.find("li", class_="field-entry pages pagesField").find("span", class_="field-value").get_text().strip()
            # print(pages)
            # if '-' in pages:
            #     pages = pages.split('-')
            # elif '–' in pages:
            #     pages = pages.split('–')
            #
            # doi = article.find("li", class_="field-entry doi-number doiField").find("span", class_="field-value").get_text().strip()
            # print(doi)
            #
            # abstract = article.find("div", class_="uk-margin-medium-top").get_text().strip()
            # print(abstract)





