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


def _opponent_ages(matches, tour):
# Return opponent ages in years for either tour
    values = matches["opponent_age_field"]
    if tour == "ATP":
        return pd.to_numeric(values, errors="coerce")
    if tour == "WTA":
        birthdays = pd.to_datetime(values, format="%Y%m%d", errors="coerce")
        return (matches["match_date"] - birthdays).dt.days / 365.25
    raise ValueError(f"Unsupported tour: {tour!r}. Expected ATP or WTA.")


def _clean_matches(js_text, player_birthday, tour):
# Turn raw career match text into a DataFrame ready for plotting
    rows = _extract_rows(js_text)
    matches = pd.DataFrame({
        name: [row[index] for row in rows] for name, index in MATCH_FIELDS.items()
    })
    matches["match_date"] = pd.to_datetime(
        matches["match_date"], format="%Y%m%d", errors="coerce"
    )
    birthday = pd.Timestamp(player_birthday)
    matches["player_age"] = (matches["match_date"] - birthday).dt.days / 365.25
    matches["opponent_age"] = _opponent_ages(matches, tour)
    matches["age_difference"] = matches["player_age"] - matches["opponent_age"]
    valid = matches["result"].isin(["W", "L"])
    matches = matches.loc[valid].dropna(subset=["match_date", "opponent_age"])
    return matches.drop(columns="opponent_age_field").reset_index(drop=True)