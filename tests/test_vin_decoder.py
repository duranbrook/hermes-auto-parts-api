import pytest
from unittest.mock import AsyncMock, patch
from services.vin_decoder import decode_vin, VehicleInfo


@pytest.mark.asyncio
async def test_decode_vin_returns_vehicle_info():
    mock_response = {
        "Results": [
            {"Variable": "Make", "Value": "HONDA"},
            {"Variable": "Model", "Value": "Civic"},
            {"Variable": "Model Year", "Value": "2021"},
            {"Variable": "Trim", "Value": "Sport"},
        ]
    }
    with patch("services.vin_decoder.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=AsyncMock(
            json=lambda: mock_response, raise_for_status=lambda: None
        ))
        mock_client_cls.return_value = mock_client
        result = await decode_vin("1HGBH41JXMN109186")

    assert result.make == "Honda"
    assert result.model == "Civic"
    assert result.year == "2021"
    assert result.trim == "Sport"


@pytest.mark.asyncio
async def test_decode_vin_handles_empty_results():
    mock_response = {"Results": []}
    with patch("services.vin_decoder.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=AsyncMock(
            json=lambda: mock_response, raise_for_status=lambda: None
        ))
        mock_client_cls.return_value = mock_client
        result = await decode_vin("INVALIDVIN")

    assert result.make == "Unknown"
    assert result.model == "Unknown"
    assert result.year == "Unknown"
