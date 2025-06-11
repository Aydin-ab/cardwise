import logging
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, computed_field

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.shop import Shop

logger = logging.getLogger(__name__)


class OfferTypeEnum(str, Enum):
    CASHBACK = "cashback"
    POINTS = "points"
    MISC = "misc"


class Offer(BaseModel):
    shop: Shop
    bank: Bank
    offer_type: OfferTypeEnum
    description: str
    expiry_date: Optional[datetime] = None

    @computed_field
    @property
    def id(self) -> str:
        """
        Deterministic identifier for this offer.
        """
        return f"{self.shop.id}|{self.bank.id}|{self.offer_type}|{self.description}"

    def is_expired(self, reference_time: Optional[datetime] = None) -> bool:
        if not self.expiry_date:
            logger.debug("No expiry date found, offer is not expired.")
            return False
        is_expired = (reference_time or datetime.now()) > self.expiry_date
        logger.debug(f"Offer expired: {is_expired} (expiry date: {self.expiry_date})")
        return is_expired

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Offer):
            return NotImplemented
        return self.id == other.id
