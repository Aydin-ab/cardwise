from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from cardwise.entities.Offer import OfferTypeEnum


class ShopDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    category: Optional[str] = None


class BankInfoDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    website: Optional[str] = None


class OfferDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    shop_id: str = Field(foreign_key="shopdb.id")
    bank_info_id: str = Field(foreign_key="bankinfodb.id")
    offer_type: OfferTypeEnum
    description: str
    expiry_date: Optional[datetime] = None
