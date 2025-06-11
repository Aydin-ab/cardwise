import json
from datetime import datetime, timedelta

import pytest

from cardwise.domain.formatters.json_offer_formatter import JSONOfferFormatter
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
def json_formatter():
    return JSONOfferFormatter()


def test_no_offers(json_formatter: JSONOfferFormatter):
    result = json_formatter.format([])
    parsed = json.loads(result)
    assert parsed == []


def test_json_output(json_formatter: JSONOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    expires_soon = datetime.now() + timedelta(days=5)
    offer = Offer(
        shop=sample_shop,
        bank=sample_bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=expires_soon,
    )
    result = json_formatter.format([offer])
    parsed = json.loads(result)
    assert len(parsed) == 1
    assert Shop.model_validate(parsed[0]["shop"]) == sample_shop
    assert Bank.model_validate(parsed[0]["bank"]) == sample_bank
    assert Offer.model_validate(parsed[0]) == offer
    assert parsed[0]["expiry_date"] == expires_soon.isoformat()


def test_response_length_multiple_offers(json_formatter: JSONOfferFormatter, sample_bank: Bank, sample_shop: Shop):
    expires_soon = datetime.now() + timedelta(days=2)
    offers = [
        Offer(
            shop=sample_shop,
            bank=sample_bank,
            offer_type=OfferTypeEnum.CASHBACK,
            description="10% cashback on electronics",
            expiry_date=expires_soon,
        ),
        Offer(
            shop=sample_shop,
            bank=sample_bank,
            offer_type=OfferTypeEnum.CASHBACK,
            description="Special holiday offer",
            expiry_date=None,
        ),
    ]
    result = json_formatter.format(offers)
    parsed = json.loads(result)
    assert len(parsed) == 2
