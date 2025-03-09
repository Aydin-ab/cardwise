import json
import os

from bs4 import BeautifulSoup

from bank_parser.exceptions import InvalidOfferDataError, MissingHTMLFileError
from utils.html_parser import read_html


def parse_chase_offers(html_path=None, save_to=None):
    """Parse Chase offers from an HTML file."""
    if not html_path:
        html_path = "htmls/chase_offers.html"

    # ✅ Raise custom error if the file does not exist
    if not os.path.exists(html_path):
        raise MissingHTMLFileError("Chase", html_path)

    html_doc = read_html(html_path)
    soup = BeautifulSoup(html_doc, "html.parser")

    results = []
    divs = soup.find_all("div", class_="r9jbije r9jbijl")

    if not divs:
        raise ValueError("❌ No valid offers found in the Chase HTML file.")

    for div in divs:
        spans = div.find_all("span")

        # ✅ Ensure spans exist and have correct format
        if len(spans) < 2:
            raise InvalidOfferDataError("Chase", "Offer data is incomplete or malformed")

        company_name = spans[0].get_text(strip=True)
        offer_text = spans[1].get_text(strip=True)

        # ✅ Normalize Text
        company_name = company_name.strip()
        offer_text = offer_text.strip()

        # ✅ Raise errors if any critical data is missing
        if not company_name:
            raise InvalidOfferDataError("Chase", "Company name not found")
        if not offer_text:
            raise InvalidOfferDataError(
                "Chase", f"Offer text not found for company '{company_name}'"
            )

        # ✅ Add metadata directly here
        results.append(
            {
                "company": company_name,
                "offer": offer_text,
                "bank": "Chase",
                "reward_type": "cash back",
            }
        )

    if save_to:
        with open(save_to, "w") as f:
            json.dump(results, f, indent=4)

    return results
