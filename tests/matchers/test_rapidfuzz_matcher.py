from typing import List

import pytest

from cardwise.domain.matchers.rapidfuzz_shopmatcher import RapidFuzzShopMatcher
from cardwise.domain.models.shop import Shop


@pytest.fixture
def known_shops():
    return [
        Shop(name="Walmart"),
        Shop(name="Target"),
        Shop(name="Best Buy"),
        Shop(name="Amazon"),
        Shop(name="Starbucks"),
        Shop(name="Starbuck's"),
        Shop(name="Starbuck"),
    ]


@pytest.fixture
def matcher():
    return RapidFuzzShopMatcher(threshold=80)


def test_match_single_exact_match(known_shops: List[Shop], matcher: RapidFuzzShopMatcher):
    result = matcher.match("Walmart", known_shops)
    assert len(result) == 1
    assert result[0].name == "Walmart"


def test_match_single_fuzzy_match(known_shops: List[Shop], matcher: RapidFuzzShopMatcher):
    result = matcher.match("Wallmart", known_shops)
    assert len(result) == 1
    assert result[0].name == "Walmart"


def test_match_multiple_similar_matches(known_shops: List[Shop], matcher: RapidFuzzShopMatcher):
    result = matcher.match("Starbuk", known_shops)
    assert len(result) == 3
    matched_names = {shop.name for shop in result}
    assert matched_names == {"Starbucks", "Starbuck's", "Starbuck"}


def test_match_no_matches(known_shops: List[Shop], matcher: RapidFuzzShopMatcher):
    result = matcher.match("NonExistentShop", known_shops)
    assert len(result) == 0


def test_match_empty_input(known_shops: List[Shop], matcher: RapidFuzzShopMatcher):
    result = matcher.match("", known_shops)
    assert len(result) == 0
