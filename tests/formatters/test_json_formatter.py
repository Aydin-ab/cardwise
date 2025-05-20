import json
from datetime import datetime, timedelta

import pytest

from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop
from cardwise.formatters.json_formatter import JSONFormatter


@pytest.fixture
def sample_bank():
    return BankInfo(name="Sample Bank")


@pytest.fixture
def sample_shop():
    return Shop(name="Sample Shop")


@pytest.fixture
def json_formatter():
    return JSONFormatter()


def test_no_offers(json_formatter: JSONFormatter):
    result = json_formatter.format([])
    parsed = json.loads(result)
    assert parsed == []


def test_json_output(json_formatter: JSONFormatter, sample_bank: BankInfo, sample_shop: Shop):
    expires_soon = datetime.now() + timedelta(days=5)
    offer = Offer(
        shop=sample_shop,
        bank_info=sample_bank,
        offer_type="cashback",
        description="10% cashback on all purchases",
        expiry_date=expires_soon,
    )
    result = json_formatter.format([offer])
    parsed = json.loads(result)
    assert len(parsed) == 1
    assert Shop.model_validate(parsed[0]["shop"]) == sample_shop
    assert BankInfo.model_validate(parsed[0]["bank_info"]) == sample_bank
    assert Offer.model_validate(parsed[0]) == offer
    assert parsed[0]["expiry_date"] == expires_soon.isoformat()


def test_response_length_multiple_offers(json_formatter: JSONFormatter, sample_bank: BankInfo, sample_shop: Shop):
    expires_soon = datetime.now() + timedelta(days=2)
    offers = [
        Offer(
            shop=sample_shop,
            bank_info=sample_bank,
            offer_type="cashback",
            description="10% cashback on electronics",
            expiry_date=expires_soon,
        ),
        Offer(
            shop=sample_shop,
            bank_info=sample_bank,
            offer_type="misc",
            description="Special holiday offer",
            expiry_date=None,
        ),
    ]
    result = json_formatter.format(offers)
    parsed = json.loads(result)
    assert len(parsed) == 2
