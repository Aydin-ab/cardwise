import logging
from typing import List, Set

from rapidfuzz import fuzz, process
from sqlmodel import Session, select

from cardwise.domain.models.offer import Offer
from cardwise.persistence.models.offer_db import OfferDB

logger = logging.getLogger(__name__)


class OfferService:
    def __init__(self, session: Session, threshold: int = 75):
        self.session = session
        self.threshold = threshold

    def list_offers(self) -> List[Offer]:
        logger.debug("Fetching all offers from DB.")
        offers = self.session.exec(select(OfferDB)).all()
        return [o.to_domain() for o in offers]

    def list_offers_paginated(self, limit: int = 20, offset: int = 0) -> List[Offer]:
        logger.debug(f"Fetching offers with limit={limit} and offset={offset}")
        stmt = select(OfferDB).offset(offset).limit(limit)
        offers = self.session.exec(stmt).all()
        return [o.to_domain() for o in offers]

    def fuzzy_search(self, shop_queries: List[str]) -> List[Offer]:
        logger.debug(f"Performing fuzzy search with queries: {shop_queries}")
        if not shop_queries:
            logger.warning("Fuzzy search received empty query list.")
            return []
        logger.debug("Fetching all offers from DB for fuzzy search.")
        db_offers = self.session.exec(select(OfferDB)).all()
        logger.debug(f"Total offers retrieved from DB: {len(db_offers)}")
        all_shop_names = {offer.shop_name for offer in db_offers}
        logger.debug(f"Unique shop names filtered: {len(all_shop_names)}")
        matched_names: Set[str] = set()
        for query in shop_queries:
            matches = process.extract(
                query.lower(),
                all_shop_names,
                scorer=fuzz.ratio,
                limit=None,
                score_cutoff=self.threshold,
            )
            logger.debug(f"Matches for '{query}': {[m[0] for m in matches]}")
            matched_names.update(match[0] for match in matches)

        filtered = [offer for offer in db_offers if offer.shop_name in matched_names]
        logger.debug(f"Fuzzy search yielded {len(filtered)} matching offers.")
        return [offer.to_domain() for offer in filtered]
