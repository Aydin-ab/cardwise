from typing import Optional

from pydantic import BaseModel, computed_field


class BankInfo(BaseModel):
    name: str  # Display name
    website: Optional[str] = None

    @computed_field
    @property
    def id(self) -> str:
        """
        Deterministic unique ID for the BankInfo.
        """
        # keep only alphanumeric characters
        id = "".join([c.lower() for c in self.name if c.isalnum() or c == " "])
        # remove spaces
        id = id.strip().replace(" ", "_")
        return id

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankInfo):
            return NotImplemented
        return self.id == other.id
