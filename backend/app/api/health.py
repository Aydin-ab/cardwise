from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", include_in_schema=False)
def ping() -> dict[str, str]:
    return {"status": "pong"}


@router.get("/health", include_in_schema=False)
def health() -> dict[str, str]:
    return {"status": "ok"}
