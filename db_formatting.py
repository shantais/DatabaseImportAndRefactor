# def create_db(basic_journal_info, basic_issue_data, article_data):
#
#     # basic_journal_info = [JOURNAL_NAME, ABBREVIATION, 'Kwartalnik', 'III, VI, IX, XII', ISSN, 'Nauki o polityce', 'Social studies']
#
#     # create_journal_db = ""
#     # create_issue_db = ""
#     # create_article_db = ""
#
#     # INSERT INTO JOURNAL(JOURNAL_NAME, ABBREVIATION, ISSN, COVER_PATH) VALUES(\'{}\'), \'{}\');\n
#     # INSERT INTO ISSUE(VOLUME_NUMBER, ISSUE_NUMBER, ISSUE_DATE, ISSUE_DOI, JOURNAL_ID) VALUES(\'{}\', \'{}\');\n
#     # INSERT INTO ARTICLE(TITLE, ABSTRACT, KEYWORDS, REFERENCES, ARTICLE_DOI, ISSUE_ID) VALUES(\'{}\', \'{}\');\n
#
#     add_journal_db_info = (f"INSERT INTO JOURNAL(JOURNAL_NAME, ABBREVIATION, ISSN, COVER_PATH) "
#                            f"VALUES(\'{basic_journal_info[0]}\', \'{basic_journal_info[1]}\', \'{basic_journal_info[4]}\', \'\');\n")
#
#     whole_journal_db = add_journal_db_info
#
#     for issue in basic_issue_data:
#         print(issue)
#         add_issue_db_info = (f"ISSUE(VOLUME_NUMBER, ISSUE_NUMBER, ISSUE_DATE, ISSUE_DOI, JOURNAL_NAME, JOURNAL_ID) "
#                              f"VALUES(\'{issue}\')\n")
#         whole_journal_db += add_issue_db_info
#
#
#     for article in article_data:
#         print(article)
#         add_article_db_info = (f"INSERT INTO ARTICLE(TITLE, ABSTRACT, KEYWORDS, REFERENCES, AUTHORS, YEAR, PAGES, ARTICLE_DOI, ISSUE_ID) "
#                                f"VALUES(\'{article[1]}\', \'{article[2]}\', \'\', \'{article[3]}\', \'{article[4]}\', \'{article[5]}\', \'{article[6]}\', \'{article[7]}\', \'\');\n")
#         whole_journal_db += add_article_db_info
#     #     add_author_db_info = ""
#
#     print(whole_journal_db)
#
#     # file = open(f"{basic_journal_info[1]}.txt", whole_journal_db)