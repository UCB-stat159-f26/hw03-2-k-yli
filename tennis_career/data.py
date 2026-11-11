import json
import re
import pandas as pd
import time


from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


BASE_URL = "https://www.tennisabstract.com"


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

def _fetch_text(url, retries=3):
    # Read a Tennis Abstract page or JS file as text
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=20) as response:
                return response.read().decode("utf-8")
        except HTTPError as exc:
            if exc.code == 404:
                return ""
            if exc.code != 429 or attempt == retries - 1:
                raise RuntimeError(f"Tennis Abstract returned HTTP {exc.code}.") from exc
            time.sleep(2 ** attempt)
        except (URLError, TimeoutError) as exc:
            raise RuntimeError("Could not reach Tennis Abstract.") from exc


def _find_player(player_name):
    # Find the player's URL identifier and birthday.
    words = player_name.split()
    candidates = ["".join(word[:1].upper() + word[1:] for word in words)]
    for slug in dict.fromkeys(candidates):
        if slug:
            url = f"{BASE_URL}/cgi-bin/player.cgi?p={quote(slug, safe='')}"
            profile = _fetch_text(url)
            dob = re.search(r"\bvar\s+dob\s*=\s*['\"]?(\d{8})\b", profile)
            if dob:
                return slug, pd.to_datetime(dob.group(1), format="%Y%m%d")
    raise ValueError(f"No Tennis Abstract player found for {player_name!r}.")


def _infer_tour(rows):
    # Identify the opponent age format in the career file.
    for row in rows:
        value = str(row[MATCH_FIELDS["opponent_age_field"]]).strip()
        if re.fullmatch(r"[0-9]{8}", value):
            return "WTA"
        if re.fullmatch(r"[0-9]{1,2}(?:\.[0-9]+)?", value):
            return "ATP"
    raise ValueError("Could not identify the opponent age format.")


def get_career_matches(player_name):
    # Download and clean career match data for a Tennis Abstract player.
    slug, birthday = _find_player(player_name)
    url = f"{BASE_URL}/jsmatches/{quote(slug, safe='')}Career.js"
    js_text = _fetch_text(url)
    if not js_text:
        raise ValueError(f"No career match file found for {player_name!r}.")
    tour = _infer_tour(_extract_rows(js_text))
    return _clean_matches(js_text, birthday, tour)