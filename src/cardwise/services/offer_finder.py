from pathlib import Path
from typing import List, Optional

from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop
from cardwise.formatters.base import OfferFormatter
from cardwise.matchers.base import ShopMatcher
from cardwise.parsers.base import BankOfferParser


class OfferFinderService:
    def __init__(
        self,
        parsers: List[BankOfferParser],
        matcher: ShopMatcher,
        formatter: OfferFormatter,
        html_dir: Path,
    ):
        self.parsers = parsers
        self.matcher = matcher
        self.formatter = formatter
        self.html_dir = html_dir
        self._cached_offers: Optional[List[Offer]] = None

    def _get_default_path_from_parser(self, parser: BankOfferParser) -> Path:
        """
        Returns the default path for the given parser.
        """
        bank_id = parser.bank.bank_id
        return self.html_dir / f"{bank_id}_offers.html"

    def _load_offers_from_parser(self, parser: BankOfferParser) -> List[Offer]:
        """
        Loads offers from a specific parser and returns them.
        """
        html_path = self._get_default_path_from_parser(parser)
        if not html_path.exists():
            return []
        return parser.parse(html_path)

    def _load_all_offers(self) -> List[Offer]:
        if self._cached_offers is not None:
            return self._cached_offers

        offers: List[Offer] = []

        for parser in self.parsers:
            parsed_offers = self._load_offers_from_parser(parser)
            offers.extend(parsed_offers)

        self._cached_offers = offers
        return offers

    def clear_offers_cache(self) -> None:
        """
        Clears the cached offers. Useful for refreshing after HTML updates.
        """
        self._cached_offers = None

    def precompute_offers(self) -> None:
        """
        Precomputes the offers for faster access later.
        """
        self._load_all_offers()

    def _get_matching_offers(self, query: str) -> List[Offer]:
        """
        Matches the query against known shops and filters offers accordingly.
        """
        offers = self._load_all_offers()
        unique_shops_byID: List[Shop] = list({offer.shop for offer in offers})
        matched_shops = self.matcher.match(query, unique_shops_byID)
        matched_names = {shop.name for shop in matched_shops}

        return [offer for offer in offers if offer.shop.name in matched_names]

    def _find_offers_single_query(self, query: str) -> str:
        matched_offers = self._get_matching_offers(query)
        return self.formatter.format(matched_offers)

    def _find_offers_batch_query(self, queries: List[str]) -> str:
        all_matched_offers: List[Offer] = []
        for query in queries:
            matched = self._get_matching_offers(query)
            all_matched_offers.extend(matched)
        return self.formatter.format(all_matched_offers)

    def find_offers(self, query_or_queries: str | List[str]) -> str:
        """
        Public interface to get formatted offers from either a single query or a list of queries.
        """
        if isinstance(query_or_queries, str):
            offers = self._find_offers_single_query(query_or_queries)
        else:
            offers = self._find_offers_batch_query(query_or_queries)
        return offers
