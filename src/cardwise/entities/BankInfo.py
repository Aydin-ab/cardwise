from typing import Optional

from pydantic import BaseModel


class BankInfo(BaseModel):
    name: str  # Display name
    bank_id: Optional[str] = None  # Internal ID for parser/lookup
    website: Optional[str] = None
