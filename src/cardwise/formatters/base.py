from abc import ABC, abstractmethod
from typing import List

from cardwise.entities.Offer import Offer


class OfferFormatter(ABC):
    @abstractmethod
    def format(self, offers: List[Offer]) -> str:
        """
        Takes a list of offers and returns a formatted string (e.g., JSON, CLI).
        """
        pass
