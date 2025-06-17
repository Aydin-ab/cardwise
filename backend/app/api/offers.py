import logging
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from backend.app.db.session import get_session
from backend.app.services.offer_service import OfferService
from cardwise.domain.models.offer import Offer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/search")
def search_offers(
    shops: List[str] = Query(..., description="Fuzzy search for shop names"),
    session: Session = Depends(get_session),
) -> List[Offer]:
    logger.info(f"🔍 Search request received with shop queries: {shops}")
    service = OfferService(session)
    offers = service.fuzzy_search(shops)
    logger.info(f"🔎 Found {len(offers)} offers matching fuzzy search.")
    return offers


@router.get("/")
def get_offers_paginated(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
) -> List[Offer]:
    logger.info(f"📄 Paginated request received: limit={limit}, offset={offset}")
    service = OfferService(session)
    offers = service.list_offers_paginated(limit=limit, offset=offset)
    logger.info(f"📦 Returned {len(offers)} offers (paginated)")
    return offers


@router.get("/all")
def get_all_offers(session: Session = Depends(get_session)) -> List[Offer]:
    logger.info("📥 Full offers list requested.")
    service = OfferService(session)
    offers = service.list_offers()
    logger.info(f"📤 Returned {len(offers)} total offers.")
    return offers
