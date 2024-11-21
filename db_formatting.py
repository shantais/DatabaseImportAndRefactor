def create_db(basic_journal_info, basic_issue_data, article_data):

    # basic_journal_info = [JOURNAL_NAME, ABBREVIATION, 'Kwartalnik', 'III, VI, IX, XII', ISSN, 'Nauki o polityce', 'Social studies']

    # create_journal_db = ""
    # create_issue_db = ""
    # create_article_db = ""

    # INSERT INTO JOURNAL(JOURNAL_NAME, ABBREVIATION, ISSN, COVER_PATH) VALUES(\'\', \'\', \'\', \'\');
    # INSERT INTO ARTICLE(TITLE, ABSTRACT, KEYWORDS, REFERENCES, ARTICLE_DOI, ISSUE_ID) VALUES(\'\', \'\', \'\');

    add_journal_db_info = (f"INSERT INTO JOURNAL(JOURNAL_NAME, ABBREVIATION, ISSN, COVER_PATH) "
                           f"VALUES(\'{basic_journal_info[0]}\', \'{basic_journal_info[1]}\', \'{basic_journal_info[4]}\', \'\');")

    whole_journal_db = add_journal_db_info

    for article in article_data:
        print(article)
        add_article_db_info = ""
    #     add_author_db_info = ""

    # file = open(f"{basic_journal_info[1]}.txt", whole_journal_db)