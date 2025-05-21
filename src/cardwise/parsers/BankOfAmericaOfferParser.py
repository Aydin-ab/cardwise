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


class BankOfAmericaOfferParser(BankOfferParser):
    def __init__(self):
        super().__init__(bank_name="Bank of America", parser_id="bank_of_america")

    def _extract_offers(self, soup: BeautifulSoup) -> List[Offer]:
        results: set[Offer] = set()

        deal_wrappers = [tag for tag in soup.find_all("div", class_="deal-logo-wrapper top") if isinstance(tag, Tag)]

        if not deal_wrappers:
            raise OfferParsingError(self.bank.name, "No offer wrappers found")

        for wrapper in deal_wrappers:
            img_tag = wrapper.find("img")
            span_tag = wrapper.find("span", class_="deal-offer-percent")

            if not isinstance(img_tag, Tag) or not img_tag.has_attr("alt"):
                raise OfferShopNameParsingError(
                    self.bank.name,
                    f"""Missing 'alt' in img tag.
                                                                    Found img tag: {img_tag}""",
                )
            shop_name = str(img_tag["alt"]).replace(" Logo", "").strip()

            if not isinstance(span_tag, Tag):
                raise OfferDescriptionParsingError(
                    self.bank.name,
                    f"""Span found is not a tag.
                                                                        Found: {span_tag}""",
                )
            offer_description = span_tag.get_text(strip=True)
            if not offer_description:
                raise OfferDescriptionParsingError(
                    self.bank.name,
                    f"""Missing text in span tag.
                                                                        Span: {span_tag}""",
                )

            results.add(
                Offer(
                    shop=Shop(name=shop_name),
                    bank_info=self.bank,
                    offer_type="cashback",
                    description=offer_description,
                )
            )

        return list(results)
