# Data Sources Guide

## Overview
This document provides comprehensive information about all free data sources, APIs, and datasets used in the Migration Forecasting System.

---

## 1. Migration & Displacement Data

### 1.1 UNHCR Refugee Statistics API
**Provider**: United Nations High Commissioner for Refugees  
**Access**: Free, Open API (No API key required)  
**Base URL**: `https://api.unhcr.org/`  
**Documentation**: https://api.unhcr.org/docs/refugee-statistics.html  

**Available Endpoints:**
- `/population` - Refugee and asylum-seeker populations by country/region
- `/demographics` - Age, gender, and demographic breakdowns
- `/asylumApplications` - Asylum application statistics
- `/asylumDecisions` - Decision outcomes on asylum claims
- `/solutions` - Durable solutions (resettlement, return, integration)
- `/idmc` - Internal Displacement Monitoring Centre data

**Rate Limits**: Not publicly specified (reasonable use expected)  
**Data Format**: JSON, XML  
**Update Frequency**: Annually (mid-year updates)  
**Historical Coverage**: 1951-present

**Example Request:**
```python
import requests

# Get population data for all countries in 2023
url = "https://api.unhcr.org/population/v1/population/"
params = {
    "year": 2023,
    "limit": 1000
}
response = requests.get(url, params=params)
data = response.json()
```

**Key Metrics Available:**
- Refugees under UNHCR mandate
- Asylum-seekers
- Internally displaced persons (IDPs)
- Returnees
- Stateless persons
- Host community populations

---

### 1.2 UNHCR Operational Data Portal
**Provider**: UNHCR  
**Access**: Free, Web-based + Data exports  
**Portal**: https://data.unhcr.org/  

**Features:**
- Real-time emergency response data
- Regional situation dashboards
- Operational updates from field offices
- Downloadable datasets (CSV, Excel, JSON)

**Use Cases:**
- Recent crisis monitoring
- Emergency response planning
- Regional flow analysis

---

### 1.3 IDMC Global Internal Displacement Database
**Provider**: Internal Displacement Monitoring Centre  
**Access**: Free API and bulk downloads  
**Website**: https://www.internal-displacement.org/database/api  
**API Documentation**: https://api.internal-displacement.org/  

**Data Coverage:**
- Conflict-induced displacement
- Disaster-induced displacement
- Country-level estimates
- Subnational data (where available)

**Update Frequency**: Real-time for disasters, periodic for conflict

---

## 2. Conflict & Security Data

### 2.1 ACLED (Armed Conflict Location & Event Data Project)
**Provider**: ACLED  
**Access**: Free tier available (requires registration)  
**Base URL**: `https://api.acleddata.com/`  
**Registration**: https://developer.acleddata.com/  

**Free Tier Limits:**
- Academic/Research use: Full access with attribution
- Commercial: Limited (contact for pricing)
- Rate limit: 10 requests/minute

**Data Export Tool**: https://acleddata.com/data-export-tool/  

**Event Types Covered:**
- Battles
- Violence against civilians
- Protests and riots
- Strategic developments
- Remote violence (drones, IEDs)

**Geographic Coverage**: 
- Africa (1997-present)
- Middle East (2017-present)
- South Asia, Southeast Asia (2010-present)
- Latin America & Caribbean (2018-present)
- Europe (2018-present)
- United States (2020-present)

**Key Variables:**
- Event date and location (geocoded)
- Actor information (armed groups, governments, protesters)
- Fatality estimates
- Event descriptions

**Example Request:**
```python
import requests

# ACLED Data Export API
url = "https://api.acleddata.com/acled/read"
params = {
    "key": "YOUR_API_KEY",
    "email": "YOUR_EMAIL",
    "country": "Somalia",
    "event_date": "2023-01-01|2023-12-31",
    "event_date_where": "BETWEEN"
}
response = requests.get(url, params=params)
data = response.json()
```

---

### 2.2 GDELT (Global Database of Events, Language, and Tone)
**Provider**: GDELT Project  
**Access**: Free, Open Access  
**Base URL**: https://api.gdeltproject.org/  
**Documentation**: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/  

**Data Streams:**
- GDELT Events: 300+ categories of human activity
- Global Knowledge Graph (GKG): Entity recognition, themes, locations
- TV & Online News Archive
- Visual Global Entity Graph: Image analysis

**Coverage:**
- Real-time global news monitoring
- 65+ languages
- 100+ countries
- Updated every 15 minutes

**Access Methods:**
- BigQuery (Google Cloud): Free tier available
- File downloads: Daily/historical files
- API queries: Via GDELT Doc API

**Example BigQuery:**
```sql
SELECT 
  SQLDATE, Actor1Name, Actor2Name, EventCode, NumMentions, 
  ActionGeo_Lat, ActionGeo_Long
FROM `gdelt-bq.gdeltv2.events`
WHERE SQLDATE >= 20230101 AND SQLDATE <= 20231231
  AND EventRootCode = '19'  -- 'Fight' events
LIMIT 1000
```

**Key Use Cases:**
- Early warning signals
- Sentiment analysis
- Media coverage tracking
- Conflict escalation monitoring

---

## 3. Population & Demographics

### 3.1 WorldPop
**Provider**: University of Southampton  
**Access**: Free, Open Access  
**API**: https://www.worldpop.org/sdi/introapi/  
**Data Access**: https://www.worldpop.org/geodata/listing  

**Available Datasets:**
- Population counts and density (100m resolution)
- Age and sex structures
- Population projections (2020-2030)
- Migration flows (select countries)
- Birth and death rates
- Poverty mapping

**API Services:**
- `stats`: Population totals for areas of interest
- `sample`: Random spatial sampling
- Direct file downloads via FTP

**Resolution**: 100m x 100m grid cells  
**Coverage**: Global  
**Update**: Annual releases

**Example API Request:**
```python
# Get population stats for a specific area
import requests

url = "https://www.worldpop.org/rest/data/pop/wpgp"
params = {
    "iso3": "SOM",  # Somalia ISO code
    "year": 2020
}
response = requests.get(url, params=params)
```

**Data Formats:**
- GeoTIFF (raster)
- CSV (tabular)
- Shapefiles (vector)

---

### 3.2 UN Population Division Data
**Provider**: United Nations DESA  
**Access**: Free API and bulk downloads  
**API**: https://population.un.org/dataportal/about/dataapi  

**Available Data:**
- World Population Prospects
- International migrant stock
- Urban/rural populations
- Fertility and mortality indicators

---

## 4. Climate & Environmental Data

### 4.1 NASA Earth Observing System Data and Information System (EOSDIS)
**Provider**: NASA  
**Access**: Free (requires free Earthdata account)  
**Portal**: https://earthdata.nasa.gov/  
**Registration**: https://urs.earthdata.nasa.gov/  

**Key Datasets:**
- **MODIS**: Land cover, vegetation indices, fire detection
- **GPM**: Global Precipitation Measurement
- **GRACE**: Groundwater storage changes
- **SMAP**: Soil moisture
- **OMI**: Air quality indicators

**Access Methods:**
- Direct download from Earthdata Search
- OPeNDAP for programmatic access
- NASA POWER API (see below)

---

### 4.2 NASA POWER (Prediction Of Worldwide Energy Resources)
**Provider**: NASA  
**Access**: Free, Open API  
**Base URL**: https://power.larc.nasa.gov/api/  
**Documentation**: https://power.larc.nasa.gov/docs/  

**No API Key Required**

**Available Parameters:**
- Temperature (min, max, average)
- Precipitation
- Humidity
- Solar radiation
- Wind speed
- Evapotranspiration

**Temporal Coverage**: 1981-present (near real-time)  
**Spatial Resolution**: 0.5° x 0.5° (≈55km at equator)

**Example Request:**
```python
import requests

# Get temperature and precipitation for a location
url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "T2M,PRECTOTCORR",  # Temperature, Precipitation
    "community": "AG",
    "longitude": 45.3,
    "latitude": 2.0,
    "start": "20230101",
    "end": "20231231",
    "format": "JSON"
}
response = requests.get(url, params=params)
data = response.json()
```

---

### 4.3 NOAA Climate Data Online (CDO)
**Provider**: National Oceanic and Atmospheric Administration  
**Access**: Free (API key required)  
**Base URL**: `https://www.ncdc.noaa.gov/cdo-web/api/v2/`  
**API Token**: https://www.ncdc.noaa.gov/cdo-web/token  

**Rate Limit**: 1000 requests per day

**Available Datasets:**
- Global Historical Climatology Network (GHCN)
- Integrated Surface Database (ISD)
- Severe weather data
- Climate normals

**Example Request:**
```python
import requests

headers = {"token": "YOUR_NOAA_TOKEN"}
url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
params = {
    "datasetid": "GHCND",
    "locationid": "FIPS:SO",  # Somalia
    "startdate": "2023-01-01",
    "enddate": "2023-12-31",
    "units": "metric",
    "limit": 1000
}
response = requests.get(url, headers=headers, params=params)
```

---

### 4.4 Copernicus Climate Data Store
**Provider**: European Union Copernicus Programme  
**Access**: Free (registration required)  
**Portal**: https://cds.climate.copernicus.eu/  
**API**: CDS API (Python client available)

**Key Datasets:**
- ERA5 Reanalysis (hourly climate data)
- Seasonal forecasts
- Climate projections
- Drought indicators
- Fire danger indices

**Installation:**
```bash
pip install cdsapi
```

---

### 4.5 Sentinel Satellite Imagery
**Provider**: European Space Agency (ESA)  
**Access**: Free  
**Portal**: https://scihub.copernicus.eu/  
**API**: Copernicus Open Access Hub  

**Satellites:**
- **Sentinel-1**: Radar imagery (all-weather)
- **Sentinel-2**: Optical imagery (10m resolution)
- **Sentinel-3**: Ocean and land monitoring
- **Sentinel-5P**: Atmospheric monitoring

**Access Methods:**
- Copernicus Open Access Hub API
- Google Earth Engine (free for research)
- AWS Open Data (requester pays)

**Use Cases:**
- Land use change detection
- Flood monitoring
- Agricultural assessment
- Urban expansion tracking

---

### 4.6 Landsat (USGS)
**Provider**: USGS/NASA  
**Access**: Free  
**Portal**: https://earthexplorer.usgs.gov/  
**API**: USGS Machine-to-Machine (M2M) API

**Resolution**: 30m (multispectral), 15m (panchromatic)  
**Temporal Coverage**: 1972-present (Landsat 1-9)  
**Revisit Time**: 8 days (combined Landsat 8 & 9)

---

## 5. Economic Indicators

### 5.1 World Bank Indicators API
**Provider**: World Bank  
**Access**: Free, Open API (no authentication required)  
**Base URL**: `https://api.worldbank.org/v2/`  
**Documentation**: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392  

**Key Indicator Categories:**
- GDP and economic growth
- Poverty and inequality
- Employment and labor force
- Trade and finance
- Agriculture and food security
- Infrastructure
- Education and health expenditure

**Popular Indicators for Migration Forecasting:**
- `NY.GDP.PCAP.CD` - GDP per capita
- `SI.POV.DDAY` - Poverty headcount ratio at $2.15/day
- `SL.UEM.TOTL.ZS` - Unemployment rate
- `FP.CPI.TOTL.ZG` - Inflation rate
- `MS.MIL.XPND.GD.ZS` - Military expenditure (% of GDP)
- `AG.LND.PRCP.MM` - Average precipitation

**Example Request:**
```python
import requests

# Get GDP per capita for Somalia (2015-2023)
url = "https://api.worldbank.org/v2/country/SOM/indicator/NY.GDP.PCAP.CD"
params = {
    "date": "2015:2023",
    "format": "json",
    "per_page": 100
}
response = requests.get(url, params=params)
data = response.json()
```

**Response Format**: JSON or XML  
**Rate Limits**: None (reasonable use expected)

---

### 5.2 IMF Data API
**Provider**: International Monetary Fund  
**Access**: Free  
**API**: https://data.imf.org/  
**Documentation**: https://datahelp.imf.org/knowledgebase/articles/667681-using-json-restful-web-service  

**Key Datasets:**
- International Financial Statistics (IFS)
- Direction of Trade Statistics (DOTS)
- Balance of Payments (BOP)
- Government Finance Statistics (GFS)

---

### 5.3 FAOSTAT (Food and Agriculture Organization)
**Provider**: UN FAO  
**Access**: Free API and bulk downloads  
**API**: https://www.fao.org/faostat/en/#data  
**Bulk Download**: https://fenixservices.fao.org/faostat/api/  

**Data Categories:**
- Food security indicators
- Crop production and prices
- Land use
- Agricultural trade
- Food balance sheets

---

## 6. Social & Humanitarian Indicators

### 6.1 HDX (Humanitarian Data Exchange)
**Provider**: OCHA (UN Office for Coordination of Humanitarian Affairs)  
**Access**: Free  
**Portal**: https://data.humdata.org/  
**API**: https://hdx-hapi.readthedocs.io/  

**HAPI (Humanitarian API):**
- Population statistics
- Humanitarian needs
- Food security
- Conflict events
- Funding data
- 3W (Who does What Where)

**Geographic Coverage**: 250+ countries/territories  
**Update Frequency**: Varies by dataset

---

### 6.2 INFORM Risk Index
**Provider**: European Commission / Inter-Agency Standing Committee  
**Access**: Free downloads  
**Portal**: https://drmkc.jrc.ec.europa.eu/inform-index  

**Components:**
- Hazard & Exposure
- Vulnerability
- Lack of Coping Capacity

**Use Case**: Pre-crisis risk assessment for displacement

---

## 7. Social Media & News (Alternative Data)

### 7.1 Twitter/X Academic Research API
**Provider**: X Corp (formerly Twitter)  
**Access**: Free for academic research (application required)  
**Application**: https://developer.twitter.com/en/products/twitter-api/academic-research  

**Academic Track Benefits:**
- 10 million tweets per month
- Full archive search (2006-present)
- Enhanced filtering and metadata

**Note**: Approval process required. Alternative: use pre-collected datasets or GDELT for news sentiment.

---

### 7.2 Reddit API (PRAW)
**Provider**: Reddit  
**Access**: Free (OAuth authentication)  
**Documentation**: https://www.reddit.com/dev/api/  
**Python Library**: PRAW (Python Reddit API Wrapper)

**Rate Limits**: 60 requests per minute

**Use Cases:**
- Community sentiment analysis
- Discussion topic modeling
- Early warning signals from affected populations

---

## 8. Geospatial Administrative Boundaries

### 8.1 Natural Earth
**Provider**: Open source collaboration  
**Access**: Free, Public Domain  
**Website**: https://www.naturalearthdata.com/  

**Available Data:**
- Country boundaries (1:10m, 1:50m, 1:110m scale)
- Admin-1 (states/provinces)
- Populated places
- Geographic features

**Format**: Shapefiles, GeoJSON

---

### 8.2 GADM (Database of Global Administrative Areas)
**Provider**: GADM  
**Access**: Free for non-commercial use  
**Website**: https://gadm.org/  

**Administrative Levels**: Up to 5 levels (country to village)  
**Format**: Shapefiles, GeoPackage, R (sf)

---

### 8.3 OpenStreetMap
**Provider**: OpenStreetMap Foundation  
**Access**: Free, Open Data  
**API**: Overpass API  
**Documentation**: https://wiki.openstreetmap.org/wiki/API  

**Use Cases:**
- Road networks for accessibility analysis
- Points of interest (hospitals, schools, camps)
- Building footprints
- Refugee camp mapping

---

## 9. Health & Disease Data

### 9.1 WHO Global Health Observatory
**Provider**: World Health Organization  
**Access**: Free API  
**Base URL**: https://ghoapi.azureedge.net/api/  
**Documentation**: https://www.who.int/data/gho/info/gho-odata-api  

**Key Indicators:**
- Disease surveillance
- Health infrastructure
- Vaccination coverage
- Maternal and child health

---

### 9.2 EM-DAT (Emergency Events Database)
**Provider**: CRED (Centre for Research on Epidemiology of Disasters)  
**Access**: Free registration required  
**Portal**: https://www.emdat.be/  

**Coverage:**
- Natural disasters (floods, droughts, earthquakes, etc.)
- Technological disasters
- Biological disasters (epidemics)

**Time Range**: 1900-present

---

## 10. Additional Resources

### 10.1 Google Earth Engine
**Platform**: Google Cloud  
**Access**: Free for research and education  
**Sign up**: https://earthengine.google.com/  

**Data Catalog**: 50+ petabytes including:
- All Landsat and Sentinel imagery
- Climate reanalysis datasets
- Population density
- Night lights
- Land cover classifications

**API**: JavaScript and Python APIs available

---

### 10.2 World Resources Institute (WRI) Data
**Provider**: WRI  
**Access**: Free  
**Platforms**:
- Global Forest Watch: https://www.globalforestwatch.org/
- Resource Watch: https://resourcewatch.org/
- Aqueduct Water Risk Atlas: https://www.wri.org/aqueduct

---

## Data Integration Strategy

### Priority Tier 1 (Essential):
1. UNHCR Refugee Statistics API
2. ACLED Conflict Data
3. WorldPop Population Grids
4. World Bank Indicators API
5. NASA POWER Climate Data

### Priority Tier 2 (Important):
6. GDELT Global Events
7. HDX Humanitarian Data
8. Sentinel-2 Satellite Imagery
9. NOAA Climate Data
10. GADM Administrative Boundaries

### Priority Tier 3 (Enrichment):
11. IDMC Displacement Data
12. EM-DAT Disaster Events
13. WHO Health Indicators
14. FAO Food Security
15. Social media sentiment (if available)

---

## Data Quality & Limitations

### Known Issues:
1. **ACLED**: May have reporting bias in areas with limited media coverage
2. **GDELT**: High false-positive rate; requires extensive filtering
3. **Social Media**: Platform API restrictions increasing; consider alternatives
4. **Satellite Imagery**: Processing requires significant computational resources
5. **WorldPop**: Model-based estimates; actual accuracy varies by region

### Best Practices:
- Always validate data against multiple sources
- Implement outlier detection and anomaly flags
- Track data provenance and version control
- Set up automated data quality checks
- Monitor API health and implement fallback mechanisms

---

## Rate Limits Summary

| Data Source | Rate Limit | Authentication |
|-------------|-----------|----------------|
| UNHCR API | Unspecified (reasonable use) | None |
| ACLED | 10 req/min (free tier) | API Key |
| World Bank | No hard limit | None |
| NASA POWER | No hard limit | None |
| NOAA CDO | 1000 req/day | Token |
| GDELT | Query size limits | None (BigQuery) |
| WorldPop | Unspecified | None |
| Twitter Academic | 10M tweets/month | OAuth |
| Reddit | 60 req/min | OAuth |

---

## Update Frequencies

| Data Source | Update Frequency |
|-------------|------------------|
| UNHCR Population | Annual |
| ACLED Events | Daily |
| GDELT | Every 15 minutes |
| NASA POWER | Daily (1-2 day lag) |
| Sentinel-2 | 5-day revisit |
| World Bank | Annual (most indicators) |
| WorldPop | Annual |
| NOAA Climate | Daily to monthly |

---

## Next Steps

1. **Set up API credentials** for services requiring authentication
2. **Test API connections** with sample requests
3. **Design data ingestion pipeline** with scheduled updates
4. **Implement caching strategy** to minimize API calls
5. **Set up monitoring** for API health and data quality
6. **Create data documentation** for internal feature catalog

---

**Last Updated**: 2025-10-13  
**Maintained By**: Development Team  
**Questions?** Open an issue or contact the data team
