from typing import List

from bs4 import BeautifulSoup, Tag

from cardwise.entities.Offer import Offer
from cardwise.entities.Shop import Shop
from cardwise.exceptions import (
    OfferDescriptionParsingError,
    OfferParsingError,
    OfferShopNameParsingError,
)
from cardwise.parsers.base import BankOfferParser


class ChaseOfferParser(BankOfferParser):
    def __init__(self):
        super().__init__(bank_name="Chase", parser_id="chase")

    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        results: List[Offer] = []
        divs = [tag for tag in soup.find_all("div", class_="r9jbije r9jbijl") if isinstance(tag, Tag)]

        if not divs:
            raise OfferParsingError(self.bank.name, "No valid divs found")

        for div in divs:
            spans = [span for span in div.find_all("span") if isinstance(span, Tag)]
            if len(spans) < 2:
                raise OfferParsingError(
                    self.bank.name,
                    f"""Offer data is incomplete: need at least 2 spans
                                        for shop name (index 0) and description (index 1).
                                        Found: {len(spans)} spans with spans: {spans}""",
                )

            shop_name = spans[0].get_text(strip=True)
            if not shop_name:
                raise OfferShopNameParsingError(self.bank.name, f"""Missing text in span tag. Span: {spans[0]}""")
            shop_description = spans[1].get_text(strip=True)
            if not shop_description:
                raise OfferDescriptionParsingError(self.bank.name, f"""Missing text in span tag. Span: {spans[1]}""")

            results.append(
                Offer(
                    shop=Shop(name=shop_name),
                    bank_info=self.bank,
                    offer_type="cashback",
                    description=shop_description,
                )
            )

        return results
