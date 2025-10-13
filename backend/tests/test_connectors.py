import pytest
from unittest.mock import AsyncMock, patch
from app.connectors.unhcr import UNHCRConnector
from app.connectors.worldbank import WorldBankConnector


@pytest.mark.asyncio
async def test_unhcr_connector_transform():
    """Test UNHCR data transformation."""
    connector = UNHCRConnector()
    
    raw_data = {
        "items": [
            {
                "year": 2023,
                "coo_name": "Afghanistan",
                "coo_iso": "AFG",
                "coa_name": "Pakistan",
                "coa_iso": "PAK",
                "refugees": 1500000,
                "asylum_seekers": 50000,
                "idps": 0,
                "returnees": 0,
                "stateless": 0
            }
        ]
    }
    
    transformed = connector.transform_data(raw_data)
    
    assert len(transformed) == 1
    assert transformed[0]["country_of_origin"] == "Afghanistan"
    assert transformed[0]["country_of_origin_iso"] == "AFG"
    assert transformed[0]["refugees"] == 1500000
    assert transformed[0]["source"] == "UNHCR"


@pytest.mark.asyncio
async def test_worldbank_connector_transform():
    """Test World Bank data transformation."""
    connector = WorldBankConnector()
    
    raw_data = [
        {"page": 1, "pages": 1, "per_page": 500, "total": 2},
        [
            {
                "indicator": {"id": "NY.GDP.PCAP.CD", "value": "GDP per capita"},
                "country": {"id": "SOM", "value": "Somalia"},
                "countryiso3code": "SOM",
                "date": "2023",
                "value": 450.5,
                "unit": ""
            },
            {
                "indicator": {"id": "NY.GDP.PCAP.CD", "value": "GDP per capita"},
                "country": {"id": "SOM", "value": "Somalia"},
                "countryiso3code": "SOM",
                "date": "2022",
                "value": 420.3,
                "unit": ""
            }
        ]
    ]
    
    transformed = connector.transform_data(raw_data, "NY.GDP.PCAP.CD")
    
    assert len(transformed) == 2
    assert transformed[0]["country_iso"] == "SOM"
    assert transformed[0]["indicator_code"] == "NY.GDP.PCAP.CD"
    assert transformed[0]["year"] == 2023
    assert transformed[0]["value"] == 450.5
    assert transformed[0]["source"] == "WorldBank"


@pytest.mark.asyncio
async def test_unhcr_connector_fetch_mock():
    """Test UNHCR connector with mocked API call."""
    connector = UNHCRConnector()
    
    mock_response = {
        "items": [
            {
                "year": 2023,
                "coo_name": "Syria",
                "coo_iso": "SYR",
                "coa_name": "Turkey",
                "coa_iso": "TUR",
                "refugees": 3500000,
                "asylum_seekers": 100000,
                "idps": 0,
                "returnees": 0,
                "stateless": 0
            }
        ]
    }
    
    with patch.object(connector, 'get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        
        result = await connector.fetch_population_data(year=2023, country_code="SYR")
        
        assert result["record_count"] == 1
        assert result["data"][0]["country_of_origin_iso"] == "SYR"
        assert result["provenance"]["source"] == "UNHCR"


@pytest.mark.asyncio
async def test_worldbank_connector_fetch_mock():
    """Test World Bank connector with mocked API call."""
    connector = WorldBankConnector()
    
    mock_response = [
        {"page": 1, "pages": 1, "per_page": 500, "total": 1},
        [
            {
                "indicator": {"id": "NY.GDP.PCAP.CD", "value": "GDP per capita"},
                "country": {"id": "AFG", "value": "Afghanistan"},
                "countryiso3code": "AFG",
                "date": "2023",
                "value": 350.0,
                "unit": ""
            }
        ]
    ]
    
    with patch.object(connector, 'get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        
        result = await connector.fetch_indicator(
            country_code="AFG",
            indicator_code="NY.GDP.PCAP.CD",
            start_year=2023,
            end_year=2023
        )
        
        assert result["record_count"] == 1
        assert result["data"][0]["country_iso"] == "AFG"
        assert result["data"][0]["value"] == 350.0
