# pyright: reportMissingModuleSource=false

import json
import os
from typing import Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError
from bank_parser.logger import logger  # ✅ Import centralized logger
from utils.html_parser import read_html


def parse_chase_offers(html_path: Optional[str] = None, save_to: Optional[str] = None) -> List[Dict[str, str]]:
    """Parse Chase offers from an HTML file."""
    if html_path is None:
        html_path = "htmls/chase_offers.html"

    logger.info(f"📂 Parsing Chase offers from: {html_path}")

    # ✅ Raise custom error if the file does not exist
    if not os.path.exists(html_path):
        logger.error(f"❌ File not found: {html_path}")
        raise MissingHTMLFileError("Chase", html_path)

    html_doc: str = read_html(html_path)
    soup: BeautifulSoup = BeautifulSoup(html_doc, "html.parser")

    results: List[Dict[str, str]] = []

    # ✅ Convert to list and filter only `Tag` elements
    divs: List[Tag] = [tag for tag in soup.find_all("div", class_="r9jbije r9jbijl") if isinstance(tag, Tag)]

    if not divs:
        logger.error(f"❌ No offers found in {html_path}: no valid divs found")
        raise ValueError("❌ No valid offers found in the Chase HTML file.")

    for div in divs:
        # ✅ Ensure spans are `Tag` elements
        spans: List[Tag] = [span for span in div.find_all("span") if isinstance(span, Tag)]

        # ✅ Ensure spans exist and have correct format
        if len(spans) < 2:
            logger.error("❌ Can't find offer, offer is incomplete or malformed: missing spans")
            raise InvalidOfferDataError("Chase", "Offer data is incomplete or malformed")

        company_name: str = spans[0].get_text(strip=True)
        offer_text: str = spans[1].get_text(strip=True)

        # ✅ Normalize Text
        company_name = company_name.strip()
        offer_text = offer_text.strip()

        # ✅ Raise errors if any critical data is missing
        if not company_name:
            logger.error("❌ Missing company name in Chase offers")
            raise InvalidOfferDataError("Chase", "Company name not found")
        if not offer_text:
            logger.error(f"❌ Missing offer text for '{company_name}'")
            raise InvalidOfferDataError("Chase", f"Offer text not found for '{company_name}'")

        # ✅ Add metadata directly here
        results.append(
            {
                "company": company_name,
                "offer": offer_text,
                "bank": "Chase",
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

    logger.info(f"✅ Successfully parsed {len(results)} Chase offers")
    return results
