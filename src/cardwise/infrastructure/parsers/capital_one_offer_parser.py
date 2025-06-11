import logging
import re
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop
from cardwise.infrastructure.parsers.base_offer_parser import BankOfferParser
from cardwise.shared.exceptions import (
    OfferDescriptionParsingError,
    OfferParsingError,
    OfferShopNameParsingError,
)

logger = logging.getLogger(__name__)


class CapitalOneOfferParser(BankOfferParser):
    def __init__(self):
        super().__init__(bank_name="Capital One", offer_type=OfferTypeEnum.POINTS)

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
            logger.warning("No tiles found in the HTML document.")
            raise OfferParsingError(self.bank.name, "No tile elements found")
        logger.debug(f"Capital One HTML: Found {len(tiles)} relevant tiles")
        logger.debug("Starting Parsing...")
        for tile in tiles:
            img_tag = tile.find("img")
            if not isinstance(img_tag, Tag) or not img_tag.has_attr("src"):
                logger.warning("Missing 'src' attribute in image tag.")
                raise OfferShopNameParsingError(self.bank.name, "Missing 'src' in image tag, no URL to get shop name")
            src_attr = img_tag["src"]
            src_url = src_attr[0] if isinstance(src_attr, list) else str(src_attr)
            match: Optional[re.Match[str]] = re.search(r"domain=([^.]+)\.", src_url)
            if not match:
                logger.warning("Shop name not found in URL.")
                raise OfferShopNameParsingError(self.bank.name, f"""Not in expected position at URL: {src_url}""")
            shop_name = match.group(1).strip()
            logger.debug(f"Shop name found: {shop_name}")

            offer_divs = [div for div in tile.find_all("div") if isinstance(div, Tag)]
            if len(offer_divs) < 2:
                logger.warning(
                    f"Expected >2 divs with description at index 1. Found: {len(offer_divs)} divs: {offer_divs}"
                )
                raise OfferDescriptionParsingError(
                    self.bank.name,
                    f"""Expected >2 divs with description at index 1. Found: {len(offer_divs)} divs: {offer_divs}""",
                )
            offer_description = offer_divs[1].get_text(strip=True)
            logger.debug(f"Offer description found: {offer_description}")
            if not offer_description:
                logger.warning(f"Missing text in div tag. Div: {offer_divs[1]}")
                raise OfferDescriptionParsingError(self.bank.name, f"""Missing text in div tag. Div: {offer_divs[1]}""")

            offer = Offer(
                shop=Shop(name=shop_name),
                bank=self.bank,
                offer_type=self.offer_type,
                description=offer_description,
            )
            logger.debug(f"Parsed offer: {offer}")
            results.add(offer)

        logger.debug(f"Parsing over. Found {len(results)} offers.")
        return list(results)

    def __repr__(self):
        return f"{self.__class__.__name__}(bank_name={self.bank.name}, offer_type={self.offer_type})"
