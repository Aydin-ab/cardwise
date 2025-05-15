# pyright: reportUnknownMemberType=false
# pyright: reportUntypedFunctionDecorator=false
# pyright: reportMissingImports=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownVariableType=false

from typing import Dict, List, Tuple, cast

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from cardwise.utils.fuzzy_matcher import find_best_matches, get_offers_for_company, load_fresh_offers


@pytest.fixture
def sample_offers() -> List[Dict[str, str]]:
    """Provide sample offers for testing fuzzy matching."""
    return [
        {
            "company": "Starbucks",
            "offer": "10% Cash Back",
            "bank": "Bank of America",
            "reward_type": "cash back",
        },
        {
            "company": "McDonald's",
            "offer": "3X Points",
            "bank": "Capital One",
            "reward_type": "points",
        },
        {
            "company": "Amazon",
            "offer": "5% Cash Back",
            "bank": "Chase",
            "reward_type": "cash back",
        },
    ]


def test_find_best_matches(sample_offers: List[Dict[str, str]]) -> None:
    """Test fuzzy matching with different user inputs."""
    company_names: List[str] = [offer["company"].lower() for offer in sample_offers]

    assert find_best_matches("starbucks", company_names) == ["starbucks"]
    assert find_best_matches("mcdonald", company_names) == ["mcdonald's"]
    assert find_best_matches("amzn", company_names) == ["amazon"]  # Should still find Amazon


def test_get_offers_for_company(sample_offers: List[Dict[str, str]], monkeypatch: pytest.MonkeyPatch) -> None:
    """Test getting offers dynamically."""

    def mock_load_offers(_: object) -> Tuple[List[Dict[str, str]], List[str]]:
        return sample_offers, []  # ✅ Returning (offers, warnings) to match the function signature

    monkeypatch.setattr("cardwise.utils.fuzzy_matcher.load_fresh_offers", mock_load_offers)

    offers, warnings = get_offers_for_company("starbucks")  # ✅ Unpacking both values

    assert len(offers) == 1
    assert offers[0]["company"] == "Starbucks"
    assert warnings == []  # ✅ Ensure no warnings are returned


def test_get_offers_with_partial_bank_failures(
    sample_offers: List[Dict[str, str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ensure results are still returned even when some banks fail."""

    def mock_load_offers(_: object) -> Tuple[List[Dict[str, str]], List[str]]:
        return (
            [sample_offers[0]],  # ✅ Simulate successful parsing for Bank of America
            [
                "❌ Error: The HTML file 'missing.html' for Chase does not exist. Please provide a valid file."
            ],  # ✅ Simulate Chase failure
        )

    monkeypatch.setattr("cardwise.utils.fuzzy_matcher.load_fresh_offers", mock_load_offers)

    offers, warnings = get_offers_for_company("starbucks")

    assert len(offers) == 1  # ✅ Should still return Starbucks offer
    assert offers[0]["company"] == "Starbucks"

    # ✅ Ensure the missing Chase file warning appears
    assert any("The HTML file 'missing.html' for Chase does not exist" in warning for warning in warnings)


def test_find_best_matches_low_similarity(sample_offers: List[Dict[str, str]]) -> None:
    """Test fuzzy matching when the match score is low."""
    company_names: List[str] = [offer["company"].lower() for offer in sample_offers]
    assert find_best_matches("xyzcompany", company_names) == []  # No match should be found


def test_fuzzy_matching_performance(
    benchmark: BenchmarkFixture,
    sample_offers: List[Dict[str, str]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Benchmark fuzzy matching with a large dataset."""
    large_sample: List[Dict[str, str]] = sample_offers * 1000  # Simulate a large dataset

    def mock_load_offers(_: object) -> Tuple[List[Dict[str, str]], List[str]]:
        return large_sample, []  # ✅ Returning both offers & warnings

    monkeypatch.setattr("cardwise.utils.fuzzy_matcher.load_fresh_offers", mock_load_offers)

    result: List[Dict[str, str]] = cast(List[Dict[str, str]], benchmark(lambda: get_offers_for_company("starbucks")[0]))

    assert len(result) > 0  # Ensure we still get a valid result


def test_load_fresh_offers_handles_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """✅ Ensure `html_paths` defaults to an empty dictionary but does not use production data."""

    # ✅ Mock all parsers to prevent real file loading
    monkeypatch.setattr("cardwise.utils.fuzzy_matcher.PARSERS", {})

    offers, warnings = load_fresh_offers(None)  # ✅ Explicitly passing None

    assert offers == []  # ✅ No offers should be returned (ensures no production data is used)
    assert warnings == []  # ✅ No warnings should be returned


def test_get_offers_returns_warnings_when_no_offers(monkeypatch: pytest.MonkeyPatch) -> None:
    """✅ Ensure `get_offers_for_company` correctly returns warnings if no offers exist."""

    def mock_load_offers(_: object) -> Tuple[List[Dict[str, str]], List[str]]:
        return [], ["❌ Warning: No offers found."]

    monkeypatch.setattr("cardwise.utils.fuzzy_matcher.load_fresh_offers", mock_load_offers)

    offers, warnings = get_offers_for_company("starbucks")

    assert offers == []  # ✅ No offers available
    assert warnings == ["❌ Warning: No offers found."]  # ✅ Ensure warnings are returned


def test_get_offers_no_match_but_warnings(sample_offers: List[Dict[str, str]], monkeypatch: pytest.MonkeyPatch) -> None:
    """✅ Ensure `get_offers_for_company` correctly returns warnings when no match is found."""

    def mock_load_offers(_: object) -> Tuple[List[Dict[str, str]], List[str]]:
        return sample_offers, ["❌ Warning: Some banks were unavailable."]

    monkeypatch.setattr("cardwise.utils.fuzzy_matcher.load_fresh_offers", mock_load_offers)

    offers, warnings = get_offers_for_company("unknown_brand")  # No match should be found

    assert offers == []  # ✅ No offers available
    assert warnings == ["❌ Warning: Some banks were unavailable."]  # ✅ Ensure warnings are returned
