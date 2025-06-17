import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from bs4 import BeautifulSoup

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum

logger = logging.getLogger(__name__)


class BankOfferParser(ABC):
    """
    Base class for all bank offer parsers.
    Provides HTML loading and parsing boilerplate.
    """

    def __init__(self, bank_name: Optional[str] = None, offer_type: Optional[OfferTypeEnum] = None):
        if not bank_name:
            logger.error("Bank name must be provided for the parser.")
            raise ValueError("Bank name must be provided for the parser.")
        if not offer_type:
            logger.error("Offer type must be provided for the parser.")
            raise ValueError("Offer type must be provided for the parser.")
        self.bank = Bank(name=bank_name)
        self.offer_type = offer_type

    def parse(self, html_doc: str) -> List[Offer]:
        logger.debug("Calling BeautifulSoup...")
        soup = BeautifulSoup(html_doc, "html.parser")
        return self._extract_offers(soup)

    @abstractmethod
    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Subclasses implement this to extract offers from soup."""
        pass
