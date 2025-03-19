import json
import os
import subprocess
from pathlib import Path
from typing import Dict
from unittest import mock

# ✅ Define paths to test-specific HTML files
TEST_HTML_FILES: Dict[str, str] = {
    "bofa": "tests/samples/valid/sample_boa_valid.html",
    "chase": "tests/samples/valid/sample_chase_valid.html",
    "capital_one": "tests/samples/valid/sample_capital_one_valid.html",
}


def test_search_offers_help() -> None:
    """Test CLI help command."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        ["search_offers", "--help"], capture_output=True, text=True
    )
    assert "Find the best offers for one or more companies." in result.stdout


def test_search_offers_no_args() -> None:
    """Test CLI error when no arguments are provided."""
    result: subprocess.CompletedProcess[str] = subprocess.run(["search_offers"], capture_output=True, text=True)
    assert "❌ Error: You must provide at least one company name" in result.stdout


def test_search_offers_valid() -> None:
    """Test CLI with a valid query using test HTML files."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "starbucks",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
        ],
        capture_output=True,
        text=True,
    )
    assert "Here are the best offers found" in result.stdout
    assert "Starbucks" in result.stdout
    assert "Bank of America: 10% Cash Back (cash back)" in result.stdout
    assert "starbucks" in result.stdout
    assert "Capital One: 5X miles (points)" in result.stdout


def test_search_offers_no_results() -> None:
    """Test CLI when no offers are found for a company."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "unknown company",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
        ],
        capture_output=True,
        text=True,
    )
    assert "No offers found for any of the provided companies." in result.stdout


def test_search_offers_partial_results() -> None:
    """Test CLI when one bank file is missing, ensuring it still processes the others."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "starbucks",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            "missing.html",
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
        ],
        capture_output=True,
        text=True,
    )
    assert "Here are the best offers found" in result.stdout
    assert "Starbucks" in result.stdout
    assert "Bank of America: 10% Cash Back (cash back)" in result.stdout
    assert "starbucks" in result.stdout
    assert "Capital One: 5X miles (points)" in result.stdout
    assert "Error: The HTML file 'missing.html' for Chase does not exist." in result.stdout


def test_search_offers_multiple_queries() -> None:
    """Test CLI handling multiple company queries."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "starbucks",
            "nike",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
        ],
        capture_output=True,
        text=True,
    )
    assert "Here are the best offers found" in result.stdout
    assert "Starbucks" in result.stdout
    assert "Bank of America: 10% Cash Back (cash back)" in result.stdout
    assert "starbucks" in result.stdout
    assert "Capital One: 5X miles (points)" in result.stdout
    assert "Nike" in result.stdout
    assert "Chase: 15% cash back (cash back)" in result.stdout


def test_search_offers_special_chars() -> None:
    """Test CLI handling special characters in company names."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "mc'donald's",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
        ],
        capture_output=True,
        text=True,
    )
    assert "Here are the best offers found" in result.stdout
    assert "McDonald's" in result.stdout
    assert "Bank of America: 5% Cash Back (cash back)" in result.stdout
    assert "Chase: 5% cash back (cash back)" in result.stdout


def test_search_offers_case_insensitive() -> None:
    """Test CLI case insensitivity."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "STARBUCKS",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
        ],
        capture_output=True,
        text=True,
    )
    assert "Here are the best offers found" in result.stdout
    assert "Starbucks" in result.stdout
    assert "Bank of America: 10% Cash Back (cash back)" in result.stdout
    assert "starbucks" in result.stdout
    assert "Capital One: 5X miles (points)" in result.stdout


def test_search_offers_warning_for_multiple_missing_files() -> None:
    """Test CLI handling multiple missing bank files gracefully."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "starbucks",
            "--bofa-html",
            "invalid.html",
            "--chase-html",
            "missing.html",
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
        ],
        capture_output=True,
        text=True,
    )
    assert "Here are the best offers found" in result.stdout
    assert "starbucks" in result.stdout
    assert "Capital One: 5X miles (points)" in result.stdout
    assert "Error: The HTML file 'invalid.html' for Bank of America does not exist." in result.stdout
    assert "Error: The HTML file 'missing.html' for Chase does not exist." in result.stdout


def test_search_offers_save_to(tmp_path: Path) -> None:
    """✅ Test CLI saving results to a JSON file."""
    output_file: Path = tmp_path / "saved_offers.json"

    subprocess.run(
        [
            "search_offers",
            "starbucks",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
            "--save",
            str(output_file),
        ],
        capture_output=True,
        text=True,
    )

    # ✅ Ensure the file was created
    assert output_file.exists()

    # ✅ Ensure the file contains valid JSON data
    with open(output_file, "r", encoding="utf-8") as f:
        saved_offers = json.load(f)

    # ✅ Expected output
    expected_offers = [
        {
            "company": "Starbucks",
            "offer": "10% Cash Back",
            "bank": "Bank of America",
            "reward_type": "cash back",
        },
        {
            "company": "starbucks",
            "offer": "5X miles",
            "bank": "Capital One",
            "reward_type": "points",
        },
    ]

    assert saved_offers == expected_offers  # ✅ Check saved content


def test_search_offers_with_stmp(tmp_path: Path) -> None:
    """Test CLI with SMTP logging enabled."""

    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "search_offers",
            "starbucks",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
            "--capone-html",
            TEST_HTML_FILES["capital_one"],
            "--enable-email-logs",
        ],
        capture_output=True,
        text=True,
    )

    assert "📧 Email SMTP logging enabled for critical" in result.stdout

    with (
        mock.patch("bank_parser.logger.load_dotenv"),
        mock.patch.dict(
            os.environ,
            {
                "SMTP_HOST": "smtp.example.com",
                "SMTP_PORT": "587",
                "SMTP_USER": "",  # missing information
                "SMTP_PASSWORD": "",  # missing information
                "SMTP_TO": "to@example.com",
                "SMTP_FROM": "from@example.com",
            },
        ),
    ):
        result: subprocess.CompletedProcess[str] = subprocess.run(
            [
                "search_offers",
                "starbucks",
                "--bofa-html",
                TEST_HTML_FILES["bofa"],
                "--chase-html",
                TEST_HTML_FILES["chase"],
                "--capone-html",
                TEST_HTML_FILES["capital_one"],
                "--enable-email-logs",
            ],
            capture_output=True,
            text=True,
        )
    assert "SMTP environment variables are missing or incomplete" in result.stderr
    assert "Failed to enable email logging:" in result.stdout
    assert "Check your email configuration and try again." in result.stdout
