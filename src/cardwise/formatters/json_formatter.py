import json
from typing import List

from cardwise.entities.Offer import Offer
from cardwise.formatters.base import OfferFormatter


class JSONFormatter(OfferFormatter):
    def format(self, offers: List[Offer]) -> str:
        return json.dumps([offer.model_dump(mode="json") for offer in offers], indent=2)
