import re
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop
from cardwise.exceptions import (
    OfferDescriptionParsingError,
    OfferParsingError,
    OfferShopNameParsingError,
)
from cardwise.parsers.base import BankOfferParser


class CapitalOneOfferParser(BankOfferParser):
    def __init__(self):
        super().__init__(bank_name="Capital One", parser_id="capital_one")

    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        results: set[Offer] = set()

        tiles = [
            tag
            for tag in soup.find_all(
                "div", class_="standard-tile relative flex flex-col justify-between w-full h-full mt-0"
            )
            if isinstance(tag, Tag)
        ]

        if not tiles:
            raise OfferParsingError(self.bank.name, "No tile elements found")

        for tile in tiles:
            img_tag = tile.find("img")
            if not isinstance(img_tag, Tag) or not img_tag.has_attr("src"):
                raise OfferShopNameParsingError(self.bank.name, "Missing 'src' in image tag, no URL to get shop name")
            src_attr = img_tag["src"]
            src_url = src_attr[0] if isinstance(src_attr, list) else str(src_attr)
            match: Optional[re.Match[str]] = re.search(r"domain=([^.]+)\.", src_url)
            if not match:
                raise OfferShopNameParsingError(self.bank.name, f"""Not in expected position at URL: {src_url}""")
            shop_name = match.group(1).strip()

            offer_divs = [div for div in tile.find_all("div") if isinstance(div, Tag)]
            if len(offer_divs) < 2:
                raise OfferDescriptionParsingError(
                    self.bank.name,
                    f"""Expected >2 divs with description at index 1
                                                            Found: {len(offer_divs)} divs: {offer_divs}""",
                )
            offer_description = offer_divs[1].get_text(strip=True)
            if not offer_description:
                raise OfferDescriptionParsingError(self.bank.name, f"""Missing text in div tag. Div: {offer_divs[1]}""")

            results.add(
                Offer(
                    shop=Shop(name=shop_name),
                    bank_info=self.bank,
                    offer_type="points",  # Now normalized with "miles" as "points"
                    description=offer_description,
                )
            )

        return list(results)
