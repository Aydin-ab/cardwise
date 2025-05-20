from pathlib import Path
from typing import List

import pytest
from bs4 import BeautifulSoup

from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop
from cardwise.exceptions import OfferSourceNotFound
from cardwise.parsers.base import BankOfferParser


class MockBankOfferParser(BankOfferParser):
    """Mock implementation of BankOfferParser for testing."""

    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        # Mock implementation: Extract offers based on a specific tag
        offers: List[Offer] = []
        for offer_tag in soup.find_all("offer"):
            offer_type = offer_tag.get("type", "misc")  # type: ignore
            offers.append(
                Offer(
                    shop=Shop(name="Mock Shop"),
                    bank_info=self.bank,
                    offer_type=offer_type,  # type: ignore
                    description=offer_tag.text,
                    expiry_date=None,
                )
            )
        return offers


@pytest.fixture
def mock_parser():
    return MockBankOfferParser(bank_name="Mock Bank", parser_id="mock_bank")


def test_parse_file_not_found(mock_parser: MockBankOfferParser):
    non_existent_path = Path("non_existent_file.html")
    with pytest.raises(OfferSourceNotFound, match="non_existent_file.html"):
        mock_parser.parse(non_existent_path)


def test_parse_valid_html(mock_parser: MockBankOfferParser, tmp_path: Path):
    # Create a temporary HTML file
    html_content = """
    <html>
        <body>
            <offer type="cashback">10% cashback on electronics</offer>
            <offer type="points">Earn double points on groceries</offer>
        </body>
    </html>
    """
    html_file = tmp_path / "offers.html"
    html_file.write_text(html_content, encoding="utf-8")

    # Parse the file
    offers = mock_parser.parse(html_file)

    # Validate the parsed offers
    assert len(offers) == 2
    assert offers[0].offer_type == "cashback"
    assert offers[0].description == "10% cashback on electronics"
    assert offers[1].offer_type == "points"
    assert offers[1].description == "Earn double points on groceries"
