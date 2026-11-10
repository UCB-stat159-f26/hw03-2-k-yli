from pathlib import Path

import pytest

from tennis_career.data import _clean_matches


TEST_DATA = Path(__file__).parent / "data"


def test_wta_opponent_birth_date():
    text = (TEST_DATA / "FemalePlayerCareer.js").read_text(encoding="utf-8")
    matches = _clean_matches(text, "1981-09-26", "WTA")
    first = matches.iloc[0]

    assert len(matches) == 3
    assert first["opponent"] == "Anne Miller"
    assert first["result"] == "L"
    assert first["player_age"] == pytest.approx(14.09, abs=0.01)
    assert first["age_difference"] == pytest.approx(-4.68, abs=0.01)


def test_atp_opponent_age():
    text = (TEST_DATA / "MalePlayerCareer.js").read_text(encoding="utf-8")
    matches = _clean_matches(text, "1986-06-03", "ATP")

    assert len(matches) == 3
    assert matches.iloc[0]["opponent_age"] == pytest.approx(22.264202601)
    assert matches["result"].tolist() == ["L", "L", "W"]


def test_missing_match_array():
    with pytest.raises(ValueError, match="morematchmx"):
        _clean_matches("no match data", "1981-09-26", "WTA")