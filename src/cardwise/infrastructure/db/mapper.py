import logging
from typing import Optional

from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer
from cardwise.domain.models.shop import Shop
from cardwise.infrastructure.db.models import BankDB, OfferDB, ShopDB

logger = logging.getLogger(__name__)


def offer_to_db(offer: Offer) -> tuple[OfferDB, ShopDB, BankDB]:
    shop = offer.shop
    bank = offer.bank
    offerDB = OfferDB(
        id=offer.id,
        shop_id=shop.id,
        bank_id=bank.id,
        offer_type=offer.offer_type,
        description=offer.description,
        expiry_date=offer.expiry_date,
    )
    logger.debug(f"Built offerDB: {offerDB}")
    shopDB = ShopDB(id=shop.id, name=shop.name)
    logger.debug(f"Built shopDB: {shopDB}")
    bankDB = BankDB(id=bank.id, name=bank.name)
    logger.debug(f"Built bankDB: {bankDB}")
    return (offerDB, shopDB, bankDB)


def db_to_offer(offer_db: OfferDB, shop: Optional[ShopDB], bank: Optional[BankDB]) -> Offer:
    if shop is None:
        logger.error(f"Shop not found in the database for offer: {offer_db}")
        raise ValueError("Shop not found in the database.")
    shop_ = Shop(name=shop.name)
    if bank is None:
        logger.error(f"BankInfo not found in the database for offer: {offer_db}")
        raise ValueError("BankInfo not found in the database.")
    bank_ = Bank(name=bank.name)
    offer = Offer(
        shop=shop_,
        bank=bank_,
        offer_type=offer_db.offer_type,
        description=offer_db.description,
        expiry_date=offer_db.expiry_date,
    )
    logger.debug(f"Converted to Offer: {offer}")
    return offer
