import argparse
import sys
from pathlib import Path
from typing import List

from cardwise.exceptions import CardwiseError
from cardwise.formatters.cli_formatter import CLIFormatter
from cardwise.formatters.json_formatter import JSONFormatter
from cardwise.matchers.rapidfuzz_matcher import RapidFuzzMatcher
from cardwise.parsers.BankOfAmericaOfferParser import BankOfAmericaOfferParser
from cardwise.parsers.base import BankOfferParser
from cardwise.parsers.CapitalOneOfferParser import CapitalOneOfferParser
from cardwise.parsers.ChaseOfferParser import ChaseOfferParser
from cardwise.services.offer_finder import OfferFinderService


def main():
    parser = argparse.ArgumentParser(description="Find the best card offers for given shop(s).")
    parser.add_argument("shops", nargs="+", help="Shop name(s) to search for")
    parser.add_argument(
        "--json",
        nargs="?",
        const=True,
        default=False,
        help="Output results in JSON format. Optionally provide a filename to save.",
    )
    parser.add_argument(
        "--html-dir",
        type=str,
        default="data/htmls",
        help="Directory containing bank offer HTML files",
    )
    args = parser.parse_args()

    try:
        html_dir = Path(args.html_dir)

        parsers: List[BankOfferParser] = [
            BankOfAmericaOfferParser(),
            CapitalOneOfferParser(),
            ChaseOfferParser(),
        ]

        matcher = RapidFuzzMatcher()
        formatter = JSONFormatter() if args.json else CLIFormatter()

        service = OfferFinderService(
            parsers=parsers,
            matcher=matcher,
            formatter=formatter,
            html_dir=html_dir,
        )

        output = service.find_offers(args.shops if len(args.shops) > 1 else args.shops[0])

        if isinstance(args.json, str):
            output_path = Path(args.json)
            output_path.write_text(output)
            print(f"✅ Output saved to {output_path}")
        else:
            print(output)

    except CardwiseError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
