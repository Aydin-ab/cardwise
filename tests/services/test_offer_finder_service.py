from typing import List
from unittest.mock import MagicMock

import pytest

from cardwise.app.offer_finder_service import OfferFinderService, OfferMatcherWrapper
from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop


@pytest.fixture()
def offer(shop_name: str = "Costco", bank_name: str = "Amex") -> Offer:
    return Offer(
        shop=Shop(name=shop_name),
        bank=Bank(name=bank_name),
        offer_type=OfferTypeEnum.CASHBACK,
        description="5% back",
    )


@pytest.fixture
def mock_loader():
    return MagicMock()


@pytest.fixture
def mock_formatter():
    formatter = MagicMock()
    formatter.format.return_value = "Formatted Offers"
    return formatter


@pytest.fixture
def finder(mock_loader: MagicMock, mock_formatter: MagicMock, offer: Offer):
    mock_loader.get_or_restore_offers.return_value = [offer]
    offer_finder_service = OfferFinderService(
        data_loader=mock_loader, shop_matcher=MagicMock(), formatter=mock_formatter
    )
    offer_finder_service.matcher = MagicMock()
    offer_finder_service.matcher.match.return_value = [offer]  # always match
    return offer_finder_service


def test_find_offers_single_query(finder: OfferFinderService, mock_formatter: MagicMock):
    result = finder.find_offers("costco")

    assert result == "Formatted Offers"
    mock_formatter.format.assert_called_once()
    assert isinstance(result, str)


def test_find_offers_multiple_queries(finder: OfferFinderService, mock_formatter: MagicMock):
    result = finder.find_offers(["costco", "walmart"])

    assert result == "Formatted Offers"
    assert mock_formatter.format.call_count == 1


def test_caching_behavior(finder: OfferFinderService, mock_loader: MagicMock):
    finder.find_offers("query1")
    finder.find_offers("query2")
    # Loader should only be called once due to caching
    mock_loader.get_or_restore_offers.assert_called_once()


def test_clear_cache_triggers_reload(finder: OfferFinderService, mock_loader: MagicMock):
    finder.find_offers("query1")
    finder.clear_offers_cache()
    finder.find_offers("query2")

    assert mock_loader.get_or_restore_offers.call_count == 2


def make_offer(shop_name: str) -> Offer:
    return Offer(
        shop=Shop(name=shop_name),
        bank=Bank(name="Amex"),
        offer_type=OfferTypeEnum.CASHBACK,
        description=f"Deal at {shop_name}",
    )


@pytest.fixture
def offers():
    return [
        make_offer("Costco"),
        make_offer("Walmart"),
        make_offer("Target"),
    ]


def test_match_filters_by_matched_shop_names(offers: List[Offer]):
    # Mock matcher to match only "Walmart"
    mock_matcher = MagicMock()
    mock_matcher.match.return_value = [Shop(name="Walmart")]

    wrapper = OfferMatcherWrapper(mock_matcher)
    result = wrapper.match(offers, query="some query")

    assert len(result) == 1
    assert result[0].shop.name == "Walmart"
    mock_matcher.match.assert_called_once()


def test_match_returns_empty_if_no_matches(offers: List[Offer]):
    mock_matcher = MagicMock()
    mock_matcher.match.return_value = []

    wrapper = OfferMatcherWrapper(mock_matcher)
    result = wrapper.match(offers, query="doesn't match anything")

    assert result == []


def test_match_handles_duplicate_shops(offers: List[Offer]):
    # Add duplicate shop offer
    offers.append(make_offer("Costco"))

    mock_matcher = MagicMock()
    mock_matcher.match.return_value = [Shop(name="Costco")]

    wrapper = OfferMatcherWrapper(mock_matcher)
    result = wrapper.match(offers, query="costco")

    assert len(result) == 2
    assert all(offer.shop.name == "Costco" for offer in result)
