import re

import re

# Define known journal DOI formats
patterns = {
    "CDM": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>CDM)\.(?P<year>\d{4})\.(?P<issue>\d{1,2})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('issue')}"
    },
    "MF": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>MF)\.(?P<year>\d{4})(?P<issue>\d{1})(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}{m.group('issue')}"
    },
    "ve": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>ve)\.(?P<year>\d{4})\.(?P<issue>\d{2})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('issue')}"
    },
    "CCNiW": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>CCNiW)\.(?P<year>\d{4})\.(?P<issue>\d{2})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('issue')}"
    },
    "CPLS": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>CPLS)\.(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}{m.group('issue')}"
    },
    "sdhw": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>sdhw)\.(?P<year>\d{4})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}"
    },
    "CEJSS": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>CEJSS)\.(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}{m.group('issue')}"
    },
    "sal": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>sal)(?P<year>\d{4})(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
    },
    "so": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>so)(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
    },
    "pbs": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>pbs)\.(?P<year>\d{4})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}"
    },
    "pomi": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>pomi)(?P<year>\d{4})(?P<article>\d{2})$",
        "build_journal": lambda m: "https://doi.org/10.15804/pomi",
        "build_issue": lambda m: f"https://doi.org/10.15804/pomi{m.group('year')}"
    },
    "PPUSN": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>PPUSN)\.(?P<year>\d{4})\.(?P<issue>\d{2})\.(?P<article>\d{2})$",
        "build_journal": lambda m: "https://doi.org/10.15804/pomi",
        "build_issue": lambda m: f"https://doi.org/10.15804/pomi.{m.group('year')}.{m.group('issue')}"
    },
    "PPUSI": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>PPUSI)\.(?P<year>\d{4})\.(?P<issue>\d{2})\.(?P<article>\d{2})$",
        "build_journal": lambda m: "https://doi.org/10.15804/pomi",
        "build_issue": lambda m: f"https://doi.org/10.15804/pomi.{m.group('year')}.{m.group('issue')}"
    },
    "athena": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>athena)\.(?P<year>\d{4})\.(?P<volume>\d{1,3})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('volume')}"
    },
    "ppk": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>ppk)\.(?P<year>\d{4})\.(?P<issue>\d{2})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('issue')}"
    },
    "hso": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>hso)(?P<year>\d{2})(?P<issue>\d{2})(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
    },
    "tner": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>tner)\.(?P<year>\d{2,4})\.(?P<volume>\d{1,2})\.(?P<issue>\d)\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('volume')}.{m.group('issue')}"
    },
    "kie": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>kie)\.(?P<year>\d{4})\.(?P<issue>\d{2})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('issue')}"
    },
    "tpn": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>tpn)(?P<year>\d{4})\.(?P<issue>\d{1})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}.{m.group('issue')}"
    },
    "acno": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>acno)(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
    },
    "siip": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>siip)(?P<year>\d{4})(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
    },
    "IFforE": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>IFforE)(?P<year>\d{4})\.(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
    },
    "kimwe": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>kimwe)(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
    },
    "cip": {
        "regex": r"^https://doi\.org/10\.5604/(?P<journal>cip)(?P<year>\d{4})(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.5604/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.5604/{m.group('journal')}{m.group('year')}"
    },
    "IW": [
        {
            # With volume and article
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>IW)\.(?P<year>\d{4})\.(?P<volume>\d{2})\.(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('volume')}"
        },
        {
            # With volume, issue, and article
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>IW)\.(?P<year>\d{4})\.(?P<volume>\d{2})\.(?P<issue>\d)\.(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('volume')}.{m.group('issue')}"
        }
    ],
    "tpom": {
        "regex": r"^https://doi\.org/10\.15804/(?P<journal>tpom)(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
        "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
        "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
    },
    "ap": [
        {
            # Pattern with 1-digit issue number and dot separators (e.g., ap2023.2.01)
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>ap)(?P<year>\d{4})\.(?P<issue>\d{1,2})\.(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}.{m.group('issue')}"
        },
        {
            # Pattern without issue number (e.g., ap201201)
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>ap)(?P<year>\d{4})(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
        }
    ],
    "rop": [
            {
                # Pattern with 1-digit issue number
                "regex": r"^https://doi\.org/10\.15804/(?P<journal>rop)(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
                "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
                "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
            },
            {
                # Pattern without issue number (defaults to year only)
                "regex": r"^https://doi\.org/10\.15804/(?P<journal>rop)(?P<year>\d{4})(?P<article>\d{2})$",
                "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
                "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
            }
        ],
    "npw": [
        {
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>npw)(?P<year>\d{4})(?P<volume>\d{2})(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('volume')}"
        },
        {
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>npw)(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
        }
    ],
    "ksm": [
        {
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>ksm)(?P<year>\d{4})(?P<issue>\d{2})(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
        },
        {
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>ksm)(?P<year>\d{4})(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
        }
    ],
    "em": [
        {
            # With year, issue, and article
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>em)\.(?P<year>\d{4})\.(?P<issue>\d{2})\.(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}.{m.group('issue')}"
        },
        {
            # With year and article only
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>em)\.(?P<year>\d{4})\.(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}.{m.group('year')}"
        }
    ],
    "ppsy": [
        {
            # With year + 1-digit issue + 2-digit article (e.g., ppsy2017101)
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>ppsy)(?P<year>\d{4})(?P<issue>\d)(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}{m.group('issue')}"
        },
        {
            # With year only and 3-digit article (e.g., ppsy2006001)
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>ppsy)(?P<year>\d{4})(?P<article>\d{3})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
        },
        {
            # With year only and 2-digit article (e.g., ppsy202101)
            "regex": r"^https://doi\.org/10\.15804/(?P<journal>ppsy)(?P<year>\d{4})(?P<article>\d{2})$",
            "build_journal": lambda m: f"https://doi.org/10.15804/{m.group('journal')}",
            "build_issue": lambda m: f"https://doi.org/10.15804/{m.group('journal')}{m.group('year')}"
        }
    ]
}

def group_cut(doi, build):
    for journal_key, config in patterns.items():
        configs = config if isinstance(config, list) else [config]
        for entry in configs:
            match = re.match(entry["regex"], doi)
            if match:
                try:
                    print(f"Matched for DOI {doi} with pattern '{journal_key}'")
                    cut_doi = entry[build](match)
                    return cut_doi
                except Exception as e:
                    print(f"Error building {build} for DOI {doi} with pattern '{journal_key}': {e}")
                    return "-"
    # fallback:
    return "-"
