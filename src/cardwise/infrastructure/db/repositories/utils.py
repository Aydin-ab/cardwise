from cardwise.infrastructure.db.repositories.base_offer_repository import OfferRepository
from cardwise.infrastructure.db.repositories.SQLModel_offer_repository import SQLModelOfferRepository


def get_offer_repository() -> OfferRepository:
    """
    Returns the appropriate offer repository based on the input parameter.
    For now, only SQLModelOfferRepository is supported.
    So it will always return an instance of SQLModelOfferRepository.

    Returns:
        OfferRepository: An instance of SQLModelOfferRepository.
    """
    return SQLModelOfferRepository()
