from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch

import pytest

from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop
from cardwise.formatters.base import OfferFormatter
from cardwise.matchers.base import ShopMatcher
from cardwise.parsers.base import BankOfferParser
from cardwise.services.offer_finder import OfferFinderService


@pytest.fixture
def mock_parsers() -> List[BankOfferParser]:
    return [MagicMock(), MagicMock()]


@pytest.fixture
def mock_matcher() -> ShopMatcher:
    return MagicMock()


@pytest.fixture
def mock_formatter() -> OfferFormatter:
    return MagicMock()


@pytest.fixture
def html_dir() -> Path:
    return Path("/fake/html/dir")


@pytest.fixture
def offer_finder_service(
    mock_parsers: List[BankOfferParser], mock_matcher: ShopMatcher, mock_formatter: OfferFormatter, html_dir: Path
) -> OfferFinderService:
    return OfferFinderService(
        parsers=mock_parsers,
        matcher=mock_matcher,
        formatter=mock_formatter,
        html_dir=html_dir,
    )


def test_get_default_path_from_parser(offer_finder_service: OfferFinderService, mock_parsers: List[MagicMock]):
    mock_parsers[0].bank.bank_id = "bank1"

    result = offer_finder_service._get_default_path_from_parser(mock_parsers[0])  # type: ignore
    assert result == Path("/fake/html/dir/bank1_offers.html")


def test_load_offers_from_parser(offer_finder_service: OfferFinderService, mock_parsers: List[MagicMock]):
    offer = Offer(
        shop=Shop(name="Shop1"), bank_info=BankInfo(name="Bank 1"), offer_type="cashback", description="Cashback offer"
    )
    mock_parsers[0].parse.return_value = [offer]

    with patch("pathlib.Path.exists", return_value=True):
        offers = offer_finder_service._load_offers_from_parser(mock_parsers[0])  # type: ignore

    assert len(offers) == 1
    assert offers[0].shop.name == "Shop1"
    mock_parsers[0].parse.assert_called_once()


def test_load_offers_from_parser_no_file(offer_finder_service: OfferFinderService, mock_parsers: List[MagicMock]):
    mock_parsers[0].parse.return_value = []

    with patch("pathlib.Path.exists", return_value=False):
        offers = offer_finder_service._load_offers_from_parser(mock_parsers[0])  # type: ignore

    assert len(offers) == 0
    mock_parsers[0].parse.assert_not_called()


def test_load_all_offers_without_cache(offer_finder_service: OfferFinderService, mock_parsers: List[MagicMock]):
    offer1 = Offer(
        shop=Shop(name="Shop1"), bank_info=BankInfo(name="Bank 1"), offer_type="cashback", description="Cashback offer"
    )
    offer2 = Offer(
        shop=Shop(name="Shop2"), bank_info=BankInfo(name="Bank 2"), offer_type="points", description="Points offer"
    )
    mock_parsers[0].parse.return_value = [offer1]
    mock_parsers[1].parse.return_value = [offer2]

    with patch("pathlib.Path.exists", return_value=True):
        offers = offer_finder_service._load_all_offers()  # type: ignore

    assert len(offers) == 2
    assert offers[0].shop.name == "Shop1"
    assert offers[1].shop.name == "Shop2"
    assert offer_finder_service._cached_offers == offers  # type: ignore


def test_load_all_offers_with_cache(offer_finder_service: OfferFinderService):
    offer1 = Offer(
        shop=Shop(name="Shop1"), bank_info=BankInfo(name="Bank 1"), offer_type="cashback", description="Cashback offer"
    )
    offer_finder_service._cached_offers = [offer1]  # type: ignore
    offers = offer_finder_service._load_all_offers()  # type: ignore

    assert offers == offer_finder_service._cached_offers  # type: ignore


def test_precompute_offers(offer_finder_service: OfferFinderService, mock_parsers: List[MagicMock]):
    offer1 = Offer(
        shop=Shop(name="Shop1"), bank_info=BankInfo(name="Bank 1"), offer_type="cashback", description="Cashback offer"
    )
    mock_parsers[0].parse.return_value = [offer1]

    with patch("pathlib.Path.exists", return_value=True):
        offer_finder_service.precompute_offers()
    cached_offers = offer_finder_service._cached_offers  # type: ignore
    assert cached_offers is not None
    assert len(cached_offers) == 1
    assert cached_offers[0].shop.name == "Shop1"


def test_clear_cache(offer_finder_service: OfferFinderService):
    cached_offers = [
        Offer(
            shop=Shop(name="Shop1"),
            bank_info=BankInfo(name="Bank 1"),
            offer_type="cashback",
            description="Cashback offer",
        )
    ]
    offer_finder_service._cached_offers = cached_offers  # type: ignore
    offer_finder_service.clear_offers_cache()
    assert offer_finder_service._cached_offers is None  # type: ignore


def test_get_matching_offers(offer_finder_service: OfferFinderService, mock_matcher: MagicMock):
    offer1 = Offer(
        shop=Shop(name="Shop1"), bank_info=BankInfo(name="Bank 1"), offer_type="cashback", description="Cashback offer"
    )
    offer2 = Offer(
        shop=Shop(name="Shop2"), bank_info=BankInfo(name="Bank 2"), offer_type="points", description="Points offer"
    )
    offer_finder_service._cached_offers = [offer1, offer2]  # type: ignore
    mock_matcher.match.return_value = [Shop(name="Shop1")]

    matching_offers = offer_finder_service._get_matching_offers("query")  # type: ignore
    assert matching_offers == [offer1]
    unique_shops = list({offer.shop for offer in offer_finder_service._cached_offers})  # type: ignore
    mock_matcher.match.assert_called_once_with("query", unique_shops)  # type: ignore


def test_find_offers_single_query(offer_finder_service: OfferFinderService, mock_formatter: MagicMock):
    offer1 = Offer(
        shop=Shop(name="Shop1"), bank_info=BankInfo(name="Bank 1"), offer_type="cashback", description="Cashback offer"
    )
    offer_finder_service._get_matching_offers = MagicMock(return_value=[offer1])  # type: ignore
    mock_formatter.format.return_value = "Formatted Offers"

    result = offer_finder_service._find_offers_single_query("query")  # type: ignore
    assert result == "Formatted Offers"
    offer_finder_service._get_matching_offers.assert_called_once_with("query")  # type: ignore
    mock_formatter.format.assert_called_once_with([offer1])


def test_find_offers_batch_query(offer_finder_service: OfferFinderService, mock_formatter: MagicMock):
    offer1 = Offer(
        shop=Shop(name="Shop1"), bank_info=BankInfo(name="Bank 1"), offer_type="cashback", description="Cashback offer"
    )
    offer2 = Offer(
        shop=Shop(name="Shop2"), bank_info=BankInfo(name="Bank 2"), offer_type="points", description="Points offer"
    )
    offer_finder_service._get_matching_offers = MagicMock(  # type: ignore
        side_effect=[
            [offer1],
            [offer2],
        ]
    )  # Mock internal method
    mock_formatter.format.return_value = "Formatted Batch Offers"

    result = offer_finder_service._find_offers_batch_query(["query1", "query2"])  # type: ignore
    assert result == "Formatted Batch Offers"
    offer_finder_service._get_matching_offers.assert_any_call("query1")  # type: ignore
    offer_finder_service._get_matching_offers.assert_any_call("query2")  # type: ignore
    mock_formatter.format.assert_called_once_with([offer1, offer2])


def test_find_offers_single_query_input(offer_finder_service: OfferFinderService):
    offer_finder_service._find_offers_single_query = MagicMock(return_value="Single Query Result")  # type: ignore # Mock internal method

    result = offer_finder_service.find_offers("query")
    assert result == "Single Query Result"
    offer_finder_service._find_offers_single_query.assert_called_once_with("query")  # type: ignore


def test_find_offers_batch_query_input(offer_finder_service: OfferFinderService):
    offer_finder_service._find_offers_batch_query = MagicMock(return_value="Batch Query Result")  # type: ignore # Mock internal method

    result = offer_finder_service.find_offers(["query1", "query2"])
    assert result == "Batch Query Result"
    offer_finder_service._find_offers_batch_query.assert_called_once_with(["query1", "query2"])  # type: ignore
