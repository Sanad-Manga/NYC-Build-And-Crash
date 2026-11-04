"""Search mode: turn a short phrase such as "Brooklyn 2022 new buildings" into filter values."""
import re

# Longest phrases come first so "new buildings" is not read as "buildings".
METRIC_PHRASES = [
    ("new construction", "new_building_count"),
    ("new buildings", "new_building_count"),
    ("new building", "new_building_count"),
    ("buildings", "housing_job_count"),
    ("building", "housing_job_count"),
    ("filings", "housing_job_count"),
    ("filing", "housing_job_count"),
    ("jobs", "housing_job_count"),
    ("job", "housing_job_count"),
    ("housing", "housing_job_count"),
    ("collisions", "collision_count"),
    ("collision", "collision_count"),
    ("crashes", "collision_count"),
    ("crash", "collision_count"),
    ("injuries", "persons_injured"),
    ("injury", "persons_injured"),
    ("injured", "persons_injured"),
]

BOROUGH_ALIASES = {
    "manhattan": "Manhattan",
    "brooklyn": "Brooklyn", "bk": "Brooklyn", "bklyn": "Brooklyn",
    "queens": "Queens",
    "bronx": "Bronx",
    "si": "Staten Island",
}
NO_FILTER_WORDS = {"nyc", "citywide", "all"}      # recognised, but they mean "no borough filter"
FILLER_WORDS = {"the", "in", "for", "of", "and", "show", "me", "year", "with"}   # ignored silently
YEAR_MIN, YEAR_MAX = 2022, 2026


def _phrase_regex(phrase: str) -> re.Pattern:
    """Whole-word, case-insensitive pattern for a (possibly multi-word) phrase."""
    return re.compile(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])")


def parse_query(text) -> dict:
    """Parse free text into {borough, year, metric, zip_code, unparsed}.

    Missing parts are None. Words that were not understood (typos, a second borough, a year
    outside 2022-2026 ...) are returned in `unparsed` so the app can show "Ignored: ...".
    """
    result = {"borough": None, "year": None, "metric": None, "zip_code": None, "unparsed": []}
    if not isinstance(text, str):
        return result
    rest = re.sub(r"[^a-z0-9 ]+", " ", text.lower())           # lower-case, drop punctuation

    # 1) multi-word phrases first: metric phrases, then "staten island"
    for phrase, metric in METRIC_PHRASES:
        pattern = _phrase_regex(phrase)
        if pattern.search(rest):
            if result["metric"] is None:
                result["metric"] = metric
            else:                                              # a second metric word
                result["unparsed"].append(phrase)
            rest = pattern.sub(" ", rest)
    staten = _phrase_regex("staten island")
    if staten.search(rest):
        result["borough"] = "Staten Island"
        rest = staten.sub(" ", rest)

    # 2) remaining single tokens: borough alias, year, ZIP, filler, or unknown
    for token in rest.split():
        if token in BOROUGH_ALIASES:
            borough = BOROUGH_ALIASES[token]
            if result["borough"] is None:
                result["borough"] = borough
            elif result["borough"] != borough:
                result["unparsed"].append(token)               # only one borough is supported
        elif token in NO_FILTER_WORDS or token in FILLER_WORDS:
            continue
        elif re.fullmatch(r"\d{5}", token):
            if result["zip_code"] is None:
                result["zip_code"] = token
            else:
                result["unparsed"].append(token)
        elif re.fullmatch(r"\d{4}", token) and YEAR_MIN <= int(token) <= YEAR_MAX:
            if result["year"] is None:
                result["year"] = int(token)
            else:
                result["unparsed"].append(token)
        else:
            result["unparsed"].append(token)
    return result


def describe_query(parsed: dict) -> tuple:
    """Plain-language (understood, ignored) strings for the app to show under the search box."""
    parts = []
    if parsed["borough"]:
        parts.append(f"borough = {parsed['borough']}")
    if parsed["year"]:
        parts.append(f"year = {parsed['year']}")
    if parsed["zip_code"]:
        parts.append(f"ZIP = {parsed['zip_code']}")
    if parsed["metric"]:
        parts.append(f"metric = {parsed['metric']}")
    understood = ", ".join(parts) if parts else "nothing recognised"
    ignored = ", ".join(parsed["unparsed"])
    return understood, ignored
