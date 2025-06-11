from datetime import datetime, timedelta

import pytest

from cardwise.domain.formatters.cli_offer_formatter import CLIOfferFormatter
from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop


@pytest.fixture
def sample_bank():
    return Bank(name="Sample Bank")


@pytest.fixture
def sample_shop():
    return Shop(name="Sample Shop")


@pytest.fixture
def cli_formatter():
    return CLIOfferFormatter()


def test_format_no_offers(cli_formatter: CLIOfferFormatter):
    result = cli_formatter.format([])
    assert result == "\033[2mNo offers found.\033[0m"


def test_format_offer_bank_name(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=None,
    )
    result = cli_formatter.format([offer])
    assert f"\033[36m[{sample_bank.name}]\033[0m" in result


def test_format_offer_shop_name(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=None,
    )
    result = cli_formatter.format([offer])
    assert f"\033[1m\033[37m{sample_shop.name}\033[0m" in result


def test_format_offer_type_cashback(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=None,
    )
    result = cli_formatter.format([offer])
    assert "\033[32mCASHBACK\033[0m" in result


def test_format_offer_type_points(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.POINTS,
        description="Earn double points on groceries",
        expiry_date=None,
    )
    result = cli_formatter.format([offer])
    assert "\033[34mPOINTS\033[0m" in result


def test_format_offer_type_misc(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.MISC,
        description="Special holiday offer",
        expiry_date=None,
    )
    result = cli_formatter.format([offer])
    assert "\033[35mMISC\033[0m" in result


def test_format_offer_description(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=None,
    )
    result = cli_formatter.format([offer])
    assert "10% cashback on all purchases" in result


def test_format_offer_expiry_date(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    expires_soon = datetime.now() + timedelta(days=5)
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=expires_soon,
    )
    result = cli_formatter.format([offer])
    assert f"\033[2m(expires: {expires_soon.date()})\033[0m" in result


def test_format_offer_no_expiry_date(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=None,
    )
    result = cli_formatter.format([offer])
    assert "\033[2m(no expiry date found)\033[0m" in result


def test_format_multiple_offers_length(cli_formatter: CLIOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    offers = [
        Offer(
            shop=sample_shop,
            bank=sample_bank,
            offer_type=OfferTypeEnum.CASHBACK,
            description="10% cashback on electronics",
            expiry_date=datetime.now() + timedelta(days=2),
        ),
        Offer(
            shop=sample_shop,
            bank=sample_bank,
            offer_type=OfferTypeEnum.MISC,
            description="Special holiday offer",
            expiry_date=None,
        ),
        Offer(
            shop=sample_shop,
            bank=sample_bank,
            offer_type=OfferTypeEnum.POINTS,
            description="Earn triple points on travel",
            expiry_date=datetime.now() + timedelta(days=10),
        ),
        Offer(
            shop=sample_shop,
            bank=sample_bank,
            offer_type=OfferTypeEnum.CASHBACK,
            description="5% cashback on groceries",
            expiry_date=None,
        ),
        Offer(
            shop=sample_shop,
            bank=sample_bank,
            offer_type=OfferTypeEnum.MISC,
            description="Limited time offer",
            expiry_date=datetime.now() - timedelta(days=20),
        ),
    ]
    result = cli_formatter.format(offers)
    lines = result.splitlines()
    assert len(lines) == 5
