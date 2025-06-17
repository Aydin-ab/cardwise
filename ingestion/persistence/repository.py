import logging
from typing import List

from sqlmodel import Session, delete

from cardwise.domain.models.offer import Offer
from cardwise.persistence.models.offer_db import OfferDB

logger = logging.getLogger(__name__)


class OfferRepository:
    def __init__(self, session: Session):
        self.session = session

    def delete_all(self) -> None:
        """
        Delete all existing offers in the database.
        """
        logger.info("Deleting all existing offers from the database...")
        self.session.exec(delete(OfferDB))  # type: ignore
        self.session.commit()
        logger.info("All offers deleted.")

    def insert_many(self, offers: List[Offer]) -> None:
        """
        Insert a batch of offers into the database.
        """
        if not offers:
            logger.info("No offers to insert.")
            return

        logger.info(f"Inserting {len(offers)} offer(s) into the database...")
        for offer in offers:
            self.session.add(OfferDB.from_domain(offer))
        self.session.commit()
        logger.info("Insert complete.")
