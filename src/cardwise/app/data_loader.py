import logging
from pathlib import Path
from typing import List, Optional

from cardwise.domain.models.offer import Offer
from cardwise.infrastructure.db.repositories.base_offer_repository import OfferRepository
from cardwise.infrastructure.db.repositories.SQLModel_offer_repository import SQLModelOfferRepository
from cardwise.infrastructure.parsers.base_offer_parser import BankOfferParser

logger = logging.getLogger(__name__)


class OfferDataLoader:
    def __init__(
        self,
        parsers: List[BankOfferParser],
        html_dir: Path,
        repository: Optional[OfferRepository] = None,
    ):
        self.parsers = parsers
        self.html_dir = html_dir
        self.repository = repository or SQLModelOfferRepository()

    def _get_default_path(self, parser: BankOfferParser) -> Path:
        default_path = self.html_dir / f"{parser.bank.id}_offers.html"
        logger.debug(f"Default path for parser {parser.bank.id}: {default_path}")
        return default_path

    def _load_offers_from_parser(self, parser: BankOfferParser) -> List[Offer]:
        html_path = self._get_default_path(parser)
        if not html_path.exists():
            logger.warning(f"HTML file not found for {parser.bank.name}: {html_path}")
            return []
        logger.debug(f"Calling parser for {parser.bank.name} with HTML path: {html_path}")
        return parser.parse(html_path)

    def _load_from_parsers(self) -> List[Offer]:
        offers: List[Offer] = []
        logger.debug("Loading offers from parsers...")
        for parser in self.parsers:
            offers.extend(self._load_offers_from_parser(parser))
        logger.debug(f"Total offers loaded from parsers: {len(offers)}")
        return offers

    def get_or_restore_offers(self) -> List[Offer]:
        offers = self.repository.get_all()
        if not offers:
            logger.debug("No offers found in the repository. Loading from parsers...")
            offers = self._load_from_parsers()
            logger.debug(f"Total offers loaded from parsers: {len(offers)}. Saving to repository...")
            self.repository.save_all(offers)
        return offers

    def refresh_offers_from_html(self) -> List[Offer]:
        offers = self._load_from_parsers()
        logger.debug(f"Total offers loaded from HTML files: {len(offers)}.")
        logger.debug("Refreshing repository...")
        self.repository.refresh()
        logger.debug("Repository refreshed.")
        logger.debug("Saving offers to repository...")
        self.repository.save_all(offers)
        logger.debug("Offers saved to repository.")
        return offers

    def __repr__(self):
        repr_ = (
            f"{self.__class__.__name__}(parsers={self.parsers}, "
            "html_dir={self.html_dir}, "
            "repository={self.repository})"
        )
        return repr_
