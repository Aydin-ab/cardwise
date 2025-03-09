import os
import json
from bs4 import BeautifulSoup
from utils.html_parser import read_html
from bank_parser.exceptions import MissingHTMLFileError, InvalidOfferDataError


def parse_bank_of_america_offers(html_path=None, save_to=None):
    """Parse Bank of America offers from an HTML file."""
    if not html_path:
        html_path = "htmls/bank_of_america_offers.html"

    # ✅ Raise custom error if the file does not exist
    if not os.path.exists(html_path):
        raise MissingHTMLFileError("Bank of America", html_path)

    html_doc = read_html(html_path)
    soup = BeautifulSoup(html_doc, "html.parser")

    results = []
    deal_wrappers = soup.find_all("div", class_="deal-logo-wrapper top")

    if not deal_wrappers:
        raise ValueError("❌ No valid offers found in the HTML file.")

    for wrapper in deal_wrappers:
        img_tag = wrapper.find("img")
        span_tag = wrapper.find("span", class_="deal-offer-percent")

        # ✅ Raise an error if company name is missing
        if not img_tag or not img_tag.has_attr("alt"):
            raise InvalidOfferDataError("Bank of America", "Company name not found")

        # ✅ Raise an error if the offer amount is missing
        if not span_tag or not span_tag.get_text(strip=True):
            raise InvalidOfferDataError(
                "Bank of America", f"Offer text not found for company '{img_tag['alt']}'"
            )

        # ✅ Extract the offer information
        company_name = img_tag["alt"].replace(" Logo", "").strip()
        offer_text = span_tag.get_text(strip=True)

        results.append(
            {
                "company": company_name,
                "offer": offer_text,
                "bank": "Bank of America",
                "reward_type": "cash back",
            }
        )

    if save_to:
        with open(save_to, "w") as f:
            json.dump(results, f, indent=4)

    return results
