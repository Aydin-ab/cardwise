import json
import logging
from typing import List

from cardwise.domain.formatters.base_offer_formatter import OfferFormatter
from cardwise.domain.models.offer import Offer

logger = logging.getLogger(__name__)


class JSONOfferFormatter(OfferFormatter):
    def format(self, offers: List[Offer]) -> str:
        logger.debug(f"Formatting {len(offers)} offers for JSON output.")
        json_dump = json.dumps([offer.model_dump(mode="json") for offer in offers], indent=2)
        logger.debug(f"Formatted JSON: {json_dump}")
        return json_dump

    def __repr__(self):
        return f"{self.__class__.__name__}()"
