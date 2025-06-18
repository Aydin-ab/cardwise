import logging
from pathlib import Path

import toml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import health, offers
from backend.app.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

logger.info("🚀 Starting Cardwise API...")


def get_project_version() -> str:
    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    data = toml.load(pyproject)
    return data["project"]["version"]


app = FastAPI(
    title="Cardwise API",
    description="API for accessing parsed card offers",
    version=get_project_version(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔓 Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(offers.router, prefix="/offers", tags=["Offers"])
app.include_router(health.router)

logger.info("✅ Cardwise API is ready.")
