def cut(doi, doi_j, doi_i):
    if doi_j == '-':
        doi_j = doi[:28]

    # print("doi_i: " + doi_i + "\ndoi:   " + doi)
    if (doi_i == '-') or (doi_i not in doi and doi != '-'):
        doi_i = doi[:32]
    return doi_j, doi_i