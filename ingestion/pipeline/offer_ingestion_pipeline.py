# ingestion/pipeline/offer_ingestion_pipeline.py
import logging
from pathlib import Path
from typing import List

from cardwise.domain.models.offer import Offer
from ingestion.parser_registry import discover_parsers
from ingestion.persistence.repository import OfferRepository
from ingestion.pipeline.load_htmls import load_htmls

logger = logging.getLogger(__name__)


class OfferIngestionPipeline:
    def __init__(self, html_folder: Path, repository: OfferRepository):
        self.html_folder = html_folder
        self.repository = repository
        self.parsers = discover_parsers()

    def run(self) -> List[Offer]:
        logger.info("🔄 Running ingestion pipeline...")
        offer_docs = load_htmls()
        parser_map = {parser.bank.id: parser for parser in self.parsers}

        offers: List[Offer] = []

        for bank_id, html_doc in offer_docs:
            parser = parser_map.get(bank_id)
            if not parser:
                logger.warning(f"❌ No parser found for bank: '{bank_id}', skipping file: {html_doc}")
                continue
            logger.info(f"📝 Parsing html docs: {bank_id} using {parser.__class__.__name__}")
            parsed = parser.parse(html_doc)
            logger.info(f"✅ Parsed {len(parsed)} offer(s) from {bank_id}")
            offers.extend(parsed)

        logger.info(f"📦 Going to insert {len(offers)} offer(s) into the database...")
        self.repository.delete_all()
        self.repository.insert_many(offers)

        logger.info("🎉 Ingestion pipeline complete.")
        return offers
