# pyright: reportUnknownMemberType=false
# pyright: reportUntypedFunctionDecorator=false
# pyright: reportMissingImports=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false

import json
import os
from pathlib import Path
from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch

from cardwise.bank_parser.bank_of_america import parse_bank_of_america_offers
from cardwise.bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError

# ✅ Base path for sample files
SAMPLES_DIR: str = os.path.join(os.path.dirname(__file__), "samples")


@pytest.fixture
def valid_boa_html() -> str:
    return os.path.join(SAMPLES_DIR, "valid/sample_boa_valid.html")


@pytest.fixture
def corrupted_no_offer() -> str:
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_boa_no_offer.html")


@pytest.fixture
def corrupted_no_company() -> str:
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_boa_no_company.html")


@pytest.fixture
def corrupted_invalid() -> str:
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_boa_invalid.html")


@pytest.fixture
def non_existent_file() -> str:
    return "tests/samples/non_existent_file.html"


@pytest.fixture
def html_with_whitespace() -> str:
    return os.path.join(SAMPLES_DIR, "valid/sample_boa_whitespace.html")


@pytest.fixture
def html_with_duplicates() -> str:
    return os.path.join(SAMPLES_DIR, "valid/sample_boa_duplicates.html")


@pytest.fixture
def html_with_special_chars() -> str:
    return os.path.join(SAMPLES_DIR, "valid/sample_boa_special_chars.html")


@pytest.fixture
def malformed_html() -> str:
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_boa_malformed.html")


def test_parse_bank_of_america_offers_valid(valid_boa_html: str) -> None:
    """✅ Test parsing a valid Bank of America offers page."""
    offers = parse_bank_of_america_offers(html_path=valid_boa_html)
    assert isinstance(offers, list)
    assert len(offers) == 2  # Expecting two offers
    assert offers[0]["company"] == "Starbucks"
    assert offers[0]["offer"] == "10% Cash Back"
    assert offers[1]["company"] == "McDonald's"
    assert offers[1]["offer"] == "5% Cash Back"


def test_parse_bank_of_america_offers_extra_whitespace(html_with_whitespace: str) -> None:
    """✅ Test handling of extra whitespace in company names and offers."""
    offers = parse_bank_of_america_offers(html_path=html_with_whitespace)
    assert offers[0]["company"] == "Starbucks"  # Ensure it trims whitespace
    assert offers[0]["offer"] == "10% Cash Back"


def test_parse_bank_of_america_offers_duplicates(html_with_duplicates: str) -> None:
    """✅ Test handling of duplicate offers."""
    offers = parse_bank_of_america_offers(html_path=html_with_duplicates)
    assert len(offers) == 2  # If duplicates should be kept, test as is


def test_parse_bank_of_america_offers_special_chars(html_with_special_chars: str) -> None:
    """✅ Test handling of special characters in offer text."""
    offers = parse_bank_of_america_offers(html_path=html_with_special_chars)
    assert offers[0]["offer"] == "15% & $5 Bonus Cashback"


def test_parse_bank_of_america_offers_missing_file(non_existent_file: str) -> None:
    """❌ Test handling of missing HTML file."""
    with pytest.raises(MissingHTMLFileError) as excinfo:
        parse_bank_of_america_offers(html_path=non_existent_file)
    assert "does not exist" in str(excinfo.value)


def test_parse_bank_of_america_offers_missing_offer(corrupted_no_offer: str) -> None:
    """❌ Test handling of missing offer amount."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_bank_of_america_offers(html_path=corrupted_no_offer)
    assert "Offer text not found" in str(excinfo.value)


def test_parse_bank_of_america_offers_missing_company(corrupted_no_company: str) -> None:
    """❌ Test handling of missing company name."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_bank_of_america_offers(html_path=corrupted_no_company)
    assert "Company name not found" in str(excinfo.value)


def test_parse_bank_of_america_offers_invalid_structure(corrupted_invalid: str) -> None:
    """❌ Test handling of an invalid HTML structure."""
    with pytest.raises(ValueError) as excinfo:
        parse_bank_of_america_offers(html_path=corrupted_invalid)
    assert "No valid offers found" in str(excinfo.value)


def test_parse_bank_of_america_offers_malformed_html(malformed_html: str) -> None:
    """✅ Test handling of malformed HTML (missing closing tags)."""
    offers = parse_bank_of_america_offers(html_path=malformed_html)
    assert len(offers) > 0  # Should either parse correctly or raise `ValueError`


def test_parse_bank_of_america_offers_empty_file() -> None:
    """❌ Test handling of an empty HTML file."""
    empty_file = "tests/samples/corrupted/corrupted_boa_empty.html"
    with pytest.raises(ValueError) as excinfo:
        parse_bank_of_america_offers(html_path=empty_file)
    assert "No valid offers found" in str(excinfo.value)


def test_parse_bank_of_america_offers_default_path(valid_boa_html: str, monkeypatch: MonkeyPatch) -> None:
    """✅ Test parsing using the default HTML path (mocked)."""

    def mock_read_html(_: str) -> str:
        """Mock function to return the contents of a valid HTML file."""
        with open(valid_boa_html, "r", encoding="utf-8") as f:
            return f.read()

    # ✅ Mock os.path.exists to always return True (so it doesn’t raise MissingHTMLFileError)
    def mock_exists(_: str) -> bool:
        return True

    monkeypatch.setattr("os.path.exists", mock_exists)

    # ✅ Monkeypatch the read_html function to return test HTML content
    monkeypatch.setattr("bank_parser.bank_of_america.read_html", mock_read_html)

    # ✅ Run the parser without passing `html_path`, so it defaults
    offers = parse_bank_of_america_offers()

    # ✅ Ensure valid offers are found
    assert isinstance(offers, list)
    assert len(offers) > 0  # Should not be empty
    assert any(offer["company"] == "Starbucks" for offer in offers)


def test_parse_bank_of_america_offers_save_to_file(valid_boa_html: str, tmp_path: Path) -> None:
    """✅ Test saving parsed offers to a JSON file."""
    save_path = tmp_path / "boa_offers.json"

    parse_bank_of_america_offers(html_path=valid_boa_html, save_to=str(save_path))

    assert save_path.exists()  # Ensure file was created

    with open(save_path, "r") as f:
        data: Any = json.load(f)
    assert isinstance(data, list)  # Ensure it's valid JSON
