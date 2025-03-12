import argparse
import json
from collections import defaultdict
from typing import Dict, List, Tuple

from bank_parser.logger import logger, set_log_level  # ✅ Import centralized logger
from utils.fuzzy_matcher import get_offers_for_company

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"  # Reset to default terminal color


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for the offer search script."""
    parser = argparse.ArgumentParser(
        description="Find the best offers for one or more companies.",
        usage='search_offer "starbucks" "mcdonalds" [--save results.json] '
        "[--bofa-html path.html] [--capone-html path.html] [--chase-html path.html]"
        " [-v | -vv | -vvv] [--log-level INFO]",
    )

    parser.add_argument("queries", nargs="*", type=str, help="Company names to search for")

    parser.add_argument(
        "-s",
        "--save",
        nargs="?",
        const="results.json",
        type=str,
        help="Save results to a JSON file (default: results.json)",
    )

    parser.add_argument(
        "--bofa-html",
        type=str,
        default="htmls/bank_of_america_offers.html",
        help="Custom HTML file for Bank of America",
    )
    parser.add_argument(
        "--capone-html",
        type=str,
        default="htmls/capital_one_offers.html",
        help="Custom HTML file for Capital One",
    )
    parser.add_argument(
        "--chase-html",
        type=str,
        default="htmls/chase_offers.html",
        help="Custom HTML file for Chase",
    )

    # 🔥 Add verbosity flag (-v, -vv, -vvv)
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv, -vvv)")

    # 🔥 Add explicit log level flag (Overrides -v if used)
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Manually set log level",
    )

    args = parser.parse_args()

    # 🔥 Apply log level (Priority: `--log-level` > `-v`)
    set_log_level(args.verbose, args.log_level)

    logger.info(f"Parsed arguments: {vars(args)}")  # Log parsed arguments
    return args


def build_html_paths(args: argparse.Namespace) -> Dict[str, str]:
    """Constructs a dictionary of provided HTML file paths, filtering out None values."""
    paths = {
        "bank_of_america": args.bofa_html,
        "capital_one": args.capone_html,
        "chase": args.chase_html,
    }
    html_paths = {bank: path for bank, path in paths.items() if path is not None}

    logger.info(f"Using HTML files: {html_paths}")
    return html_paths


def process_company_offers(queries: List[str], html_paths: Dict[str, str]) -> Tuple[List[Dict[str, str]], List[str]]:
    """Retrieves and processes offers for each queried company."""
    all_offers: List[Dict[str, str]] = []
    all_warnings: List[str] = []

    for query in queries:
        logger.info(f"🔍 Searching offers for '{query}'...")
        offers, warnings = get_offers_for_company(query, html_paths)

        if warnings:
            all_warnings.extend(warnings)
            logger.warning(f"⚠️ Warnings encountered for {query}: {warnings}")

        if offers:
            all_offers.extend(offers)
            logger.info(f"✅ Found {len(offers)} offers for '{query}'")
        else:
            logger.info(f"❌ No offers found for '{query}'")

    return all_offers, all_warnings


def display_warnings(warnings: List[str]) -> None:
    """Displays warnings related to missing bank data."""
    if warnings:
        logger.warning(f"⚠️ Missing bank data: {warnings}")
        for warning in set(warnings):
            print(f"{YELLOW}- {warning}{RESET}")  # Keep this for user readability


def save_offers(offers: List[Dict[str, str]], save_path: str) -> None:
    """Saves retrieved offers to a JSON file."""
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(offers, f, indent=4)
        logger.info(f"💾 Results saved to {save_path}")
    except Exception as e:
        logger.error(f"❌ Failed to save offers: {e}")


def main() -> None:
    """Main function to execute the offer search process."""
    args = parse_arguments()

    if not args.queries:
        error_msg = "❌ Error: You must provide at least one company name to search for."
        logger.error(error_msg)
        print(f"\n{RED}{error_msg}{RESET}")
        print(f"{BLUE}🔹 Example usage:{RESET}")
        print('   search_offer "starbucks" "mcdonalds"')
        print(
            '   search_offer "nike" --save my_results.json '
            "--bofa-html custom_bofa.html --capone-html custom_capone.html\n"
        )
        return

    html_paths = build_html_paths(args)
    all_offers, all_warnings = process_company_offers(args.queries, html_paths)

    display_warnings(all_warnings)

    if not all_offers:
        logger.info("❌ No offers found for any company.")
        print(f"{RED}❌ No offers found for any of the provided companies.{RESET}")
        return

    # ✅ Group offers by company
    offers_by_company: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for offer in all_offers:
        offers_by_company[offer["company"]].append(offer)

    # ✅ Print grouped offers
    print("\n🔹 Here are the best offers found:\n")
    for company, offers in offers_by_company.items():
        print(f"{BLUE}📌 {company}{RESET}")  # Company header
        for offer in offers:
            print(f"  {GREEN}- {offer['bank']}: {offer['offer']} ({offer['reward_type']}){RESET}")

    if args.save:
        save_offers(all_offers, args.save)


if __name__ == "__main__":
    main()
