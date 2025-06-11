from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop
from cardwise.infrastructure.db.mapper import db_to_offer, offer_to_db
from cardwise.infrastructure.db.models import BankDB, OfferDB, ShopDB
from cardwise.infrastructure.db.repositories.SQLModel_offer_repository import SQLModelOfferRepository


@pytest.fixture(name="repo")
def repo_fixture() -> SQLModelOfferRepository:
    # In-memory SQLite engine
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    # Override get_session for this test instance
    class TestRepo(SQLModelOfferRepository):
        def __init__(self):
            self._engine = engine

        def get_all(self):
            with Session(self._engine) as session:
                offer_dbs = session.exec(select(OfferDB)).all()
                return [
                    db_to_offer(
                        o,
                        session.get(ShopDB, o.shop_id),
                        session.get(BankDB, o.bank_id),
                    )
                    for o in offer_dbs
                ]

        def save_all(self, offers: list[Offer]) -> None:
            with Session(self._engine) as session:
                for offer in offers:
                    offer_db, shop_db, bank_db = offer_to_db(offer)

                    if not session.get(ShopDB, shop_db.id):
                        session.add(shop_db)
                    if not session.get(BankDB, bank_db.id):
                        session.add(bank_db)
                    session.add(offer_db)

                session.commit()

        def refresh(self):
            SQLModel.metadata.drop_all(self._engine)
            SQLModel.metadata.create_all(self._engine)

    return TestRepo()


@pytest.fixture()
def offer() -> Offer:
    return Offer(
        shop=Shop(name="Costco"),
        bank=Bank(name="Amex"),
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% back",
        expiry_date=datetime(2025, 12, 31),
    )


def test_save_and_get_offer_roundtrip(repo: SQLModelOfferRepository, offer: Offer):
    repo.save_all([offer])

    offers = repo.get_all()
    assert len(offers) == 1
    restored = offers[0]

    assert restored.id == offer.id
    assert restored.shop.name == offer.shop.name
    assert restored.bank.name == offer.bank.name
    assert restored.description == offer.description
    assert restored.expiry_date == offer.expiry_date


def test_refresh_clears_data(repo: SQLModelOfferRepository, offer: Offer):
    repo.save_all([offer])
    assert len(repo.get_all()) == 1

    repo.refresh()
    assert repo.get_all() == []
