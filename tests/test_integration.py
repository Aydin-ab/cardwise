# pyright: reportUnknownMemberType=false
# pyright: reportUntypedFunctionDecorator=false
# pyright: reportMissingImports=false
import json
import os
from pathlib import Path
from typing import Dict, List

import pytest

from cardwise.utils.fuzzy_matcher import load_fresh_offers

# ✅ Base path for sample files
SAMPLES_DIR: str = os.path.join(os.path.dirname(__file__), "samples/valid")


@pytest.fixture
def valid_bank_files() -> Dict[str, str]:
    """Fixture returning valid sample files for all banks."""
    return {
        "bank_of_america": os.path.join(SAMPLES_DIR, "sample_boa_valid.html"),
        "chase": os.path.join(SAMPLES_DIR, "sample_chase_valid.html"),
        "capital_one": os.path.join(SAMPLES_DIR, "sample_capital_one_valid.html"),
    }


@pytest.fixture
def missing_bank_file() -> Dict[str, str]:
    """Fixture simulating a missing Chase file."""
    return {
        "bank_of_america": os.path.join(SAMPLES_DIR, "sample_boa_valid.html"),
        "chase": "tests/samples/non_existent_chase.html",
        "capital_one": os.path.join(SAMPLES_DIR, "sample_capital_one_valid.html"),
    }


def test_load_fresh_offers(valid_bank_files: Dict[str, str]) -> None:
    """✅ Ensure offers are loaded from all banks correctly."""
    offers: List[Dict[str, str]]
    warnings: List[str]
    offers, warnings = load_fresh_offers(valid_bank_files)

    assert isinstance(offers, list)
    assert len(offers) == 6  # Expecting 6 offers based on provided samples
    assert any(offer["company"] == "Starbucks" and offer["bank"] == "Bank of America" for offer in offers)
    assert any(offer["company"] == "McDonald's" and offer["bank"] == "Chase" for offer in offers)
    assert any(offer["company"] == "Nike" and offer["bank"] == "Chase" for offer in offers)
    assert any(offer["company"] == "adidas" and offer["bank"] == "Capital One" for offer in offers)
    assert warnings == []  # ✅ No warnings since all banks have data


def test_load_fresh_offers_missing_file(missing_bank_file: Dict[str, str]) -> None:
    """✅ Ensure results are still returned even when a bank file is missing."""
    offers: List[Dict[str, str]]
    warnings: List[str]
    offers, warnings = load_fresh_offers(missing_bank_file)

    assert len(offers) > 0  # ✅ Should still return offers from BOA & Capital One
    assert any(offer["company"] == "Starbucks" for offer in offers)
    assert any(offer["company"] == "adidas" for offer in offers)

    # ✅ Ensure we get a warning about the missing Chase file
    assert any("The HTML file" in warning and "Chase" in warning for warning in warnings)  # ✅ Check Chase file missing


def test_load_fresh_offers_no_data() -> None:
    """✅ Ensure handling when all HTML files are empty."""
    empty_files: Dict[str, str] = {
        "bank_of_america": "tests/samples/empty_boa.html",
        "chase": "tests/samples/empty_chase.html",
        "capital_one": "tests/samples/empty_capital_one.html",
    }

    offers: List[Dict[str, str]]
    warnings: List[str]
    offers, warnings = load_fresh_offers(empty_files)

    assert offers == []  # ✅ Should return an empty list
    assert len(warnings) == 3  # ✅ Should have warnings for all missing data


def test_load_fresh_offers_saves_json(valid_bank_files: Dict[str, str], tmp_path: Path) -> None:
    """✅ Ensure offers can be saved to a JSON file."""
    output_file: Path = tmp_path / "offers.json"

    offers: List[Dict[str, str]]
    offers, _ = load_fresh_offers(valid_bank_files, output_file=str(output_file))

    # ✅ Ensure the file was created
    assert output_file.exists()

    # ✅ Read the saved file and validate content
    with open(output_file, "r", encoding="utf-8") as f:
        saved_offers: List[Dict[str, str]] = json.load(f)

    assert len(saved_offers) == len(offers)  # ✅ Should match the returned offers
