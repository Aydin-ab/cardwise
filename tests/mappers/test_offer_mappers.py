from datetime import datetime

import pytest

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop
from cardwise.infrastructure.db.mapper import db_to_offer, offer_to_db
from cardwise.infrastructure.db.models import BankDB, OfferDB, ShopDB


@pytest.fixture()
def offer() -> Offer:
    return Offer(
        shop=Shop(name="Costco"),
        bank=Bank(name="Amex"),
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback at Costco",
        expiry_date=datetime(2025, 12, 31),
    )


def test_offer_to_db_returns_all_db_models(offer: Offer):
    offer_db, shop_db, bank_db = offer_to_db(offer)

    assert isinstance(offer_db, OfferDB)
    assert offer_db.id == offer.id
    assert offer_db.shop_id == shop_db.id
    assert offer_db.bank_id == bank_db.id
    assert offer_db.offer_type == offer.offer_type
    assert offer_db.description == offer.description
    assert offer_db.expiry_date == offer.expiry_date

    assert isinstance(shop_db, ShopDB)
    assert shop_db.id == offer.shop.id
    assert shop_db.name == offer.shop.name

    assert isinstance(bank_db, BankDB)
    assert bank_db.id == offer.bank.id
    assert bank_db.name == offer.bank.name


def test_db_to_offer_reconstructs_correctly(offer: Offer):
    offer_db, shop_db, bank_db = offer_to_db(offer)

    reconstructed = db_to_offer(offer_db, shop_db, bank_db)

    assert isinstance(reconstructed, Offer)
    assert reconstructed.id == offer.id
    assert reconstructed.shop.name == "Costco"
    assert reconstructed.bank.name == "Amex"
    assert reconstructed.offer_type == OfferTypeEnum.CASHBACK
    assert reconstructed.description == "10% cashback at Costco"
    assert reconstructed.expiry_date == datetime(2025, 12, 31)


def test_db_to_offer_raises_if_missing_shop(offer: Offer):
    offer_db, _, bank_db = offer_to_db(offer)

    with pytest.raises(ValueError, match="Shop not found"):
        db_to_offer(offer_db, shop=None, bank=bank_db)


def test_db_to_offer_raises_if_missing_bank(offer: Offer):
    offer_db, shop_db, _ = offer_to_db(offer)

    with pytest.raises(ValueError, match="BankInfo not found"):
        db_to_offer(offer_db, shop=shop_db, bank=None)
