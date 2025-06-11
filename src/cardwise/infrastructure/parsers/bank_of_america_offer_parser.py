import logging
from typing import List

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


class BankOfAmericaOfferParser(BankOfferParser):
    def __init__(self):
        super().__init__(bank_name="Bank of America", offer_type=OfferTypeEnum.CASHBACK)

    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        results: set[Offer] = set()

        deal_wrappers = [tag for tag in soup.find_all("div", class_="deal-logo-wrapper top") if isinstance(tag, Tag)]
        if not deal_wrappers:
            logger.exception(f"No offer wrappers found for {self.bank.name}.")
            raise OfferParsingError(self.bank.name, "No offer wrappers found")

        logger.debug(f"Bank of America HTML: Found {len(deal_wrappers)} relevant deal wrappers")
        logger.debug("Starting Parsing...")
        for wrapper in deal_wrappers:
            img_tag = wrapper.find("img")
            span_tag = wrapper.find("span", class_="deal-offer-percent")

            if not isinstance(img_tag, Tag) or not img_tag.has_attr("alt"):
                logger.error(f"Missing 'alt' attribute in img tag for {self.bank.name}.")
                raise OfferShopNameParsingError(
                    self.bank.name,
                    f"""Missing 'alt' in img tag. Found img tag: {img_tag}""",
                )
            shop_name = str(img_tag["alt"]).replace(" Logo", "").strip()
            logger.debug(f"Shop name found: {shop_name}")

            if not isinstance(span_tag, Tag):
                logger.error(f"Span tag not found for {self.bank.name}.")
                raise OfferDescriptionParsingError(
                    self.bank.name,
                    f"""Span found is not a tag. Found: {span_tag}""",
                )
            offer_description = span_tag.get_text(strip=True)
            logger.debug(f"Offer description found: {offer_description}")
            if not offer_description:
                logger.error(f"Missing text in span tag for {self.bank.name}.")
                raise OfferDescriptionParsingError(
                    self.bank.name,
                    f"""Missing text in span tag. Span: {span_tag}""",
                )
            offer = Offer(
                shop=Shop(name=shop_name),
                bank=self.bank,
                offer_type=self.offer_type,
                description=offer_description,
            )
            logger.debug(f"Parsed offer {offer}")
            results.add(offer)

        logger.debug(f"Parsing over. Found {len(results)} offers.")
        return list(results)

    def __repr__(self):
        return f"{self.__class__.__name__}(bank_name={self.bank.name}, offer_type={self.offer_type})"
