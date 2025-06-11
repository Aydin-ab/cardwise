from abc import ABC, abstractmethod
from typing import List

from cardwise.domain.models.shop import Shop


class ShopMatcher(ABC):
    @abstractmethod
    def match(self, query: str, known_shops: List[Shop]) -> List[Shop]:
        """Match a single user input to one or more Shop objects."""
        pass
