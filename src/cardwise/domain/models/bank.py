import logging

from pydantic import BaseModel, computed_field

import cardwise.domain.models.utils as utils

logger = logging.getLogger(__name__)


class Bank(BaseModel):
    name: str  # Display name

    @computed_field
    @property
    def id(self) -> str:
        """
        Deterministic unique ID for the BankInfo.
        """
        return utils.normalize_string(self.name)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bank):
            return NotImplemented
        return self.id == other.id
