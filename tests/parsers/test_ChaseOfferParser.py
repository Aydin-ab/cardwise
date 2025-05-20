from typing import List

import pytest
from bs4 import BeautifulSoup

from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop
from cardwise.exceptions import (
    OfferDescriptionParsingError,
    OfferParsingError,
    OfferShopNameParsingError,
)
from cardwise.parsers.ChaseOfferParser import ChaseOfferParser


@pytest.fixture
def parser():
    return ChaseOfferParser()


def test_extract_offers_success(parser: ChaseOfferParser):
    html = """
    <div class="r9jbije r9jbijl">
        <span>Shop A</span>
        <span>10% cashback</span>
    </div>
    <div class="r9jbije r9jbijl">
        <span>Shop B</span>
        <span>15% cashback</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    offers: List[Offer] = parser._extract_offers(soup)  # type: ignore

    expected_offers = [
        Offer(shop=Shop(name="Shop A"), bank_info=parser.bank, offer_type="cashback", description="10% cashback"),
        Offer(shop=Shop(name="Shop B"), bank_info=parser.bank, offer_type="cashback", description="15% cashback"),
    ]

    assert offers == expected_offers


def test_extract_offers_no_divs(parser: ChaseOfferParser):
    html = "<div>No offers here</div>"
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferParsingError, match="No valid divs found"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_missing_shop_name(parser: ChaseOfferParser):
    html = """
    <div class="r9jbije r9jbijl">
        <span></span>
        <span>10% cashback</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferShopNameParsingError, match="Missing text in span tag"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_missing_description(parser: ChaseOfferParser):
    html = """
    <div class="r9jbije r9jbijl">
        <span>Shop A</span>
        <span></span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferDescriptionParsingError, match="Missing text in span tag"):
        parser._extract_offers(soup)  # type: ignore


def test_extract_offers_incomplete_spans(parser: ChaseOfferParser):
    html = """
    <div class="r9jbije r9jbijl">
        <span>Shop A</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    with pytest.raises(OfferParsingError, match="Offer data is incomplete: need at least 2 spans"):
        parser._extract_offers(soup)  # type: ignore
