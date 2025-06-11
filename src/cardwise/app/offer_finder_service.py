import logging
from typing import List, Optional

from cardwise.app.data_loader import OfferDataLoader
from cardwise.domain.formatters.base_offer_formatter import OfferFormatter
from cardwise.domain.matchers.base_shopmatcher import ShopMatcher
from cardwise.domain.models.offer import Offer

logger = logging.getLogger(__name__)


class OfferMatcherWrapper:
    def __init__(self, matcher: ShopMatcher):
        self.matcher = matcher

    def match(self, offers: List[Offer], query: str) -> List[Offer]:
        logger.debug("Retrieving unique shops from offers...")
        unique_shops = list({offer.shop for offer in offers})
        logger.debug(f"Reduced the {len(offers)} offers to {len(unique_shops)} unique shops")
        matched_shops = self.matcher.match(query, unique_shops)
        matched_names = {shop.name for shop in matched_shops}
        logger.debug(f"Matched {len(matched_shops)} shop name(s) for query '{query}': {matched_names}")
        matched_offers = [offer for offer in offers if offer.shop.name in matched_names]
        logger.debug(f"Found {len(matched_offers)} offer(s) for shop(s) '{matched_names}': {matched_offers}")
        return matched_offers

    def __repr__(self):
        return f"{self.__class__.__name__}(matcher={self.matcher})"


class OfferFinderService:
    def __init__(
        self,
        data_loader: OfferDataLoader,
        shop_matcher: ShopMatcher,
        formatter: OfferFormatter,
    ):
        self.data_loader = data_loader
        self.matcher = OfferMatcherWrapper(shop_matcher)
        self.formatter = formatter
        self._cached_offers: Optional[List[Offer]] = None

    def _load_all_offers(self) -> List[Offer]:
        logger.info("Fetching all offers...")
        if self._cached_offers is None:
            logger.debug("No cached offers found. Loading from data loader...")
            self._cached_offers = self.data_loader.get_or_restore_offers()
            logger.debug(f"Cached {len(self._cached_offers)} offers.")
        return self._cached_offers

    def clear_offers_cache(self) -> None:
        logger.debug("Clearing cached offers...")
        self._cached_offers = None

    def precompute_offers(self) -> None:
        logger.debug("Precomputing cached offers...")
        self._load_all_offers()

    def _find_offers_queries(self, queries: List[str]) -> str:
        logger.info(f"Finding offers for queries: {queries}")
        offers = self._load_all_offers()
        all_matched: List[Offer] = []
        logger.debug(f"Loaded {len(offers)} offers for matching.")
        for query in queries:
            logger.debug(f"Matching offers for query: {query}")
            all_matched.extend(self.matcher.match(offers, query))
        logger.debug(f"Total matched offers for all {len(queries)} queri(es); {len(all_matched)} offers: {all_matched}")
        return self.formatter.format(all_matched)

    def find_offers(self, query_or_queries: str | List[str]) -> str:
        queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries
        return self._find_offers_queries(queries)

    def __repr__(self):
        repr_ = (
            f"{self.__class__.__name__}(data_loader={self.data_loader}, "
            "matcher={self.matcher}, "
            "formatter={self.formatter}), "
            f"cached_offers size: {len(self._cached_offers) if self._cached_offers else 'None'}"
        )
        return repr_
