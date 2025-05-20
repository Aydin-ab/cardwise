from typing import List

from cardwise.entities.Offer import Offer
from cardwise.formatters.base import OfferFormatter

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


class CLIFormatter(OfferFormatter):
    def format(self, offers: List[Offer]) -> str:
        if not offers:
            return f"{DIM}No offers found.{RESET}"

        lines: List[str] = []
        for offer in offers:
            expiry = (
                f"{DIM}(expires: {offer.expiry_date.date()}){RESET}"
                if offer.expiry_date
                else f"{DIM}(no expiry date found){RESET}"
            )

            offer_type_color = OFFER_TYPE_COLOR.get(offer.offer_type, FG_MAGENTA)

            lines.append(
                f"{FG_CYAN}[{offer.bank_info.name}]{RESET} "
                f"{BOLD}{FG_WHITE}{offer.shop.name}{RESET}: "
                f"{offer_type_color}{offer.offer_type.upper()}{RESET} - "
                f"{offer.description} {expiry}"
            )

        return "\n".join(lines)
