# pyright: reportMissingModuleSource=false

import json
import os
import re
from typing import Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError
from utils.html_parser import read_html


def parse_capital_one_offers(
    html_path: Optional[str] = None, save_to: Optional[str] = None
) -> List[Dict[str, str]]:
    """Parse Capital One offers from an HTML file."""
    if html_path is None:
        html_path = "htmls/capital_one_offers.html"

    # ✅ Raise error if file doesn't exist
    if not os.path.exists(html_path):
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
        raise ValueError("❌ No valid offers found in the Capital One HTML file.")

    for tile in tiles:
        img_tag = tile.find("img")

        # ✅ Ensure img_tag is a Tag and has `src`
        if not isinstance(img_tag, Tag) or not img_tag.has_attr("src"):
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
            raise InvalidOfferDataError("Capital One", "Company name not found in the image URL")

        offer_divs: List[Tag] = [div for div in tile.find_all("div") if isinstance(div, Tag)]
        if len(offer_divs) < 2:
            raise InvalidOfferDataError(
                "Capital One", f"Offer text not found for company '{company_name}'"
            )

        offer_text: str = offer_divs[1].get_text(strip=True)

        if not offer_text:
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

    if save_to:
        with open(save_to, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

    return results
