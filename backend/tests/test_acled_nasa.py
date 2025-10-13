import pytest
from unittest.mock import AsyncMock, patch
from app.connectors.acled import ACLEDConnector
from app.connectors.nasa_power import NASAPowerConnector


@pytest.mark.asyncio
async def test_acled_connector_transform():
    """Test ACLED data transformation."""
    connector = ACLEDConnector(api_key="test_key", email="test@example.com")
    
    raw_data = {
        "success": True,
        "count": 2,
        "data": [
            {
                "event_id_cnty": "SOM12345",
                "event_date": "2023-06-15",
                "year": 2023,
                "event_type": "Battles",
                "sub_event_type": "Armed clash",
                "actor1": "Government Forces",
                "actor2": "Al-Shabaab",
                "country": "Somalia",
                "iso": 706,
                "region": "Eastern Africa",
                "latitude": 2.0469,
                "longitude": 45.3182,
                "location": "Mogadishu",
                "fatalities": 5,
                "notes": "Clash between forces"
            },
            {
                "event_id_cnty": "SOM12346",
                "event_date": "2023-06-16",
                "year": 2023,
                "event_type": "Violence against civilians",
                "sub_event_type": "Attack",
                "actor1": "Al-Shabaab",
                "actor2": "Civilians",
                "country": "Somalia",
                "iso": 706,
                "region": "Eastern Africa",
                "latitude": 2.1,
                "longitude": 45.4,
                "location": "Kismayo",
                "fatalities": 3,
                "notes": "Attack on civilians"
            }
        ]
    }
    
    transformed = connector.transform_data(raw_data)
    
    assert len(transformed) == 2
    assert transformed[0]["event_id"] == "SOM12345"
    assert transformed[0]["event_type"] == "Battles"
    assert transformed[0]["fatalities"] == 5
    assert transformed[0]["source"] == "ACLED"
    assert transformed[1]["event_type"] == "Violence against civilians"


@pytest.mark.asyncio
async def test_nasa_power_connector_transform():
    """Test NASA POWER data transformation."""
    connector = NASAPowerConnector()
    
    raw_data = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [45.3, 2.0]
        },
        "properties": {
            "parameter": {
                "T2M": {
                    "20230101": 28.5,
                    "20230102": 29.1
                },
                "PRECTOTCORR": {
                    "20230101": 0.0,
                    "20230102": 2.5
                }
            }
        },
        "header": {}
    }
    
    transformed = connector.transform_data(raw_data, latitude=2.0, longitude=45.3)
    
    assert len(transformed) == 2
    assert transformed[0]["date"] == "2023-01-01"
    assert transformed[0]["year"] == 2023
    assert transformed[0]["month"] == 1
    assert transformed[0]["day"] == 1
    assert transformed[0]["latitude"] == 2.0
    assert transformed[0]["longitude"] == 45.3
    assert transformed[0]["t2m"] == 28.5
    assert transformed[0]["prectotcorr"] == 0.0
    assert transformed[0]["source"] == "NASA_POWER"
    assert transformed[1]["prectotcorr"] == 2.5


@pytest.mark.asyncio
async def test_acled_connector_fetch_mock():
    """Test ACLED connector with mocked API call."""
    connector = ACLEDConnector(api_key="test_key", email="test@example.com")
    
    mock_response = {
        "success": True,
        "count": 1,
        "data": [
            {
                "event_id_cnty": "AFG99999",
                "event_date": "2023-07-01",
                "year": 2023,
                "event_type": "Protests",
                "sub_event_type": "Peaceful protest",
                "actor1": "Protesters",
                "actor2": None,
                "country": "Afghanistan",
                "iso": 4,
                "region": "South Asia",
                "latitude": 34.5,
                "longitude": 69.2,
                "location": "Kabul",
                "fatalities": 0,
                "notes": "Peaceful demonstration"
            }
        ]
    }
    
    with patch.object(connector, 'get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        
        result = await connector.fetch_conflict_events(
            country="Afghanistan",
            start_date="2023-07-01",
            end_date="2023-07-31"
        )
        
        assert result["record_count"] == 1
        assert result["data"][0]["country"] == "Afghanistan"
        assert result["data"][0]["event_type"] == "Protests"
        assert result["provenance"]["source"] == "ACLED"


@pytest.mark.asyncio
async def test_nasa_power_connector_fetch_mock():
    """Test NASA POWER connector with mocked API call."""
    connector = NASAPowerConnector()
    
    mock_response = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [45.3, 2.0]},
        "properties": {
            "parameter": {
                "T2M": {"20230601": 30.2, "20230602": 31.5},
                "PRECTOTCORR": {"20230601": 5.0, "20230602": 0.0}
            }
        },
        "header": {}
    }
    
    with patch.object(connector, 'get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        
        result = await connector.fetch_climate_data(
            latitude=2.0,
            longitude=45.3,
            start_date="20230601",
            end_date="20230602"
        )
        
        assert result["record_count"] == 2
        assert result["data"][0]["t2m"] == 30.2
        assert result["data"][1]["prectotcorr"] == 0.0
        assert result["provenance"]["source"] == "NASA_POWER"
