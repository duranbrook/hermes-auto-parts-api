import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app

client = TestClient(app)


def test_lookup_with_mock_db_returns_part():
    with patch("routers.parts.decode_vin", new=AsyncMock(return_value=type("V", (), {
        "make": "Honda", "model": "Civic", "year": "2021", "trim": "Sport", "engine": ""
    })())):
        resp = client.post("/lookup", json={
            "part_description": "front brake caliper single piston",
            "vin": "1HGBH41JXMN109186"
        })
    assert resp.status_code == 200
    body = resp.json()
    assert body["part_number"] is not None
    assert body["source"] == "db"
    assert body["vehicle"]["make"] == "Honda"


def test_lookup_unknown_part_returns_not_found():
    with patch("routers.parts.decode_vin", new=AsyncMock(return_value=type("V", (), {
        "make": "Unknown", "model": "Unknown", "year": "Unknown", "trim": "", "engine": ""
    })())):
        resp = client.post("/lookup", json={
            "part_description": "totally unknown widget xyz",
            "vin": "BADVIN"
        })
    assert resp.status_code == 200
    body = resp.json()
    assert body["source"] == "not_found"
    assert body["part_number"] is None


def test_lookup_missing_fields_returns_422():
    resp = client.post("/lookup", json={"vin": "1HGBH41JXMN109186"})
    assert resp.status_code == 422
