import os
import re
import json
from bs4 import BeautifulSoup
from utils.html_parser import read_html
from bank_parser.exceptions import MissingHTMLFileError, InvalidOfferDataError


def parse_capital_one_offers(html_path=None, save_to=None):
    """Parse Capital One offers from an HTML file."""
    if not html_path:
        html_path = "htmls/capital_one_offers.html"

    # ✅ Raise error if file doesn't exist
    if not os.path.exists(html_path):
        raise MissingHTMLFileError("Capital One", html_path)

    html_doc = read_html(html_path)
    soup = BeautifulSoup(html_doc, "html.parser")

    results = []
    tiles = soup.find_all(
        "div", class_="standard-tile relative flex flex-col justify-between w-full h-full mt-0"
    )

    if not tiles:
        raise ValueError("❌ No valid offers found in the Capital One HTML file.")

    for tile in tiles:
        img_tag = tile.find("img")
        if not img_tag or not img_tag.has_attr("src"):
            raise InvalidOfferDataError(
                "Capital One", "Image tag not found or missing 'src' attribute"
            )

        src_url = img_tag["src"]
        match = re.search(r"domain=([^.]+)\.", src_url)

        if match:
            company_name = match.group(1).strip()
        else:
            raise InvalidOfferDataError("Capital One", "Company name not found in the image URL")

        offer_divs = tile.find_all("div")
        if len(offer_divs) < 2:
            raise InvalidOfferDataError(
                "Capital One", f"Offer text not found for company '{company_name}'"
            )

        offer_text = offer_divs[1].get_text(strip=True)

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
        with open(save_to, "w") as f:
            json.dump(results, f, indent=4)

    return results
