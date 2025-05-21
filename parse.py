import bs4

import doi_cutter
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
    if find_info is not None:
        input_values = [input_tag.get("value", '') for input_tag in find_info.find_all('input')]
        input_values.insert(0, home_data[2])

        if str(home_data[1]).split("/")[4] == "10-15804":
            abbr = str(home_data[1]).split("/")[5]
        else:
            abbr = str(home_data[1]).split("/")[4]

        input_values.insert(1, abbr)
        # print(input_values)

        journal_dict = {
            "name": input_values[0],
            "abbr": input_values[1],
            "freq": input_values[2],
            "months": input_values[3],
            "issn": input_values[4],
            "discipline_pl": input_values[5],
            "discipline_en": input_values[6]
        }
    else:
        name = home_data[2]
        if str(home_data[1]).split("/")[4] == "10-15804":
            abbr = str(home_data[1]).split("/")[5]
        else:
            abbr = str(home_data[1]).split("/")[4]

        journal_dict = {"name": name,
                        "abbr": abbr,
                        "freq": 'Rocznik',
                        "months": "XII",
                        "issn": "2956-4875"
        }
    return journal_dict

def get_article_htmls(journal_data, issue_data, journal_dict):
    article_htmls = []
    # journal_dict[j_name] = {}

    # print(journal_data)
    # print(issue_data)
    # print('\n')

    for issue in journal_data:
        html = html_spoon(request_html.get_html(issue[0]))
        if html is None:
            continue
        # print(html)
        article_class = html.find_all("article", class_='uk-article')
        if not article_class:
            continue
        # print(article_class)

        for volume in issue_data:
            if volume[0] in issue[0]:
                journal_dict.update({volume[1]: issue[1]})
                # print(volume)
                # print(issue)


            for article in article_class:
                if volume[0] in article.get("data-permalink", '') and article.get("data-permalink", '') not in article_htmls:
                    article_htmls.append([article.get("data-permalink", ''), volume[1], issue[1]])

    return article_htmls, journal_dict


def get_articles_data(article_htmls, journal_dict):
    # print(journal_dict)
    # print(json_formatting.create_json(journal_dict))

    issue_dict = {}
    volume_dict = {}

    # checking if volume or issue changed (y-year, i-issue)
    y = 0
    i = "-"

    # doi marker
    doi = "-"
    doi_journal = "-"
    doi_issue = "-"

    for html in article_htmls:
        try:
            html_soup = html_spoon(request_html.get_html(html[0]))
            print(html_soup)

            volume = html[1]
            issue = html[2]

            year = html_soup.find("li", class_="field-entry year yearField").find("span", class_="field-value").get_text().strip()
            print(year)

            titles = [html_soup.find('h1').get_text().strip()]
            print(titles)

            if html_soup.find("li", class_="field-entry pages pagesField"):
                pages = html_soup.find("li", class_="field-entry pages pagesField").find("span", class_="field-value").get_text().strip()
            else:
                pages = '0-0'
            print(pages)

            pages = ''.join(pages.split())  # Remove all whitespace

            # Try to split on the first non-digit character
            for idx, ch in enumerate(pages):
                if not ch.isdigit():
                    pages = [pages[:idx], pages[idx + 1:]]
                    break
            else:
                # No separator found — assume single page
                pages = [pages, pages]

            print(pages)

            if html_soup.find("li", class_="field-entry doi-number doiField"):
                doi = html_soup.find("li", class_="field-entry doi-number doiField").find("span", class_="field-value").get_text().strip()
                if "http://dx.doi.org" in doi:
                    doi = "https://doi.org" + doi[17:]
            else:
                doi = '-'
            print(f"Raw DOI extracted: '{doi}'")

            if doi != '-':
                if doi_journal == '-':
                    doi_journal = doi_cutter.group_cut(doi, "build_journal")
                if doi_issue == "-" or doi_issue == "-":
                    doi_issue = doi_cutter.group_cut(doi, "build_issue")

            print(f"doi_journal {doi_journal}\ndoi_issue: {doi_issue}")

            abstract_list = []
            reference_list = []
            abstracts = []
            references = []
            try:
                print("in the abstract")
                abstract_div = html_soup.find("div", class_="uk-margin-medium-top")

                if abstract_div:
                    abstract_list = abstract_div.find_all("p")

                    for idx, p in enumerate(abstract_list):
                        text = p.get_text().strip().upper()
                        if text in ["REFERENCES:", "REFERENCES","BIBLIOGRAPHY:", "BIBLIOGRAPHY","BIBLIOGRAFIA:", "BIBLIOGRAFIA"]:
                            abstract_list = abstract_list[:idx]
                            break

                    reference_list = abstract_div.find_all("li")

                print("Abstract List")
                print(abstract_list)

                for abstract in abstract_list:
                    if abstract.find("strong") or abstract.find("b"):
                        titles.append(abstract.get_text().strip())
                    text = abstract.get_text().strip()
                    if text:
                        abstracts.append(text)

                if reference_list:
                    references = [ref.get_text().strip() for ref in reference_list]

            except Exception as e:
                print(f"Error while parsing abstracts or references: {e}")

            print("Abstracts")
            print(abstracts)
            print("Titles")
            print(titles)

            keywords = []

            try:
                keywords = [keyword.get_text().strip() for keyword in
                            html_soup.find_all("a", class_="label label-info")]
            except Exception as e:
                print(f"Error while parsing keywords: {e}")
            print(keywords)

            authors = []
            authors_dict = {}

            try:
                for idx in range(9, 0, -1):
                    try:
                        author = html_soup.find("li", class_=f"field-entry author-{idx} authorField").find("span",
                                                                                                           class_="field-value").get_text().strip()
                    except AttributeError:
                        author = '-'

                    try:
                        email = html_soup.find("li", class_=f"field-entry email-{idx} authorMail").find("span",
                                                                                                        class_="field-value").get_text().strip()
                    except AttributeError:
                        email = '-'

                    try:
                        institution = html_soup.find("li",
                                                     class_=f"field-entry institution-{idx} institutionField").find(
                            "span", class_="field-value").get_text().strip()
                    except AttributeError:
                        institution = '-'

                    try:
                        orcid = html_soup.find("li", class_=f"field-entry orcid-{idx} orcidField").find("span",
                                                                                                        class_="field-value").get_text().strip()
                    except AttributeError:
                        orcid = '-'

                    authors.append([author, email, institution, orcid])

                # Filter out empty author entries
                authors = list(filter(lambda a: a != ['-', '-', '-', '-'], authors))

                # Build author dictionary
                for auth in authors:
                    authors_dict[auth[0]] = {
                        "e-mail": auth[1],
                        "institution": auth[2],
                        "orcid": auth[3]
                    }

            except Exception as e:
                print(f"Error while parsing authors: {e}")

            print(authors)
            print(authors_dict)

            if y != year or i != issue:
                if y == 0:
                    # first iteration so assign values - no problems
                    y = year
                    i = issue
                elif y != year:
                    # year changed so automatically we have a new issue
                    issue_dict = {}
                    volume_dict = {}
                    y = year
                elif i != issue:
                    # need to clear issue so that we won't have dupes from previous in the next one
                    issue_dict = {}
                    i = issue

            article_dict = {"titles": titles,
                            "abstracts": abstracts,
                            "keywords": keywords,
                            "references": references,
                            "doi": doi,
                            "pages": pages,
                            "authors": authors_dict}

            issue_dict.update({"doi": doi_issue,
                               titles[0]: article_dict})

            volume_dict.update({"year": year,
                                issue: issue_dict})

            journal_dict.update({"doi": doi_journal,
                                 volume: volume_dict})

            doi_issue = "-"
        except Exception as e:
            print(f"Skipping article due to error: {e}\nHTML: {html}")
            continue

    return journal_dict

