from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from cardwise.domain.models.offer import OfferTypeEnum
from cardwise.infrastructure.db.models import BankDB, OfferDB, ShopDB


@pytest.fixture(name="session")
def session_fixture():
    # Use in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_insert_and_read_shop(session: Session):
    shop = ShopDB(id="costco", name="Costco")
    session.add(shop)
    session.commit()

    result = session.exec(select(ShopDB).where(ShopDB.id == "costco")).one()
    assert result.name == "Costco"


def test_insert_and_read_bank(session: Session):
    bank = BankDB(id="amex", name="American Express")
    session.add(bank)
    session.commit()

    result = session.exec(select(BankDB).where(BankDB.id == "amex")).one()
    assert result.name == "American Express"


def test_offer_with_foreign_keys(session: Session):
    # Insert dependencies
    shop = ShopDB(id="costco", name="Costco")
    bank = BankDB(id="amex", name="Amex")
    session.add(shop)
    session.add(bank)
    session.commit()

    # Insert offer
    offer = OfferDB(
        id="costco|amex|cashback|10% back",
        shop_id="costco",
        bank_id="amex",
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% cashback at Costco",
        expiry_date=datetime(2025, 12, 31),
    )
    session.add(offer)
    session.commit()

    result = session.exec(select(OfferDB).where(OfferDB.id == offer.id)).one()
    assert result.shop_id == "costco"
    assert result.bank_id == "amex"
    assert result.offer_type == OfferTypeEnum.CASHBACK
    assert result.description == "10% cashback at Costco"
