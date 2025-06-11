import argparse
import logging.config
import sys
import traceback
from pathlib import Path
from typing import List

import yaml

from cardwise.app.data_loader import OfferDataLoader
from cardwise.app.offer_finder_service import OfferFinderService
from cardwise.domain.formatters.cli_offer_formatter import CLIOfferFormatter
from cardwise.domain.formatters.json_offer_formatter import JSONOfferFormatter
from cardwise.domain.matchers.rapidfuzz_shopmatcher import RapidFuzzShopMatcher
from cardwise.infrastructure.db.repositories.SQLModel_offer_repository import SQLModelOfferRepository
from cardwise.infrastructure.db.session import init_db
from cardwise.infrastructure.logs.logging import set_log_level
from cardwise.infrastructure.parsers.bank_of_america_offer_parser import BankOfAmericaOfferParser
from cardwise.infrastructure.parsers.base_offer_parser import BankOfferParser
from cardwise.infrastructure.parsers.capital_one_offer_parser import CapitalOneOfferParser
from cardwise.infrastructure.parsers.chase_offer_parser import ChaseOfferParser
from cardwise.shared.exceptions import CardwiseError

with open("src/cardwise/logs/logging_config.yaml", "r") as f:
    logging_config = yaml.safe_load(f)

logging.config.dictConfig(logging_config)
logger = logging.getLogger("cardwise")


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
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh the database by clearing all offers and recomputing from HTML files.",
    )
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("--log-level", help="Set log level manually", type=str, default=None)
    args = parser.parse_args()
    set_log_level(logger, verbosity=args.verbose, manual_level=args.log_level)

    # Log the command line arguments
    logger.debug(f"Running command: {' '.join(sys.argv)}")
    logger.debug(f"param HTML directory: {args.html_dir}")
    logger.debug(f"param Shops: {args.shops}")
    logger.debug(f"param Refresh: {args.refresh}")
    logger.debug(f"param JSON output: {args.json}")
    logger.debug(f"param Verbose level: {args.verbose}")
    logger.debug(f"param Log level: {args.log_level}")

    logger.debug("Initializing database...")
    init_db()

    try:
        html_dir = Path(args.html_dir)

        parsers: List[BankOfferParser] = [
            BankOfAmericaOfferParser(),
            CapitalOneOfferParser(),
            ChaseOfferParser(),
        ]
        logger.debug(f"{len(parsers)} Parsers initialized: {parsers}")
        repository = SQLModelOfferRepository()
        logger.debug(f"Repository initialized: {repository}")
        data_loader = OfferDataLoader(parsers, html_dir, repository)
        logger.debug(f"Data loader initialized: {data_loader}")
        if args.refresh:
            logger.debug("Refreshing offers from HTML files...")
            data_loader.refresh_offers_from_html()
            print("✅ Offers database cleared and recomputed from HTML")
        shop_matcher = RapidFuzzShopMatcher()
        logger.debug(f"Matcher initialized: {shop_matcher}")
        formatter = JSONOfferFormatter() if args.json else CLIOfferFormatter()
        logger.debug(f"Formatter initialized: {formatter}")

        finder_service = OfferFinderService(
            data_loader=data_loader,
            shop_matcher=shop_matcher,
            formatter=formatter,
        )
        logger.debug(f"Finder service initialized: {finder_service}")
        logger.debug("Precomputing offers for faster finder service later.")
        finder_service.precompute_offers()

        output = finder_service.find_offers(args.shops if len(args.shops) > 1 else args.shops[0])
        logger.debug(f"Output formatted: {output}")
        if isinstance(args.json, str):
            logger.debug(f"Saving output to JSON file: {args.json}")
            output_path = Path(args.json)
            output_path.write_text(output)
            logger.info(f"Output saved to {output_path}")
            print(f"✅ Output saved to {output_path}")
        else:
            logger.debug("Outputting results to console")
            print(output)

    except CardwiseError as e:
        # Handle CardwiseError specifically
        logger.exception(e)
        traceback.print_exc()
        sys.exit(1)

    except Exception as e:
        # Handle any other unexpected errors
        logger.exception(e)
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
