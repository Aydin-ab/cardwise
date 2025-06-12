import logging
from typing import List

from sqlmodel import select

from cardwise.domain.models.offer import Offer
from cardwise.infrastructure.db.mapper import db_to_offer, offer_to_db
from cardwise.infrastructure.db.models import BankDB, OfferDB, ShopDB
from cardwise.infrastructure.db.repositories.base_offer_repository import OfferRepository
from cardwise.infrastructure.db.session import drop_db, get_session, init_db

logger = logging.getLogger(__name__)


class SQLModelOfferRepository(OfferRepository):
    def get_all(self) -> List[Offer]:
        with get_session() as session:
            logger.debug("Fetching all offers from the database...")
            offer_dbs = session.exec(select(OfferDB)).all()
            offers: List[Offer] = []
            for offer_db in offer_dbs:
                logger.debug(f"Converting OfferDB: {offer_db}")
                offer = db_to_offer(
                    offer_db,
                    session.get(ShopDB, offer_db.shop_id),
                    session.get(BankDB, offer_db.bank_id),
                )
                offers.append(offer)
            logger.debug(f"Total OfferDBs converted to offers: {len(offers)}")
            return offers

    def save_all(self, offers: List[Offer]) -> None:
        with get_session() as session:
            logger.debug("Saving offers to the database...")
            for offer in offers:
                logger.debug(f"Converting offer: {offer}")
                offer_db, shop_db, bank_db = offer_to_db(offer)
                if not session.get(ShopDB, shop_db.id):
                    logger.debug(f"Adding new ShopDB: {shop_db}")
                    session.add(shop_db)
                if not session.get(BankDB, bank_db.id):
                    logger.debug(f"Adding new BankDB: {bank_db}")
                    session.add(bank_db)
                logger.debug(f"Adding OfferDB: {offer_db}")
                session.add(offer_db)
            logger.debug("Committing session...")
            session.commit()
            logger.debug(f"Total offers saved: {len(offers)}")

    def refresh(self) -> None:
        drop_db()
        init_db()

    def __repr__(self):
        return f"{self.__class__.__name__}()"
