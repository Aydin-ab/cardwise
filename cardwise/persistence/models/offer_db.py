from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop


class OfferDB(SQLModel, table=True):
    """
    DB representation of an Offer.
    """

    id: str = Field(primary_key=True)
    shop_name: str
    bank_name: str
    offer_type: OfferTypeEnum
    description: str
    expiry_date: Optional[datetime] = None

    @classmethod
    def from_domain(cls, offer: Offer) -> "OfferDB":
        """
        Convert a domain Offer to a DB OfferDB.
        """
        return cls(
            id=offer.id,
            shop_name=offer.shop.name,
            bank_name=offer.bank.name,
            offer_type=offer.offer_type,
            description=offer.description,
            expiry_date=offer.expiry_date,
        )

    def to_domain(self) -> Offer:
        """
        Convert a DB object to the domain model.
        """
        return Offer(
            shop=Shop(name=self.shop_name),
            bank=Bank(name=self.bank_name),
            offer_type=self.offer_type,
            description=self.description,
            expiry_date=self.expiry_date,
        )
