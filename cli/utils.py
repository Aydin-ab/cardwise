from typing import List

from cardwise.domain.models.offer import Offer, OfferTypeEnum

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
    OfferTypeEnum.CASHBACK: FG_GREEN,
    OfferTypeEnum.POINTS: FG_BLUE,
    OfferTypeEnum.MISC: FG_MAGENTA,
}


def print_offers(offers: List[Offer]):
    if not offers:
        print(f"{DIM}No offers found.{RESET}")

    lines: List[str] = []
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
        lines.append(offer_formatted)

    print("\n".join(lines))
