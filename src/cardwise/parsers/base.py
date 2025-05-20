from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Offer import Offer
from cardwise.exceptions import OfferSourceNotFound


class BankOfferParser(ABC):
    """
    Base class for all bank offer parsers.
    Provides HTML loading and parsing boilerplate.
    """

    def __init__(self, bank_name: str, parser_id: str):
        self.bank = BankInfo(name=bank_name, bank_id=parser_id)

    def parse(self, html_path: Path) -> List[Offer]:
        if not html_path.exists():
            raise OfferSourceNotFound(self.bank.name, str(html_path))

        with open(html_path, "r", encoding="utf-8") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        return self._extract_offers(soup)

    @abstractmethod
    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Subclasses implement this to extract offers from soup."""
        pass
