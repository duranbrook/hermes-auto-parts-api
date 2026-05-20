from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from services.vin_decoder import VehicleInfo


@dataclass
class PartResult:
    part_number: str
    part_name: str
    category: str
    confidence: float


class PartsDB(ABC):
    @abstractmethod
    async def lookup(self, part_description: str, vehicle: VehicleInfo) -> Optional[PartResult]:
        """Return the best matching part or None if not found."""


class MockPartsDB(PartsDB):
    """Stub that returns plausible fake data. Replace with a real DB implementation."""

    async def lookup(self, part_description: str, vehicle: VehicleInfo) -> Optional[PartResult]:
        desc_lower = part_description.lower()
        if "brake" in desc_lower and "caliper" in desc_lower:
            return PartResult("33901-S84-A01", "Brake Caliper – Front", "Brakes", 0.75)
        if "brake" in desc_lower and "pad" in desc_lower:
            return PartResult("45022-S84-A10", "Brake Pad Set – Front", "Brakes", 0.75)
        if "filter" in desc_lower and "oil" in desc_lower:
            return PartResult("15400-PLM-A02", "Oil Filter", "Engine", 0.80)
        if "alternator" in desc_lower:
            return PartResult("31100-P8A-A01", "Alternator Assembly", "Electrical", 0.70)
        return None


def get_db() -> PartsDB:
    """Return the active DB adapter based on PARTS_DB_BACKEND env var."""
    import os
    backend = os.getenv("PARTS_DB_BACKEND", "mock").strip().lower()
    if backend == "mock":
        return MockPartsDB()
    raise ValueError(f"Unknown PARTS_DB_BACKEND: {backend!r}. Only 'mock' is supported right now.")
