from datetime import datetime, timedelta
from unittest.mock import MagicMock

from backend.app.services.offer_service import OfferService
from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop
from cardwise.persistence.models.offer_db import OfferDB


def make_offer_db(shop_name: str, bank_name: str = "Bank A") -> OfferDB:
    """
    Create a fake OfferDB object with a realistic .to_domain() implementation.
    """
    shop = Shop(name=shop_name)
    bank = Bank(name=bank_name)
    offer = Offer(
        shop=shop,
        bank=bank,
        offer_type=OfferTypeEnum.CASHBACK,
        description=f"10% off at {shop_name}",
        expiry_date=datetime.now() + timedelta(days=10),
    )

    db = MagicMock(spec=OfferDB)
    db.shop_name = shop.name
    db.to_domain.return_value = offer
    return db


def test_fuzzy_search_exact_match():
    mock_session = MagicMock()
    db_offers = [make_offer_db("Adidas"), make_offer_db("Starbucks")]
    mock_session.exec.return_value.all.return_value = db_offers

    service = OfferService(session=mock_session, threshold=75)
    results = service.fuzzy_search(["adidas"])

    assert len(results) == 1
    assert results[0].shop.name.lower() == "adidas"


def test_fuzzy_search_multiple_queries():
    mock_session = MagicMock()
    db_offers = [make_offer_db("Adidas"), make_offer_db("Starbucks"), make_offer_db("Adidaz")]
    mock_session.exec.return_value.all.return_value = db_offers

    service = OfferService(session=mock_session, threshold=70)
    results = service.fuzzy_search(["adidas", "starbucks"])

    shop_names = {offer.shop.name.lower() for offer in results}
    assert "adidas" in shop_names or "adidaz" in shop_names
    assert "starbucks" in shop_names


def test_fuzzy_search_no_matches():
    mock_session = MagicMock()
    db_offers = [make_offer_db("Nike"), make_offer_db("Puma")]
    mock_session.exec.return_value.all.return_value = db_offers

    service = OfferService(session=mock_session, threshold=90)
    results = service.fuzzy_search(["unknownshop"])

    assert results == []


def test_list_offers():
    mock_session = MagicMock()
    offer_db = make_offer_db("Adidas")
    mock_session.exec.return_value.all.return_value = [offer_db]

    service = OfferService(session=mock_session)
    offers = service.list_offers()

    assert len(offers) == 1
    assert offers[0].shop.name == "Adidas"


def test_list_offers_paginated():
    mock_session = MagicMock()
    offer_db = make_offer_db("Starbucks")
    mock_session.exec.return_value.all.return_value = [offer_db]

    service = OfferService(session=mock_session)
    offers = service.list_offers_paginated(limit=10, offset=0)

    assert len(offers) == 1
    assert offers[0].shop.name == "Starbucks"
