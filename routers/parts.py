from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.vin_decoder import decode_vin
from services.db_adapter import get_db

router = APIRouter()


class LookupRequest(BaseModel):
    part_description: str
    vin: str


class LookupResponse(BaseModel):
    part_number: Optional[str]
    part_name: Optional[str]
    category: Optional[str]
    confidence: Optional[float]
    vehicle: dict
    source: str  # "db" | "not_found"


@router.post("/lookup", response_model=LookupResponse)
async def lookup_part(req: LookupRequest) -> LookupResponse:
    vehicle = await decode_vin(req.vin)
    db = get_db()
    result = await db.lookup(req.part_description, vehicle)

    vehicle_dict = {
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "trim": vehicle.trim,
    }

    if result is None:
        return LookupResponse(
            part_number=None,
            part_name=None,
            category=None,
            confidence=None,
            vehicle=vehicle_dict,
            source="not_found",
        )

    return LookupResponse(
        part_number=result.part_number,
        part_name=result.part_name,
        category=result.category,
        confidence=result.confidence,
        vehicle=vehicle_dict,
        source="db",
    )
