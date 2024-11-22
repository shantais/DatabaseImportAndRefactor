def article_and_author(article_data):
    article_dict = {}
    author_dict = {}

    for idx, article in enumerate(article_data):
        # article_info.append([title, abstract_soup, keywords, reference_list, authors, year, pages, doi, journal, volume, issue])
        article_dict[article[0]] = {}
        article_dict[article[0]]["title"] = {article[0]}
        # article_dict[article[idx]]["abstract_soup"] = {article[1]}
        for keyword in article[2]:
            article_dict[article[0]]["keyword"] = {keyword}
        # article_dict[article[idx]]["reference_list"] = {article[3]}
        for author in article[4]:
            print(author)
            for a in author:
                print(type(a))
            # authors.append([author, email, institution, orcid])
            author_dict[author[0]] = {}
            author_dict[author[0]]["email"] = {author[1]}
            author_dict[author[0]]["institution"] = {author[2]}
            author_dict[author[0]]["orcid"] = {author[3]}
            article_dict[article[0]]["authors"] = {}
            article_dict[article[0]]["authors"][author[0]] = {}
            article_dict[article[0]]["authors"][author[0]]["email"] = {author[1]}
            article_dict[article[0]]["authors"][author[0]]["institution"] = {author[2]}
            article_dict[article[0]]["authors"][author[0]]["orcid"] = {author[3]}
        article_dict[article[0]]["year"] = {article[5]}
        print(article[6])
        article_dict[article[0]]["pages"] = {}
        article_dict[article[0]]["pages"]["from"] = {article[6][0]}
        article_dict[article[0]]["pages"]["to"] = {article[6][1]}
        article_dict[article[0]]["doi"] = {article[7]}
        article_dict[article[0]]["journal"] = {article[8]}
        article_dict[article[0]]["volume"] = {article[9]}
        article_dict[article[0]]["issue"] = {article[10]}

    return article_dict, author_dict