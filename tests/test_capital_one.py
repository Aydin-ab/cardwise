import json
import os

import pytest

from bank_parser.capital_one import parse_capital_one_offers
from bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError

# ✅ Base path for sample files
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")


@pytest.fixture
def valid_capital_one_html():
    return os.path.join(SAMPLES_DIR, "valid/sample_capital_one_valid.html")


@pytest.fixture
def corrupted_no_offer():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_capital_one_no_offer.html")


@pytest.fixture
def corrupted_no_company():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_capital_one_no_company.html")


@pytest.fixture
def corrupted_invalid():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_capital_one_invalid.html")


@pytest.fixture
def non_existent_file():
    return "tests/samples/non_existent_capital_one.html"


@pytest.fixture
def html_with_whitespace():
    return os.path.join(SAMPLES_DIR, "valid/sample_capital_one_whitespace.html")


@pytest.fixture
def html_with_duplicates():
    return os.path.join(SAMPLES_DIR, "valid/sample_capital_one_duplicates.html")


@pytest.fixture
def html_with_special_chars():
    return os.path.join(SAMPLES_DIR, "valid/sample_capital_one_special_chars.html")


@pytest.fixture
def malformed_html():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_capital_one_malformed.html")


@pytest.fixture
def html_with_missing_image():
    return os.path.join(SAMPLES_DIR, "corrupted/corrupted_capital_one_no_image.html")


def test_parse_capital_one_offers_valid(valid_capital_one_html):
    """✅ Test parsing a valid Capital One offers page."""
    offers = parse_capital_one_offers(html_path=valid_capital_one_html)
    assert isinstance(offers, list)
    assert len(offers) == 2  # Expecting two offers
    assert offers[0]["company"] == "starbucks"
    assert offers[0]["offer"] == "5X miles"
    assert offers[1]["company"] == "adidas"
    assert offers[1]["offer"] == "10X miles"


def test_parse_capital_one_offers_extra_whitespace(html_with_whitespace):
    """✅ Test handling of extra whitespace in company names and offers."""
    offers = parse_capital_one_offers(html_path=html_with_whitespace)
    assert offers[0]["company"] == "walmart"
    assert offers[0]["offer"] == "3X miles"


def test_parse_capital_one_offers_duplicates(html_with_duplicates):
    """✅ Test handling of duplicate offers."""
    offers = parse_capital_one_offers(html_path=html_with_duplicates)
    assert len(offers) == 2  # Expecting 2, since the sample contains two identical offers


def test_parse_capital_one_offers_special_chars(html_with_special_chars):
    """✅ Test handling of special characters in offer text."""
    offers = parse_capital_one_offers(html_path=html_with_special_chars)
    assert offers[0]["offer"] == "5X miles & $10 Bonus Points"


def test_parse_capital_one_offers_missing_file(non_existent_file):
    """❌ Test handling of missing HTML file."""
    with pytest.raises(MissingHTMLFileError) as excinfo:
        parse_capital_one_offers(html_path=non_existent_file)
    assert "does not exist" in str(excinfo.value)


def test_parse_capital_one_offers_missing_offer(corrupted_no_offer):
    """❌ Test handling of missing offer amount."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_capital_one_offers(html_path=corrupted_no_offer)
    assert "Offer text is empty" in str(excinfo.value)


def test_parse_capital_one_offers_missing_company(corrupted_no_company):
    """❌ Test handling of missing company name."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_capital_one_offers(html_path=corrupted_no_company)
    assert "Company name not found" in str(excinfo.value)


def test_parse_capital_one_offers_invalid_structure(corrupted_invalid):
    """❌ Test handling of an invalid HTML structure."""
    with pytest.raises(ValueError) as excinfo:
        parse_capital_one_offers(html_path=corrupted_invalid)
    assert "No valid offers found" in str(excinfo.value)


def test_parse_capital_one_offers_malformed_html(malformed_html):
    """✅ Test handling of malformed HTML (missing closing tags)."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_capital_one_offers(html_path=malformed_html)
    assert "Offer text not found" in str(excinfo.value)


def test_parse_capital_one_offers_missing_image(html_with_missing_image):
    """❌ Test handling of missing image tag inside offer tile."""
    with pytest.raises(InvalidOfferDataError) as excinfo:
        parse_capital_one_offers(html_path=html_with_missing_image)
    assert "Image tag not found or missing 'src' attribute" in str(excinfo.value)


def test_parse_capital_one_offers_saves_to_json(valid_capital_one_html, tmp_path):
    """✅ Test saving parsed results to a JSON file."""
    output_file = tmp_path / "capital_one_offers.json"

    offers = parse_capital_one_offers(html_path=valid_capital_one_html, save_to=output_file)

    # ✅ Ensure the file was created
    assert output_file.exists()

    # ✅ Ensure the file contains valid JSON data
    with open(output_file, "r", encoding="utf-8") as f:
        saved_offers = json.load(f)

    assert saved_offers == offers  # ✅ The saved JSON should match the returned offers
