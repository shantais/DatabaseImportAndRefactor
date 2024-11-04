from os.path import exists

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


def get_articles_data(article_htmls):
    article_info = []
    for html in article_htmls:
        html_soup = html_spoon(request_html.get_html(html))
        # print(html_soup)
        title = html_soup.find('h1').get_text().strip()
        # print(title)

        year = html_soup.find("li", class_="field-entry year yearField").find("span", class_="field-value").get_text().strip()
        # print(year)

        pages = html_soup.find("li", class_="field-entry pages pagesField").find("span", class_="field-value").get_text().strip()
        # print(pages)
        if '-' in pages:
            pages = pages.split('-')
        elif '–' in pages:
            pages = pages.split('–')

        doi = html_soup.find("li", class_="field-entry doi-number doiField").find("span", class_="field-value").get_text().strip()
        # print(doi)

        abstract_soup = []
        reference_list = []
        if html_soup.find("div", class_="uk-margin-medium-top"):
            abstract_soup = html_soup.find("div", class_="uk-margin-medium-top").find_all("p")
            reference_list = html_soup.find("div", class_="uk-margin-medium-top").find_all("li")


            for idx, p in enumerate(abstract_soup):
                if p.get_text().strip() == "REFERENCES:":
                    abstract_soup = abstract_soup[:idx]
                # print(p)
                # print(p.get_text().strip())
            # print(abstract_soup)
            # for r in reference_list:
            #     print(r.get_text().strip())

        authors = []
        for idx in range(9, 0, -1):
            if html_soup.find("li", class_=f"field-entry author-{idx} authorField"):
                author = html_soup.find("li", class_=f"field-entry author-{idx} authorField").find("span", class_="field-value").get_text().strip()
            else:
                author = '-'
            if html_soup.find("li", class_=f"field-entry author-{idx} authorField"):
                email = html_soup.find("li", class_=f"field-entry author-{idx} authorField").find("span", class_="field-value").get_text().strip()
            else:
                email = '-'
            if html_soup.find("li", class_=f"field-entry institution-{idx} institutionField"):
                institution = html_soup.find("li", class_=f"field-entry institution-{idx} institutionField").find("span", class_="field-value").get_text().strip()
            else:
                institution = '-'
            if html_soup.find("li", class_=f"field-entry orcid-{idx} orcidField"):
                orcid = html_soup.find("li", class_=f"field-entry orcid-{idx} orcidField").find("span", class_="field-value").get_text().strip()
            else:
                orcid = '-'
            authors.append([author, email, institution, orcid])
            authors = list(filter(lambda a: a != ['-', '-', '-', '-'], authors))
        # print(authors)

        article_info.append([title,abstract_soup, reference_list, authors, year, pages, doi])
    return article_info





