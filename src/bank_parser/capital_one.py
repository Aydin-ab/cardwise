# pyright: reportMissingModuleSource=false

import json
import os
import re
from typing import Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError
from bank_parser.logger import logger  # ✅ Import centralized logger
from utils.html_parser import read_html


def parse_capital_one_offers(
    html_path: Optional[str] = None, save_to: Optional[str] = None
) -> List[Dict[str, str]]:
    """Parse Capital One offers from an HTML file."""
    if html_path is None:
        html_path = "htmls/capital_one_offers.html"

    logger.info(f"📂 Parsing Capital One offers from: {html_path}")

    # ✅ Raise error if file doesn't exist
    if not os.path.exists(html_path):
        logger.error(f"❌ File not found: {html_path}")
        raise MissingHTMLFileError("Capital One", html_path)

    html_doc: str = read_html(html_path)
    soup: BeautifulSoup = BeautifulSoup(html_doc, "html.parser")

    results: List[Dict[str, str]] = []

    # ✅ Ensure we only work with `Tag` elements
    tiles: List[Tag] = [
        tag
        for tag in soup.find_all(
            "div", class_="standard-tile relative flex flex-col justify-between w-full h-full mt-0"
        )
        if isinstance(tag, Tag)
    ]

    if not tiles:
        logger.error(f"❌ No offers found in {html_path}: no valid tiles found")
        raise ValueError("❌ No valid offers found in the Capital One HTML file.")

    for tile in tiles:
        img_tag = tile.find("img")

        # ✅ Ensure img_tag is a Tag and has `src`
        if not isinstance(img_tag, Tag) or not img_tag.has_attr("src"):
            logger.error("❌ Can't find offer: Image tag not found or missing 'src' attribute")
            raise InvalidOfferDataError(
                "Capital One", "Image tag not found or missing 'src' attribute"
            )

        # 🔥 **Fix: Explicitly cast to `str`**
        src_attr = img_tag["src"]
        if isinstance(src_attr, list):  # Handle case where it's a list
            src_url: str = src_attr[0]  # Take the first element if it's a list
        else:
            src_url: str = str(src_attr)  # Convert to string if needed

        match: Optional[re.Match[str]] = re.search(r"domain=([^.]+)\.", src_url)

        if match:
            company_name: str = match.group(1).strip()
        else:
            logger.error("❌ Company name not found in image URL")
            raise InvalidOfferDataError("Capital One", "Company name not found in the image URL")

        offer_divs: List[Tag] = [div for div in tile.find_all("div") if isinstance(div, Tag)]
        if len(offer_divs) < 2:
            logger.error(f"❌ Offer text missing for company '{company_name}': no text found")
            raise InvalidOfferDataError(
                "Capital One", f"Offer text not found for company '{company_name}'"
            )

        offer_text: str = offer_divs[1].get_text(strip=True)

        if not offer_text:
            logger.error(f"❌ Offer text is empty for '{company_name}'")
            raise InvalidOfferDataError(
                "Capital One", f"Offer text is empty for company '{company_name}'"
            )

        # ✅ Normalize extracted text
        company_name = company_name.strip()
        offer_text = offer_text.strip()

        # ✅ Append data
        results.append(
            {
                "company": company_name,
                "offer": offer_text,
                "bank": "Capital One",
                "reward_type": "points",
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

    logger.info(f"✅ Successfully parsed {len(results)} Capital One offers")
    return results
