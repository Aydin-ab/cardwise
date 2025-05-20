from typing import Optional

from pydantic import BaseModel, computed_field


class Shop(BaseModel):
    name: str  # Canonical name
    category: Optional[str] = None

    @computed_field
    @property
    def id(self) -> str:
        """
        Deterministic unique ID for the shop.
        """
        return self.name.lower().strip().replace(" ", "_")

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Shop):
            return NotImplemented
        return self.id == other.id
