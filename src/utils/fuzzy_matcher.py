# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportMissingImports=false

import json
import logging
from typing import Callable, Dict, List, Optional, Tuple

from rapidfuzz import fuzz, process

from bank_parser.bank_of_america import parse_bank_of_america_offers
from bank_parser.capital_one import parse_capital_one_offers
from bank_parser.chase import parse_chase_offers

# ✅ Define parser functions for each bank
PARSERS: Dict[str, Callable[[Optional[str]], List[Dict[str, str]]]] = {
    "bank_of_america": parse_bank_of_america_offers,
    "capital_one": parse_capital_one_offers,
    "chase": parse_chase_offers,
}

logger = logging.getLogger("cardwise")


def load_fresh_offers(
    html_paths: Optional[Dict[str, str]] = None, output_file: Optional[str] = None
) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Dynamically calls all parsers, merges offers, and optionally saves to JSON.

    Args:
        html_paths: Optional dictionary mapping banks to custom HTML paths.
        output_file: Optional path to save merged offers as JSON.

    Returns:
        Tuple containing:
        - List of offers from available banks.
        - List of warnings for banks with missing files.
    """
    if html_paths is None:
        html_paths = {}

    logger.info("🔄 Loading fresh offers from banks...")
    offers: List[Dict[str, str]] = []
    warnings: List[str] = []  # Track missing banks

    for bank, parser in PARSERS.items():
        try:
            logger.info(f"📂 Start parsing offers from {bank}...")
            bank_offers = parser(html_paths.get(bank))
            offers.extend(bank_offers)
            logger.info(f"✅ Finished loading {len(bank_offers)} offers from {bank}")
        except Exception as e:
            warnings.append(str(e))
            logger.warning(f"⚠️ Skipping {bank}; Cause: {e}")

    # ✅ Save results to JSON if output_file is provided
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(offers, f, indent=4)
        logger.info(f"💾 Offers successfully saved to {output_file}")

    logger.info(f"✅ Finished loading offers. Total offers: {len(offers)}")
    return offers, warnings


def find_best_matches(user_input: str, company_names: List[str], threshold: int = 80) -> List[str]:
    """
    Finds all company names that match the user input above a similarity threshold.

    Args:
        user_input: The company name input by the user.
        company_names: List of company names in the dataset.
        threshold: Minimum similarity score to consider a valid match.

    Returns:
        List of matching company names.
    """
    logger.info(f"🔎 Searching for matches for: '{user_input}' (threshold: {threshold})")

    matches = process.extract(user_input, company_names, scorer=fuzz.ratio, limit=None)
    filtered_matches: List[str] = [match[0] for match in matches if match[1] >= threshold]

    if filtered_matches:
        logger.info(f"✅ Matches found for '{user_input}': {filtered_matches}")
    else:
        logger.warning(f"⚠️ No close matches found for '{user_input}'")

    return filtered_matches


def get_offers_for_company(
    user_input: str, html_paths: Optional[Dict[str, str]] = None
) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Retrieves all offers for the best-matching companies based on user input.

    Args:
        user_input: The company name input by the user.
        html_paths: Optional dictionary mapping banks to custom HTML paths.

    Returns:
        Tuple containing:
        - List of offers for all matching companies.
        - List of warnings for banks that couldn't be processed.
    """
    offers, warnings = load_fresh_offers(html_paths)

    if not offers:
        logger.warning("⚠️ No offers found from any bank, nothing to search from")
        return [], warnings  # Return warnings if no offers available

    # Extract all unique company names
    company_names: List[str] = list({offer["company"].lower().strip() for offer in offers})

    # Find all matching company names
    best_matches: List[str] = find_best_matches(user_input.lower().strip(), company_names)

    if best_matches:
        matched_offers = [offer for offer in offers if offer["company"].lower().strip() in best_matches]
        logger.info(f"✅ Found {len(matched_offers)} offers for '{user_input}'")
        return matched_offers, warnings

    logger.warning(f"⚠️ No offers found for '{user_input}' after fuzzy matching through all banks")
    return [], warnings  # No match found, but still return warnings
