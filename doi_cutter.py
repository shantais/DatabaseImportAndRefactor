def cut(doi, doi_j, doi_i):
    if doi_j == '-':
        doi_j = doi[:27]

    if doi_i == '-' or doi_i not in doi:
        doi_i = doi[:33]
    return doi_j, doi_i