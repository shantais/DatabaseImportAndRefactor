import bs4
import request_html
import json_formatting


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

def journal_data_pieced(home_url, journal_soup):
    journal_data = []
    issue_data = []
    ul_class = journal_soup.find_all('h3', class_='page-header item-title')
    # print(ul_class)
    for idx, item in enumerate(ul_class):
        details = item.find('a')
        if not item.find('span'):
            line = [home_url + details['href'], details.get_text().strip()]
            journal_data.append(line)
        else:
            line = [home_url + details['href'], details.get_text().strip()]
            issue_data.append(line)

    return journal_data, issue_data

def journal_dict_parsing(journal_spooned, home_data):
    find_info = journal_spooned.find("form", class_="magazineData mceNonEditable")
    # print(find_info)
    input_values = [input_tag.get("value", '') for input_tag in find_info.find_all('input')]
    input_values.insert(0, home_data[2])

    if str(home_data[1]).split("/")[4] == "10-15804":
        abbr = str(home_data[1]).split("/")[5]
    else:
        abbr = str(home_data[1]).split("/")[4]

    input_values.insert(1, abbr)
    print(input_values)
    # ['Medical Forum', 'mf', 'Półrocznik', 'XII', '2956-8099', '', 'medical sciences, health sciences, pharmacology and pharmacy, physical culture science']

    journal_dict = {input_values[0]: {
        "abbr": input_values[1],
        "freq": input_values[2],
        "months": input_values[3],
        "issn": input_values[4],
        "discipline_pl": input_values[5],
        "discipline_en": input_values[6]
    }}
    return journal_dict

def get_article_htmls(journal_data, issue_data, journal_dict):
    article_htmls = []
    j_name = list(journal_dict.keys())[0]
    # journal_dict[j_name] = {}

    for volume in issue_data:
        for issue in journal_data:
            if volume[0] in issue[0]:
                journal_dict[j_name].update({volume[1]: issue[1]})
                # print(volume)
                # print(issue)
            html = html_spoon(request_html.get_html(issue[0]))
            # print(html)
            article_class = html.find_all("article", class_='uk-article')
            # print(article_class)
            for article in article_class:
                if volume[0] in article.get("data-permalink", ''):
                    article_htmls.append([article.get("data-permalink", ''), volume[1], issue[1]])

    return article_htmls, journal_dict


def get_articles_data(article_htmls, journal_dict):
    j_name = list(journal_dict.keys())[0]
    # print(journal_dict)
    # print(json_formatting.create_json(journal_dict))

    issue_dict = {}
    volume_dict = {}

    # chcecking if volume or issue changed (y-year, i-issue)
    y = 0
    i = "-"

    for html in article_htmls:

        html_soup = html_spoon(request_html.get_html(html[0]))
        # print(html_soup)

        volume = html[1]
        issue = html[2]

        year = html_soup.find("li", class_="field-entry year yearField").find("span", class_="field-value").get_text().strip()
        # print(year)

        titles = [html_soup.find('h1').get_text().strip()]
        # print(titles)

        pages = html_soup.find("li", class_="field-entry pages pagesField").find("span", class_="field-value").get_text().strip()
        # print(pages)
        if '-' in pages:
            pages = pages.split('-')
        elif '–' in pages:
            pages = pages.split('–')
        else:
            pages = [pages, pages]

        doi = html_soup.find("li", class_="field-entry doi-number doiField").find("span", class_="field-value").get_text().strip()
        # print(doi)

        abstract_list = []
        reference_list = []
        if html_soup.find("div", class_="uk-margin-medium-top"):

            abstract_list = html_soup.find("div", class_="uk-margin-medium-top").find_all("p")
            for idx, p in enumerate(abstract_list):
                if p.get_text().strip() == "REFERENCES:":
                    abstract_list = abstract_list[:idx]

            reference_list = html_soup.find("div", class_="uk-margin-medium-top").find_all("li")

        abstracts = []
        if len(abstract_list) > 0:
            abstracts = [abstract.get_text().strip() for abstract in abstract_list]
        if len(abstracts) == 4:
            titles.append(abstracts[0])
            titles.append(abstracts[2])
            abstracts.pop(2)
            abstracts.pop(0)
        elif len(abstracts) == 3:
            if len(abstracts[0]) < abstracts[1]:
                titles.append(abstracts[0])
                abstracts.pop(0)
            else:
                titles.append(abstracts[1])
                abstracts.pop(1)
        elif len(abstracts) == 2:
            if len(abstracts[0]) <= len(titles[0])+20 and len(abstracts[1]) <= len(titles[0])+20:
                titles.append(abstracts[1])
                titles.append(abstracts[0])
                abstracts.pop(1)
                abstracts.pop(0)
            else:
                titles.append(abstracts[0])
                abstracts.pop(0)
        references = []
        if len(reference_list) > 0:
            references = [reference.get_text().strip() for reference in reference_list]

        keywords = [keyword.get_text().strip() for keyword in html_soup.find_all("a", class_="label label-info")]
        # print(keywords)

        authors = []
        authors_dict = {}
        for idx in range(9, 0, -1):
            if html_soup.find("li", class_=f"field-entry author-{idx} authorField"):
                author = html_soup.find("li", class_=f"field-entry author-{idx} authorField").find("span", class_="field-value").get_text().strip()
            else:
                author = '-'
            if html_soup.find("li", class_=f"field-entry author-{idx} authorField"):
                email = html_soup.find("li", class_=f"field-entry author-{idx} authorField").find("span", class_="field-value").get_text().strip()
            else:
                # todo: actual email pls
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
            for auth in authors:
                authors_dict.update({auth[0]: {
                    "e-mail": auth[1],
                    "institution": auth[2],
                    "orcid": auth[3]
                }})
        # print(authors)
        # print(authors_dict)

        if y != year or i != issue:
            if y == 0:
                # first iteration so assign values - no problems
                y = year
                i = issue
            # elif

        article_dict = {"titles": titles,
                        "abstracts": abstracts,
                        "keywords": keywords,
                        "references": references,
                        "doi": doi,
                        "pages": pages,
                        "authors": authors_dict}

        issue_dict.update({titles[0]: article_dict})

        volume_dict.update({"year": year})

        journal_dict[j_name].update({volume: volume_dict})
        print(json_formatting.create_json(journal_dict))

    return journal_dict


