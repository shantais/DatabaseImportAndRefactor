import re

def cut(doi, doi_j, doi_i):
    if doi_j == '-':
        doi_j = doi[:27]

    # print("doi_i: " + doi_i + "\ndoi:   " + doi)
    if (doi_i == '-') or (doi_i not in doi and doi != '-'):
        doi_i = doi[:37]
    return doi_j, doi_i

def group (doi):

    suffix_patterns = [r"(\d{4})(\d{2})",
                       r".(\d{4})(\d{2})",
                       r"(\d{4}).(\d{2})",
                       r".(\d{4}).(\d{2})",
                       r"(\d{2})(\d{1})(\d{2})",
                       r".(\d{2})(\d{1})(\d{2})",
                       r"(\d{2}).(\d{1}).(\d{2})",
                       r".(\d{2}).(\d{1}).(\d{2})",
                       r"(\d{2})(\d{2})(\d{2})",
                       r".(\d{2})(\d{2})(\d{2})",
                       r".(\d{2}).(\d{2}).(\d{2})",
                       r"(\d{4})(\d{1})(\d{2})",
                       r".(\d{4})(\d{1})(\d{2})",
                       r"(\d{4})(\d{2})(\d{2})",
                       r".(\d{4})(\d{2})(\d{2})",
                       r"(\d{4}).(\d{1}).(\d{2})",
                       r".(\d{4}).(\d{1}).(\d{2})",
                       r"(\d{4}).(\d{2}).(\d{2})",
                       r".(\d{4}).(\d{2}).(\d{2})",
                       r".(\d{2}).(\d{2}).(\d{1}).(\d{2})",
                       r".(\d{4}).(\d{2}).(\d{1}).(\d{2})"]

    middle_patterns = ["pomi",
                       "PPUSN",
                       "PPUSI",
                       "ppk",
                       "ppsy",
                       "athena",
                       "em",
                       "hso",
                       "IW",
                       "npw",
                       "aoto",
                       "ap",
                       "ksm",
                       "kie",
                       "pbs",
                       "rop",
                       "so",
                       "sal",
                       "tpn",
                       "ppsy",
                       "tner",
                       "sdhw",
                       "MF",
                       "CEJSS",
                       "ve",
                       "CDM",
                       "CCNiW",
                       "CPLS",
                       "ajepss"]

    prefix =  "https://doi.org/10.15804/"

    journal = "-"
    doi_journal = "-"
    doi_journal_temp = "-"
    doi_issue = "-"

    for middle_pattern in middle_patterns:
        # Create a regex pattern that allows for the middle pattern to appear anywhere after the prefix
        pattern = prefix + r"(.*" + middle_pattern + r".*)"

        # Search for the match in the DOI
        match = re.search(pattern, doi)

        if match:
            journal = middle_pattern

            if journal == "PPUSN" or journal == "PPUSI" or journal == "pomi":
                doi_journal = prefix + "PPUSN" + "."
                if journal == "pomi":
                    doi_journal_temp = prefix + journal
                if journal == "PPUSI":
                    doi_journal_temp = prefix + journal + "."
            else:
                doi_journal = prefix + journal
            print(f"Match found for middle pattern '{middle_pattern}':")
            print(doi_journal)
            break
        else:
            print(f"No match found for {middle_pattern}")

    for suffix_pattern in suffix_patterns:
        # Choose correct journal base
        base = doi_journal_temp if journal in ["PPUSI", "pomi"] else doi_journal

        # Compile pattern to match full DOI exactly
        full_pattern = re.compile(re.escape(base) + suffix_pattern + r"$")

        # Try full match
        match = full_pattern.fullmatch(doi)

        if match:
            groups = match.groups()

            # Reconstruct doi_issue by stripping the last group (and separator if present)
            if len(groups) > 1:
                trimmed_groups = groups[:-1]  # remove last group
                # Remove preceding dot if applicable
                if '.' in suffix_pattern or '-' in suffix_pattern:
                    doi_issue = base + '.'.join(trimmed_groups)
                else:
                    doi_issue = base + ''.join(trimmed_groups)
            else:
                doi_issue = base  # nothing to trim

            print(f"Match found for suffix '{suffix_pattern}':")
            print(f"doi_issue = '{doi_issue}'")
            break
        else:
            print(f"No match found for {suffix_pattern}")


    return doi_journal, doi_issue

