from typing import Optional

from cardwise.db.models import BankInfoDB, OfferDB, ShopDB
from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop


def offer_to_db(offer: Offer) -> tuple[OfferDB, ShopDB, BankInfoDB]:
    shop = offer.shop
    bank_info = offer.bank_info
    return (
        OfferDB(
            id=offer.id,
            shop_id=shop.id,
            bank_info_id=bank_info.id,
            offer_type=offer.offer_type,
            description=offer.description,
            expiry_date=offer.expiry_date,
        ),
        ShopDB(id=shop.id, name=shop.name, category=shop.category),
        BankInfoDB(id=bank_info.id, name=bank_info.name, website=bank_info.website),
    )


def db_to_offer(offer_db: OfferDB, shop: Optional[ShopDB], bankInfo: Optional[BankInfoDB]) -> Offer:
    if shop is None:
        raise ValueError("Shop not found in the database.")
    if bankInfo is None:
        raise ValueError("BankInfo not found in the database.")
    return Offer(
        shop=Shop(name=shop.name, category=shop.category),
        bank_info=BankInfo(name=bankInfo.name, website=bankInfo.website),
        offer_type=offer_db.offer_type,
        description=offer_db.description,
        expiry_date=offer_db.expiry_date,
    )
