import json
import os

import pytest

from bank_parser.chase import parse_chase_offers
from bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError

# ✅ Base path for sample files
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")


@pytest.fixture
def valid_chase_html():
    return os.path.join(SAMPLES_DIR, "valid/sample_chase_valid.html")


@pytest.fixture
def corrupted_no_offer():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_chase_no_offer.html")


@pytest.fixture
def corrupted_no_company():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_chase_no_company.html")


@pytest.fixture
def corrupted_invalid():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_chase_invalid.html")


@pytest.fixture
def non_existent_file():
    return "tests/samples/non_existent_chase.html"


@pytest.fixture
def html_with_whitespace():
    return os.path.join(SAMPLES_DIR, "valid/sample_chase_whitespace.html")


@pytest.fixture
def html_with_duplicates():
    return os.path.join(SAMPLES_DIR, "valid/sample_chase_duplicates.html")


@pytest.fixture
def html_with_special_chars():
    return os.path.join(SAMPLES_DIR, "valid/sample_chase_special_chars.html")


@pytest.fixture
def malformed_html():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_chase_malformed.html")


def test_parse_chase_offers_valid(valid_chase_html):
    """✅ Test parsing a valid Chase offers page."""
    offers = parse_chase_offers(html_path=valid_chase_html)
    assert isinstance(offers, list)
    assert len(offers) == 2  # Expecting two offers
    assert offers[0]["company"] == "McDonald's"
    assert offers[0]["offer"] == "5% cash back"
    assert offers[1]["company"] == "Nike"
    assert offers[1]["offer"] == "15% cash back"


def test_parse_chase_offers_extra_whitespace(html_with_whitespace):
    """✅ Test handling of extra whitespace in company names and offers."""
    offers = parse_chase_offers(html_path=html_with_whitespace)
    assert offers[0]["company"] == "Total Wireless"
    assert offers[0]["offer"] == "25% cash back"  # Ensures trimming works


def test_parse_chase_offers_duplicates(html_with_duplicates):
    """✅ Test handling of duplicate offers."""
    offers = parse_chase_offers(html_path=html_with_duplicates)
    assert len(offers) == 2  # Expecting 2, since the sample contains two identical offers


def test_parse_chase_offers_special_chars(html_with_special_chars):
    """✅ Test handling of special characters in offer text."""
    offers = parse_chase_offers(html_path=html_with_special_chars)
    assert offers[0]["offer"] == "15% & $5 Bonus Cashback"


def test_parse_chase_offers_missing_file(non_existent_file):
    """❌ Test handling of missing HTML file."""
    with pytest.raises(MissingHTMLFileError) as excinfo:
        parse_chase_offers(html_path=non_existent_file)
    assert "does not exist" in str(excinfo.value)


def test_parse_chase_offers_missing_offer(corrupted_no_offer):
    """❌ Test handling of missing offer amount."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_chase_offers(html_path=corrupted_no_offer)
    assert "Offer text not found" in str(excinfo.value)


def test_parse_chase_offers_missing_company(corrupted_no_company):
    """❌ Test handling of missing company name."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_chase_offers(html_path=corrupted_no_company)
    assert "Company name not found" in str(excinfo.value)


def test_parse_chase_offers_invalid_structure(corrupted_invalid):
    """❌ Test handling of an invalid HTML structure."""
    with pytest.raises(ValueError) as excinfo:
        parse_chase_offers(html_path=corrupted_invalid)
    assert "No valid offers found" in str(excinfo.value)


def test_parse_chase_offers_malformed_html(malformed_html):
    """✅ Test handling of malformed HTML (missing closing tags)."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_chase_offers(html_path=malformed_html)
    assert "Offer data is incomplete" in str(excinfo.value)


def test_parse_chase_offers_save_to(valid_chase_html, tmp_path):
    """✅ Test saving parsed Chase offers to a JSON file."""
    tmp_file = tmp_path / "test_chase_offers.json"

    # Call the function with the save_to parameter
    offers = parse_chase_offers(html_path=valid_chase_html, save_to=tmp_file)

    # Ensure the file was created
    assert tmp_file.exists()

    # Read back the saved JSON and verify contents
    with open(tmp_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data == offers
