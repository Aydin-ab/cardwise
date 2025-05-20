from datetime import datetime, timedelta

import pytest

from cardwise.entities.Bank import Bank
from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop


@pytest.fixture
def bank_info() -> BankInfo:
    return BankInfo(name="Test Bank", bank_id="123")


@pytest.fixture
def bank(bank_info: BankInfo) -> Bank:
    return Bank(metadata=bank_info)


@pytest.fixture
def shop() -> Shop:
    return Shop(name="Test Shop")


@pytest.fixture
def offers(bank_info: BankInfo, shop: Shop) -> list[Offer]:
    return [
        Offer(shop=shop, bank_info=bank_info, offer_type="cashback", description="10% cashback"),
        Offer(shop=shop, bank_info=bank_info, offer_type="points", description="Earn 100 points"),
    ]


def test_add_offer(bank: Bank, bank_info: BankInfo, shop: Shop):
    # Arrange
    offer = Offer(shop=shop, bank_info=bank_info, offer_type="cashback", description="10% cashback")

    # Act
    bank.add_offer(offer)

    # Assert
    assert len(bank.offers) == 1
    assert bank.offers[0] == offer


def test_add_batch_offers(bank: Bank, offers: list[Offer]):
    # Act
    bank.add_batch_offers(offers)

    # Assert
    assert len(bank.offers) == len(offers)
    assert bank.offers == offers


def test_offer_integration_with_bank(bank: Bank, bank_info: BankInfo, shop: Shop):
    # Arrange
    expiry_date = datetime.now() + timedelta(days=1)
    offer = Offer(
        shop=shop, bank_info=bank_info, offer_type="cashback", description="10% cashback", expiry_date=expiry_date
    )

    # Act
    bank.add_offer(offer)

    # Assert
    assert len(bank.offers) == 1
    assert not bank.offers[0].is_expired()
    assert bank.offers[0].id == "Test Shop|Test Bank|cashback|10% cashback"
