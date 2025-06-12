from cardwise.domain.matchers.base_shopmatcher import ShopMatcher
from cardwise.domain.matchers.rapidfuzz_shopmatcher import RapidFuzzShopMatcher


def get_shop_matcher() -> ShopMatcher:
    """
    Returns the appropriate matcher based on the input parameter.
    For now, only RapidFuzzShopMatcher is supported.
    So it will always return an instance of RapidFuzzShopMatcher.

    Returns:
        ShopMatcher: An instance of RapidFuzzShopMatcher.
    """
    return RapidFuzzShopMatcher()
