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
    }

}

def group_cut(doi, build):
    for journal_key, config in patterns.items():
        match = re.match(config["regex"], doi)
        if match:
            cut_doi = config[build](match)
            return cut_doi
    # fallback:
    return "-"
