from typing import List

from sqlmodel import SQLModel, select

from cardwise.db.models import BankInfoDB, OfferDB, ShopDB
from cardwise.db.session import engine, get_session
from cardwise.db.utils import db_to_offer, offer_to_db
from cardwise.entities.Offer import Offer


class OfferDBService:
    def load_all_offers(self) -> List[Offer]:
        with get_session() as session:
            offer_dbs = session.exec(select(OfferDB)).all()
            return [
                db_to_offer(
                    o,
                    session.get(ShopDB, o.shop_id),
                    session.get(BankInfoDB, o.bank_info_id),
                )
                for o in offer_dbs
            ]

    def save_offers(self, offers: List[Offer]) -> None:
        with get_session() as session:
            for offer in offers:
                offer_db, shop_db, bank_info_db = offer_to_db(offer)

                # Insert shop if not exists
                if not session.get(ShopDB, shop_db.id):
                    session.add(shop_db)
                if not session.get(BankInfoDB, bank_info_db.id):
                    session.add(bank_info_db)
                session.add(offer_db)

            session.commit()

    def refresh(self) -> None:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
