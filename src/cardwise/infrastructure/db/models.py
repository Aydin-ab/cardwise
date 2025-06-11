import logging
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from cardwise.domain.models.offer import OfferTypeEnum

logger = logging.getLogger(__name__)


class ShopDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str


class BankDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str


class OfferDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    shop_id: str = Field(foreign_key="shopdb.id")
    bank_id: str = Field(foreign_key="bankdb.id")
    offer_type: OfferTypeEnum
    description: str
    expiry_date: Optional[datetime] = None
