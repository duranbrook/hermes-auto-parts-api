from dataclasses import dataclass
import httpx

NHTSA_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"

_FIELD_MAP = {
    "Make": "make",
    "Model": "model",
    "Model Year": "year",
    "Trim": "trim",
    "Engine Configuration": "engine",
}


@dataclass
class VehicleInfo:
    make: str = "Unknown"
    model: str = "Unknown"
    year: str = "Unknown"
    trim: str = ""
    engine: str = ""


async def decode_vin(vin: str) -> VehicleInfo:
    """Call the free NHTSA VIN decode API and return structured vehicle info."""
    url = NHTSA_URL.format(vin=vin.strip().upper())
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    info = VehicleInfo()
    for entry in data.get("Results", []):
        field = _FIELD_MAP.get(entry.get("Variable", ""))
        value = (entry.get("Value") or "").strip()
        if field and value and value.lower() not in {"", "not applicable", "null"}:
            setattr(info, field, value.title() if field == "make" else value)
    return info
