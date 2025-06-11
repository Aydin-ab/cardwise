import logging
from typing import List

from cardwise.domain.formatters.base_offer_formatter import OfferFormatter
from cardwise.domain.models.offer import Offer

logger = logging.getLogger(__name__)

# ANSI escape codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

FG_CYAN = "\033[36m"
FG_GREEN = "\033[32m"
FG_BLUE = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_WHITE = "\033[37m"
FG_GRAY = "\033[90m"

OFFER_TYPE_COLOR = {
    "cashback": FG_GREEN,
    "points": FG_BLUE,
    "misc": FG_MAGENTA,
}


class CLIOfferFormatter(OfferFormatter):
    def format(self, offers: List[Offer]) -> str:
        if not offers:
            logger.debug("No offers found to format.")
            return f"{DIM}No offers found.{RESET}"

        lines: List[str] = []
        logger.debug(f"Formatting {len(offers)} offers for CLI output.")
        for offer in offers:
            expiry = (
                f"{DIM}(expires: {offer.expiry_date.date()}){RESET}"
                if offer.expiry_date
                else f"{DIM}(no expiry date found){RESET}"
            )

            offer_type_color = OFFER_TYPE_COLOR.get(offer.offer_type, FG_MAGENTA)

            offer_formatted = (
                f"{FG_CYAN}[{offer.bank.name}]{RESET} "
                f"{BOLD}{FG_WHITE}{offer.shop.name}{RESET}: "
                f"{offer_type_color}{offer.offer_type.upper()}{RESET} - "
                f"{offer.description} {expiry}"
            )
            logger.debug(f"Formatted offer: {offer_formatted}")
            lines.append(offer_formatted)

        return "\n".join(lines)

    def __repr__(self):
        return f"{self.__class__.__name__}()"
