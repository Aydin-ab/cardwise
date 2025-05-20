from typing import List

from rapidfuzz import fuzz, process

from cardwise.entities.Shop import Shop
from cardwise.matchers.base import ShopMatcher


class RapidFuzzMatcher(ShopMatcher):
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

        matches = process.extract(query.lower(), all_names, scorer=fuzz.ratio, limit=None, score_cutoff=self.threshold)
        names = [name for name, _, _ in matches]

        return [shop_name_to_shop[name] for name in names]
