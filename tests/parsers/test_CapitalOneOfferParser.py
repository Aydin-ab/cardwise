import pytest
from bs4 import BeautifulSoup

from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop
from cardwise.infrastructure.parsers.capital_one_offer_parser import CapitalOneOfferParser
from cardwise.shared.exceptions import (
    OfferDescriptionParsingError,
    OfferParsingError,
    OfferShopNameParsingError,
)


@pytest.fixture
def parser():
    return CapitalOneOfferParser()


def test_extract_offers_success(parser: CapitalOneOfferParser):
    html = """
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <img src="https://example.com/image?domain=shopa.com" />
        <div>Some irrelevant div</div>
        <div>Earn 5x points on purchases</div>
    </div>
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <img src="https://example.com/image?domain=shopb.com" />
        <div>Some irrelevant div</div>
        <div>Earn 10x points on travel</div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    offers: set[Offer] = set(parser._extract_offers(soup))  # type: ignore

    expected_offers = set(
        [
            Offer(
                shop=Shop(name="shopa"),
                bank=parser.bank,
                offer_type=OfferTypeEnum.POINTS,
                description="Earn 5x points on purchases",
            ),
            Offer(
                shop=Shop(name="shopb"),
                bank=parser.bank,
                offer_type=OfferTypeEnum.POINTS,
                description="Earn 10x points on travel",
            ),
        ]
    )

    assert offers == expected_offers


def test_extract_offers_no_tiles(parser: CapitalOneOfferParser):
    html = "<div>No offers here</div>"
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferParsingError, match="No tile elements found"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_missing_img_src(parser: CapitalOneOfferParser):
    html = """
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <img />
        <div>Some irrelevant div</div>
        <div>Earn 5x points on purchases</div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferShopNameParsingError, match="Missing 'src' in image tag"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_invalid_img_src(parser: CapitalOneOfferParser):
    html = """
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <img src="https://example.com/image" />
        <div>Some irrelevant div</div>
        <div>Earn 5x points on purchases</div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferShopNameParsingError, match="Not in expected position at URL"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_missing_description_divs(parser: CapitalOneOfferParser):
    html = """
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <img src="https://example.com/image?domain=shopa.com" />
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferDescriptionParsingError, match="Expected >2 divs with description at index 1"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_empty_description(parser: CapitalOneOfferParser):
    html = """
    <div class="standard-tile relative flex flex-col justify-between w-full h-full mt-0">
        <img src="https://example.com/image?domain=shopa.com" />
        <div>Some irrelevant div</div>
        <div></div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferDescriptionParsingError, match="Missing text in div tag"):
        parser._extract_offers(soup)  # type: ignore
