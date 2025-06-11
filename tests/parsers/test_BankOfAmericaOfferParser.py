import pytest
from bs4 import BeautifulSoup

from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop
from cardwise.infrastructure.parsers.bank_of_america_offer_parser import BankOfAmericaOfferParser
from cardwise.shared.exceptions import (
    OfferDescriptionParsingError,
    OfferParsingError,
    OfferShopNameParsingError,
)


@pytest.fixture
def parser():
    return BankOfAmericaOfferParser()


def test_extract_offers_success(parser: BankOfAmericaOfferParser):
    html = """
    <div class="deal-logo-wrapper top">
        <img alt="Shop A Logo" />
        <span class="deal-offer-percent">10% cashback</span>
    </div>
    <div class="deal-logo-wrapper top">
        <img alt="Shop B Logo" />
        <span class="deal-offer-percent">15% cashback</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    offers: set[Offer] = set(parser._extract_offers(soup))  # type: ignore

    expected_offers = set(
        [
            Offer(
                shop=Shop(name="Shop A"),
                bank=parser.bank,
                offer_type=OfferTypeEnum.CASHBACK,
                description="10% cashback",
            ),
            Offer(
                shop=Shop(name="Shop B"),
                bank=parser.bank,
                offer_type=OfferTypeEnum.CASHBACK,
                description="15% cashback",
            ),
        ]
    )

    assert offers == expected_offers


def test_extract_offers_no_wrappers(parser: BankOfAmericaOfferParser):
    html = "<div>No offers here</div>"
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferParsingError, match="No offer wrappers found"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_missing_alt(parser: BankOfAmericaOfferParser):
    html = """
    <div class="deal-logo-wrapper top">
        <img />
        <span class="deal-offer-percent">10% cashback</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferShopNameParsingError, match="Missing 'alt' in img tag"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_missing_span(parser: BankOfAmericaOfferParser):
    html = """
    <div class="deal-logo-wrapper top">
        <img alt="Shop A Logo" />
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferDescriptionParsingError, match="Span found is not a tag"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_empty_span(parser: BankOfAmericaOfferParser):
    html = """
    <div class="deal-logo-wrapper top">
        <img alt="Shop A Logo" />
        <span class="deal-offer-percent"></span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferDescriptionParsingError, match="Missing text in span tag"):
        parser._extract_offers(soup)  # type: ignore
