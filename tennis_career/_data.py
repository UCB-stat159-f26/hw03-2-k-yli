import json
import re

import pandas as pd


MATCH_FIELDS = {
    "match_date": 0,
    "tournament": 1,
    "round": 8,
    "result": 4,
    "opponent": 11,
    "opponent_age_field": 16,
}


def _extract_rows(js_text):
    # Read the match array from the JavaScript text
    assignment = re.search(r"\bvar\s+morematchmx\s*=\s*", js_text)
    if assignment is None:
        raise ValueError("The career file is missing the morematchmx array.")
    rows, _ = json.JSONDecoder().raw_decode(js_text[assignment.end():])
    return rows

