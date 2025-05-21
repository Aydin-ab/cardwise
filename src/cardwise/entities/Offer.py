from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, computed_field

from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Shop import Shop


class OfferTypeEnum(str, Enum):
    CASHBACK = "cashback"
    POINTS = "points"
    MISC = "misc"


class Offer(BaseModel):
    shop: Shop
    bank_info: BankInfo
    offer_type: OfferTypeEnum
    description: str
    expiry_date: Optional[datetime] = None

    @computed_field
    @property
    def id(self) -> str:
        """
        Deterministic identifier for this offer.
        """
        return f"{self.shop.id}|{self.bank_info.id}|{self.offer_type}|{self.description}"

    def is_expired(self, reference_time: Optional[datetime] = None) -> bool:
        if not self.expiry_date:
            return False
        return (reference_time or datetime.now()) > self.expiry_date

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Offer):
            return NotImplemented
        return self.id == other.id
