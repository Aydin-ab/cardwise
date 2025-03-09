import argparse
import json
from typing import Dict, List, Tuple

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
        "[--bofa-html path.html] [--capone-html path.html] [--chase-html path.html]",
        epilog="""Example Output:
        ✅ Found 2 offers for 'starbucks':
        - Bank of America: 10% Cash Back (cash back)
        - Capital One: 5X miles (points)
        💾 Results saved to offers.json
        """,
    )

    # Accept one or more company names
    parser.add_argument(
        "queries", nargs="*", type=str, help="Company names (e.g., Starbucks McDonald's)"
    )

    # Optional flag to save results
    parser.add_argument(
        "-s",
        "--save",
        nargs="?",
        const="offers.json",
        type=str,
        help="Save results to a JSON file (default: offers.json)",
    )

    # Separate optional HTML paths for each bank
    parser.add_argument("--bofa-html", type=str, help="Custom HTML file for Bank of America")
    parser.add_argument("--capone-html", type=str, help="Custom HTML file for Capital One")
    parser.add_argument("--chase-html", type=str, help="Custom HTML file for Chase")

    return parser.parse_args()


def build_html_paths(args: argparse.Namespace) -> Dict[str, str]:
    """Constructs a dictionary of provided HTML file paths, filtering out None values."""
    return {
        bank: path
        for bank, path in {
            "bank_of_america": args.bofa_html,
            "capital_one": args.capone_html,
            "chase": args.chase_html,
        }.items()
        if path is not None
    }


def process_company_offers(
    queries: List[str], html_paths: Dict[str, str]
) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Retrieves and processes offers for each queried company.

    Returns:
        Tuple containing:
        - List of offers found
        - List of warnings related to missing HTML files
    """
    all_offers: List[Dict[str, str]] = []
    all_warnings: List[str] = []

    for query in queries:
        offers, warnings = get_offers_for_company(query, html_paths)

        if warnings:
            all_warnings.extend(warnings)

        if offers:
            all_offers.extend(offers)
            print(f"{GREEN}✅ Found {len(offers)} offers for '{query}':{RESET}")
            for offer in offers:
                print(f"- {offer['bank']}: {offer['offer']} ({offer['reward_type']})")
        else:
            print(f"{RED}❌ No offers found for '{query}'.{RESET}")

    return all_offers, all_warnings


def display_warnings(warnings: List[str]) -> None:
    """Displays warnings related to missing bank data."""
    if warnings:
        print(f"\n{YELLOW}⚠️ Warning: Some bank data was unavailable:{RESET}")
        for warning in set(warnings):  # Avoid duplicate warnings
            print(f"   {YELLOW}- {warning}{RESET}")


def save_offers(offers: List[Dict[str, str]], save_path: str) -> None:
    """Saves retrieved offers to a JSON file."""
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(offers, f, indent=4)
    print(f"💾 {GREEN}Results saved to {save_path}{RESET}")


def main() -> None:
    """Main function to execute the offer search process."""
    args = parse_arguments()

    if not args.queries:
        print(f"\n{RED}❌ Error: You must provide at least one company name to search for.{RESET}")
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
        print(f"{RED}❌ No offers found for any of the provided companies.{RESET}")
    elif args.save:
        save_offers(all_offers, args.save)


if __name__ == "__main__":
    main()
