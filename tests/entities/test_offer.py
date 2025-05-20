from datetime import datetime, timedelta

import pytest

from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop


@pytest.fixture
def shop():
    return Shop(name="Test Shop")


@pytest.fixture
def bank():
    return BankInfo(name="Test Bank")


@pytest.fixture
def offer(shop: Shop, bank: BankInfo):
    return Offer(
        shop=shop,
        bank_info=bank,
        offer_type="cashback",
        description="10% cashback on all purchases",
        expiry_date=datetime.now() + timedelta(days=1),
    )


def test_id(offer: Offer, shop: Shop, bank: BankInfo):
    expected_id = f"{shop.name}|{bank.name}|cashback|10% cashback on all purchases"
    assert offer.id == expected_id


def test_is_expired_not_expired(offer: Offer):
    assert not offer.is_expired()


def test_is_expired_expired(shop: Shop, bank: BankInfo):
    expired_offer = Offer(
        shop=shop,
        bank_info=bank,
        offer_type="cashback",
        description="Expired offer",
        expiry_date=datetime.now() - timedelta(days=1),
    )
    assert expired_offer.is_expired()


def test_is_expired_no_expiry_date(shop: Shop, bank: BankInfo):
    no_expiry_offer = Offer(
        shop=shop,
        bank_info=bank,
        offer_type="cashback",
        description="No expiry date",
    )
    assert not no_expiry_offer.is_expired()


def test_hash(offer: Offer):
    assert hash(offer) == hash(offer.id)


def test_equality(offer: Offer, shop: Shop, bank: BankInfo):
    identical_offer = Offer(
        shop=shop,
        bank_info=bank,
        offer_type="cashback",
        description="10% cashback on all purchases",
        expiry_date=offer.expiry_date,
    )
    different_offer = Offer(
        shop=shop,
        bank_info=bank,
        offer_type="points",
        description="5 points per dollar spent",
    )
    assert offer == identical_offer
    assert offer != different_offer
