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


def get_article_htmls_and_issue_dict(journal_data, issue_data, journal_dict):
    j_abbr = list(journal_dict.keys())[0]
    issue_dict = {j_abbr: {"journal": journal_dict[j_abbr]["name"]}}

    article_htmls = []
    for volume in issue_data:
        for issue in journal_data:
            if volume[1] in issue[1]:
                issue_dict[j_abbr] = {volume[2]: issue[2]}
                print(volume)
                print(issue)

    print(issue_dict)
    return article_htmls, issue_dict

def get_article_htmls_and_basic_issue_data(journal_data, issue_data):
    # j_d (idx, html, issue num)
    # i_d (idx, html, vol num)
    # result -> i_d ([vol num, [issue num, ..., issue num]], ...)

    basic_issue_data = []
    all_htmls = []

    for volume in issue_data:
        all_issues = []
        for issue in journal_data:
            if volume[1] in issue[1]:
                all_issues.append(issue[2])
            print(issue)
            html = html_spoon(request_html.get_html(issue[1]))
            print(html)
            article_class = html.find_all("article", class_='uk-article')
            print(article_class)
            for article in article_class:
                if volume[1] in article.get("data-permalink", ''):
                    all_htmls.append([article.get("data-permalink", ''), volume[2], issue[2]])
        basic_issue_data.append([volume[2], all_issues])

    return all_htmls, basic_issue_data


def get_articles_data(article_htmls):
    article_info = []
    for html in article_htmls:
        html_soup = html_spoon(request_html.get_html(html[0]))
        # print(html_soup)

        journal = html_soup.find("li", class_="field-entry year yearField").find("span", class_="field-value").get_text().strip()
        # print(journal)

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
        else:
            pages = [pages, pages]

        doi = html_soup.find("li", class_="field-entry doi-number doiField").find("span", class_="field-value").get_text().strip()
        # print(doi)

        volume = html[1]

        issue = html[2]

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

            # input_values = [input_tag.get("value", '') for input_tag in find_info.find_all('input')]
        keywords = [keyword.get_text().strip() for keyword in html_soup.find_all("a", class_="label label-info")]
        # print(keywords)

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

        article_info.append([title, abstract_soup, keywords, reference_list, authors, year, pages, doi, journal, volume, issue])
    return article_info

