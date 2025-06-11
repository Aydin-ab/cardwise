import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.shared.exceptions import OfferSourceNotFound

logger = logging.getLogger(__name__)


class BankOfferParser(ABC):
    """
    Base class for all bank offer parsers.
    Provides HTML loading and parsing boilerplate.
    """

    def __init__(self, bank_name: str, offer_type: OfferTypeEnum):
        self.bank = Bank(name=bank_name)
        self.offer_type = offer_type

    def parse(self, html_path: Path) -> List[Offer]:
        if not html_path.exists():
            logger.error(f"HTML file not found: {html_path}")
            raise OfferSourceNotFound(self.bank.name, str(html_path))

        logger.debug(f"Parsing HTML file: {html_path}")
        with open(html_path, "r", encoding="utf-8") as f:
            html_doc = f.read()
        logger.debug("Calling BeautifulSoup...")
        soup = BeautifulSoup(html_doc, "html.parser")
        return self._extract_offers(soup)

    @abstractmethod
    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Subclasses implement this to extract offers from soup."""
        pass
