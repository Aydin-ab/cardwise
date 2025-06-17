import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop
from cardwise.persistence.models.offer_db import OfferDB
from ingestion.persistence.repository import OfferRepository


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="sample_offers")
def sample_offers_fixture() -> list[Offer]:
    return [
        Offer(
            shop=Shop(name="Walmart"),
            bank=Bank(name="Chase"),
            offer_type=OfferTypeEnum.CASHBACK,
            description="5% off groceries",
        ),
        Offer(
            shop=Shop(name="Target"),
            bank=Bank(name="Chase"),
            offer_type=OfferTypeEnum.CASHBACK,
            description="10% back on electronics",
        ),
    ]


def test_insert_and_delete_offers(session: Session, sample_offers: list[Offer]):
    repo = OfferRepository(session)

    # Insert offers
    repo.insert_many(sample_offers)
    result = session.exec(select(OfferDB)).all()
    assert len(result) == 2

    # Delete all offers
    repo.delete_all()
    result = session.exec(select(OfferDB)).all()
    assert result == []
