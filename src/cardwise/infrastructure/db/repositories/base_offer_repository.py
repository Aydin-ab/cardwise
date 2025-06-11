from abc import ABC, abstractmethod
from typing import List

from cardwise.domain.models.offer import Offer


class AbstractOfferRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Offer]: ...

    @abstractmethod
    def save_all(self, offers: List[Offer]) -> None: ...

    @abstractmethod
    def refresh(self) -> None: ...
