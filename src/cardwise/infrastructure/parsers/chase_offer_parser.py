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


class ChaseOfferParser(BankOfferParser):
    def __init__(self):
        super().__init__(bank_name="Chase", offer_type=OfferTypeEnum.CASHBACK)

    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        results: set[Offer] = set()
        divs = [tag for tag in soup.find_all("div", class_="r9jbije r9jbijl") if isinstance(tag, Tag)]
        if not divs:
            logger.error(f"No divs found for {self.bank.name}.")
            raise OfferParsingError(self.bank.name, "No valid divs found")
        logger.debug(f"Chase HTML: Found {len(divs)} relevant divs")
        logger.debug("Starting Parsing...")
        for div in divs:
            spans = [span for span in div.find_all("span") if isinstance(span, Tag)]
            if len(spans) < 2:
                logger.error(
                    f"""Offer data is incomplete: need at least 2 spans
                                        for shop name (index 0) and description (index 1).
                                        Found: {len(spans)} spans with spans: {spans}"""
                )
                raise OfferParsingError(
                    self.bank.name,
                    f"""Offer data is incomplete: need at least 2 spans
                                        for shop name (index 0) and description (index 1).
                                        Found: {len(spans)} spans with spans: {spans}""",
                )

            shop_name = spans[0].get_text(strip=True)
            logger.debug(f"Shop name found: {shop_name}")
            if not shop_name:
                logger.error(f"Missing text in span tag for {self.bank.name}.")
                raise OfferShopNameParsingError(self.bank.name, f"""Missing text in span tag. Span: {spans[0]}""")
            offer_description = spans[1].get_text(strip=True)
            logger.debug(f"Offer description found: {offer_description}")
            if not offer_description:
                logger.error(f"Missing text in span tag for {self.bank.name}.")
                raise OfferDescriptionParsingError(self.bank.name, f"""Missing text in span tag. Span: {spans[1]}""")

            offer = Offer(
                shop=Shop(name=shop_name),
                bank=self.bank,
                offer_type=self.offer_type,
                description=offer_description,
            )
            logger.debug(f"Parsed Offer: {offer}")
            results.add(offer)

        logger.debug(f"Parsing over. Found {len(results)} offers")
        return list(results)

    def __repr__(self):
        return f"{self.__class__.__name__}(bank_name={self.bank.name}, offer_type={self.offer_type})"
