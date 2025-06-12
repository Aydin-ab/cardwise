from datetime import datetime, timedelta

import pytest

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop


@pytest.fixture
def shop():
    return Shop(name="Test Shop")


@pytest.fixture
def bank():
    return Bank(name="Test Bank")


@pytest.fixture
def offer(shop: Shop, bank: Bank):
    return Offer(
        shop=shop,
        bank=bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=datetime.now() + timedelta(days=1),
    )


def test_id(offer: Offer, shop: Shop, bank: Bank):
    expected_id = f"{shop.id}|{bank.id}|{OfferTypeEnum.CASHBACK}|10% cashback on all purchases"
    assert offer.id == expected_id


def test_is_expired_not_expired(offer: Offer):
    assert not offer.is_expired()


def test_is_expired_expired(shop: Shop, bank: Bank):
    expired_offer = Offer(
        shop=shop,
        bank=bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="Expired offer",
        expiry_date=datetime.now() - timedelta(days=1),
    )
    assert expired_offer.is_expired()


def test_is_expired_no_expiry_date(shop: Shop, bank: Bank):
    no_expiry_offer = Offer(
        shop=shop,
        bank=bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="No expiry date",
    )
    assert not no_expiry_offer.is_expired()


def test_hash(offer: Offer):
    assert hash(offer) == hash(offer.id)


def test_equality(offer: Offer, shop: Shop, bank: Bank):
    identical_offer = Offer(
        shop=shop,
        bank=bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback on all purchases",
        expiry_date=offer.expiry_date,
    )
    different_offer = Offer(
        shop=shop,
        bank=bank,
        offer_type=OfferTypeEnum.POINTS,
        description="5 points per dollar spent",
    )
    assert offer == identical_offer
    assert offer != different_offer
