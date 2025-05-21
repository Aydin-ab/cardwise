from pathlib import Path
from typing import List, Optional

from cardwise.entities.Offer import Offer
from cardwise.formatters.base import OfferFormatter
from cardwise.matchers.base import ShopMatcher
from cardwise.parsers.base import BankOfferParser
from cardwise.services.offer_db_service import OfferDBService


class OfferMatcherService:
    def __init__(self, matcher: ShopMatcher):
        self.matcher = matcher

    def match(self, offers: List[Offer], query: str) -> List[Offer]:
        unique_shops = list({offer.shop for offer in offers})
        matched_shops = self.matcher.match(query, unique_shops)
        matched_names = {shop.name for shop in matched_shops}
        return [offer for offer in offers if offer.shop.name in matched_names]


class OfferRepository:
    def __init__(self, parsers: List[BankOfferParser], html_dir: Path):
        self.parsers = parsers
        self.html_dir = html_dir
        self.db_service = OfferDBService()

    def _get_default_path(self, parser: BankOfferParser) -> Path:
        return self.html_dir / f"{parser.bank_info.id}_offers.html"

    def _load_offers_from_parser(self, parser: BankOfferParser) -> List[Offer]:
        html_path = self._get_default_path(parser)
        return parser.parse(html_path) if html_path.exists() else []

    def _load_from_parsers(self) -> List[Offer]:
        offers: List[Offer] = []
        for parser in self.parsers:
            offers.extend(self._load_offers_from_parser(parser))
        return offers

    def get_all_offers(self) -> List[Offer]:
        offers = self.db_service.load_all_offers()
        if offers:
            return offers

        # fallback to HTML and persist
        offers = self._load_from_parsers()
        self.db_service.save_offers(offers)
        return offers


class OfferFinderService:
    def __init__(
        self,
        parsers: List[BankOfferParser],
        matcher: ShopMatcher,
        formatter: OfferFormatter,
        html_dir: Path,
    ):
        self.repository = OfferRepository(parsers, html_dir)
        self.matcher = OfferMatcherService(matcher)
        self.formatter = formatter
        self._cached_offers: Optional[List[Offer]] = None

    def _load_all_offers(self) -> List[Offer]:
        if self._cached_offers is None:
            self._cached_offers = self.repository.get_all_offers()
        return self._cached_offers

    def clear_offers_cache(self) -> None:
        self._cached_offers = None

    def precompute_offers(self) -> None:
        self._load_all_offers()

    def _find_offers_queries(self, queries: List[str]) -> str:
        offers = self._load_all_offers()
        all_matched: List[Offer] = []
        for query in queries:
            all_matched.extend(self.matcher.match(offers, query))
        return self.formatter.format(all_matched)

    def find_offers(self, query_or_queries: str | List[str]) -> str:
        queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries
        return self._find_offers_queries(queries)
