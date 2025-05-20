from typing import List

from pydantic import BaseModel

from cardwise.entities.BankInfo import BankInfo
from cardwise.entities.Offer import Offer


class Bank(BaseModel):
    metadata: BankInfo
    offers: List[Offer] = []

    def add_offer(self, offer: Offer) -> None:
        self.offers.append(offer)

    def add_batch_offers(self, offers: List[Offer]) -> None:
        for offer in offers:
            self.add_offer(offer)
