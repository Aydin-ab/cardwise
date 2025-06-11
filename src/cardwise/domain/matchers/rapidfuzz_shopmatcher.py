import logging
from typing import List

from rapidfuzz import fuzz, process

from cardwise.domain.matchers.base_shopmatcher import ShopMatcher
from cardwise.domain.models.shop import Shop

logger = logging.getLogger(__name__)


class RapidFuzzShopMatcher(ShopMatcher):
    def __init__(self, threshold: int = 80):
        self.threshold = threshold

    def match(self, query: str, known_shops: List[Shop]) -> List[Shop]:
        """
        Matches a single user input to known shops using fuzzy matching.

        Args:
            raw_input: A single shop name input by the user.
            known_shops: List of Shop objects known to the system.

        Returns:
            List of matched Shop objects (above threshold).
        """
        shop_name_to_shop = {shop.name.lower(): shop for shop in known_shops}
        all_names = list(shop_name_to_shop.keys())

        logger.debug(f"Matching query {query} ...")
        matches = process.extract(query.lower(), all_names, scorer=fuzz.ratio, limit=None, score_cutoff=self.threshold)
        logger.debug(f"Found {len(matches)} matche(s) : (name, score, index)= {matches}")
        names = [name for name, _, _ in matches]

        return [shop_name_to_shop[name] for name in names]

    def __repr__(self):
        return f"{self.__class__.__name__}(threshold={self.threshold})"
