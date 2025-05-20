import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from cardwise.cli.main import main
from cardwise.exceptions import CardwiseError


@pytest.fixture
def html_dir_with_samples(tmp_path: Path):
    html_dir = tmp_path / "htmls"
    html_dir.mkdir()

    # Bank of America
    (html_dir / "bank_of_america_offers.html").write_text("""
    <div class="deal-logo-wrapper top">
        <div class="deal-logo">
            <img alt="Starbucks Logo" src="https://example.com/starbucks.png">
        </div>
        <span class="deal-offer-percent">10% Cash Back</span>
    </div>
    <div class="deal-logo-wrapper top">
        <div class="deal-logo">
            <img alt="McDonald's Logo" src="https://example.com/mcdonalds.png">
        </div>
        <span class="deal-offer-percent">5% Cash Back</span>
    </div>
    """)

    # Capital One
    (html_dir / "capital_one_offers.html").write_text("""
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <div class="flex flex-col items-center justify-center w-full h-full">
            <img src="https://images.capitaloneshopping.com/api/v1/logos?domain=starbucks.com">
        </div>
        <div class="border-none text-center">5X miles</div>
    </div>
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <div class="flex flex-col items-center justify-center w-full h-full">
            <img src="https://images.capitaloneshopping.com/api/v1/logos?domain=adidas.com">
        </div>
        <div class="border-none text-center">10X miles</div>
    </div>
    """)

    # Chase
    (html_dir / "chase_offers.html").write_text("""
    <div class="r9jbije r9jbijl">
        <span class="mds-body-small-heavier r9jbijk semanticColorTextRegular ">McDonald's</span>
        <span class="mds-body-large-heavier r9jbijj semanticColorTextRegular ">5% cash back</span>
    </div>
    <div class="r9jbije r9jbijl">
        <span class="mds-body-small-heavier r9jbijk semanticColorTextRegular ">Nike</span>
        <span class="mds-body-large-heavier r9jbijj semanticColorTextRegular ">15% cash back</span>
    </div>
    """)

    return html_dir


def test_cli_outputs_stdout(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str], html_dir_with_samples: Path):
    monkeypatch.setattr(sys, "argv", ["cli", "starbucks", "--html-dir", str(html_dir_with_samples)])
    main()

    out = capsys.readouterr().out
    assert "[Bank of America]" in out
    assert "Starbucks" in out
    assert "CASHBACK" in out
    assert "10% Cash Back" in out or "5X miles" in out
    assert "(no expiry date found)" in out


def test_cli_outputs_to_json_file(monkeypatch: MonkeyPatch, tmp_path: Path, html_dir_with_samples: Path):
    json_file = tmp_path / "results.json"
    monkeypatch.setattr(
        sys, "argv", ["cli", "nike", "--json", str(json_file), "--html-dir", str(html_dir_with_samples)]
    )

    main()

    assert json_file.exists()
    content = json_file.read_text()
    assert "Nike" in content
    assert "15%" in content


def test_cli_no_match(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str], html_dir_with_samples: Path):
    monkeypatch.setattr(sys, "argv", ["cli", "nonexistentstore", "--html-dir", str(html_dir_with_samples)])
    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    out = capsys.readouterr().out
    assert "No offers found" in out


def test_cli_cardwise_nofiles(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str], tmp_path: Path):
    bad_dir = tmp_path / "no_such_folder"
    monkeypatch.setattr(sys, "argv", ["cli", "nike", "--html-dir", str(bad_dir)])
    main()
    out = capsys.readouterr().out
    assert "No offers found." in out


def test_cli_handles_cardwise_exception(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]):
    # Simulate CLI args
    monkeypatch.setattr(sys, "argv", ["cli", "starbucks", "--html-dir", "fake_dir"])

    # Patch OfferFinderService.find_offers to raise CardwiseError
    with patch(
        "cardwise.services.offer_finder.OfferFinderService.find_offers", side_effect=CardwiseError("Fake parsing error")
    ):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1
        err = capsys.readouterr().err
        assert "❌ Error: Fake parsing error" in err

    with patch(
        "cardwise.services.offer_finder.OfferFinderService.find_offers", side_effect=Exception("Fake parsing error")
    ):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 2
        err = capsys.readouterr().err
        assert "Unexpected error" in err
