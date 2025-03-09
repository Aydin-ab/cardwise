import json
import subprocess

# ✅ Define paths to test-specific HTML files
TEST_HTML_FILES = {
    "bofa": "tests/samples/valid/sample_boa_valid.html",
    "chase": "tests/samples/valid/sample_chase_valid.html",
    "capital_one": "tests/samples/valid/sample_capital_one_valid.html",
}


def test_search_offer_help():
    """Test CLI help command."""
    result = subprocess.run(["search_offer", "--help"], capture_output=True, text=True)
    assert "Find the best offers for one or more companies." in result.stdout


def test_search_offer_no_args():
    """Test CLI error when no arguments are provided."""
    result = subprocess.run(["search_offer"], capture_output=True, text=True)
    assert "❌ Error: You must provide at least one company name" in result.stdout


def test_search_offer_valid():
    """Test CLI with a valid query using test HTML files."""
    result = subprocess.run(
        [
            "search_offer",
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
    assert "✅ Matches found for 'starbucks'" in result.stdout
    assert "✅ Found 2 offers for 'starbucks':" in result.stdout  # Should find in all banks


def test_search_offer_partial_results():
    """Test CLI when one bank file is missing, ensuring it still processes the others."""
    result = subprocess.run(
        [
            "search_offer",
            "starbucks",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            "missing.html",
        ],  # Chase file does not exist
        capture_output=True,
        text=True,
    )
    assert "✅ Matches found for 'starbucks'" in result.stdout
    assert "✅ Found 1 offers for 'starbucks':" in result.stdout  # Only BofA should match
    assert "⚠️ Warning: Some bank data was unavailable" in result.stdout
    assert "❌ Error: The HTML file 'missing.html' for Chase does not exist." in result.stdout


def test_search_offer_multiple_queries():
    """Test CLI handling multiple company queries."""
    result = subprocess.run(
        [
            "search_offer",
            "starbucks",
            "nike",
            "--bofa-html",
            TEST_HTML_FILES["bofa"],
            "--chase-html",
            TEST_HTML_FILES["chase"],
        ],
        capture_output=True,
        text=True,
    )
    assert "✅ Matches found for 'starbucks'" in result.stdout
    assert "✅ Matches found for 'nike'" in result.stdout


def test_search_offer_special_chars():
    """Test CLI handling special characters in company names."""
    result = subprocess.run(
        ["search_offer", "mc'donald's", "--bofa-html", TEST_HTML_FILES["bofa"]],
        capture_output=True,
        text=True,
    )
    assert "✅ Matches found for 'mc'donald's'" in result.stdout  # Should normalize correctly


def test_search_offer_case_insensitive():
    """Test CLI case insensitivity."""
    result = subprocess.run(
        ["search_offer", "STARBUCKS", "--bofa-html", TEST_HTML_FILES["bofa"]],
        capture_output=True,
        text=True,
    )
    assert "✅ Matches found for 'starbucks'" in result.stdout  # Should match regardless of case


def test_search_offer_warning_for_multiple_missing_files():
    """Test CLI handling multiple missing bank files gracefully."""
    result = subprocess.run(
        [
            "search_offer",
            "starbucks",
            "--bofa-html",
            "invalid.html",
            "--chase-html",
            "missing.html",
        ],
        capture_output=True,
        text=True,
    )
    assert "⚠️ Warning: Some bank data was unavailable" in result.stdout
    assert (
        "❌ Error: The HTML file 'invalid.html' for Bank of America does not exist."
        in result.stdout
    )
    assert "❌ Error: The HTML file 'missing.html' for Chase does not exist." in result.stdout
    assert (
        "❌ No offers found for any of the provided companies." in result.stdout
    )  # No valid banks left


def test_search_offer_save_to(tmp_path):
    """✅ Test CLI saving results to a JSON file."""
    output_file = tmp_path / "saved_offers.json"

    subprocess.run(
        [
            "search_offer",
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
