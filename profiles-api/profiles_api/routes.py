from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root() -> dict[str, Any]:
    return {"Hello": "World"}
