# pyright: reportMissingModuleSource=false

import json
import os
from typing import Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError
from bank_parser.logger import logger  # ✅ Import centralized logger
from utils.html_parser import read_html


def parse_bank_of_america_offers(
    html_path: Optional[str] = None, save_to: Optional[str] = None
) -> List[Dict[str, str]]:
    """Parse Bank of America offers from an HTML file."""
    if html_path is None:
        html_path = "htmls/bank_of_america_offers.html"

    logger.info(f"📂 Parsing Bank of America offers from: {html_path}")

    # ✅ Raise custom error if the file does not exist
    if not os.path.exists(html_path):
        logger.error(f"❌ File not found: {html_path}")
        raise MissingHTMLFileError("Bank of America", html_path)

    html_doc: str = read_html(html_path)
    soup: BeautifulSoup = BeautifulSoup(html_doc, "html.parser")

    results: List[Dict[str, str]] = []

    # ✅ Explicitly convert to a list and filter only `Tag` elements
    deal_wrappers: List[Tag] = [
        tag for tag in soup.find_all("div", class_="deal-logo-wrapper top") if isinstance(tag, Tag)
    ]

    if not deal_wrappers:
        logger.error(f"❌ No offers found in {html_path}")
        raise ValueError("❌ No valid offers found in the HTML file.")

    for wrapper in deal_wrappers:
        img_tag = wrapper.find("img")
        span_tag = wrapper.find("span", class_="deal-offer-percent")

        # ✅ Ensure img_tag and span_tag are valid
        if not isinstance(img_tag, Tag) or not img_tag.has_attr("alt"):
            logger.error("❌ Company name not found: no 'alt' attribute in img tag")
            raise InvalidOfferDataError("Bank of America", "Company name not found")

        if not isinstance(span_tag, Tag) or not span_tag.get_text(strip=True):
            logger.error(f"❌ Offer text missing for company '{img_tag['alt']}': no text found")
            raise InvalidOfferDataError(
                "Bank of America", f"Offer text not found for company '{img_tag['alt']}'"
            )

        # ✅ Extract and clean text safely
        company_name: str = str(img_tag["alt"]).replace(" Logo", "").strip()
        offer_text: str = span_tag.get_text(strip=True)

        results.append(
            {
                "company": company_name,
                "offer": offer_text,
                "bank": "Bank of America",
                "reward_type": "cash back",
            }
        )

        logger.info(f"✅ Offer parsed: {company_name} - {offer_text}")

    if save_to:
        try:
            with open(save_to, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)
            logger.info(f"💾 Offers saved to {save_to}")
        except Exception as e:
            logger.error(f"❌ Failed to save offers to {save_to}: {e}")

    logger.info(f"✅ Successfully parsed {len(results)} Bank of America offers")
    return results
