# Urban Green Monitoring

This folder contains the start and configuration script (`run_service.py`) for 
an [actinia](https://github.com/actinia-org) workflow for urban green monitoring.
It is designed to be used with the actinia image from the [athen_urban_green](https://github.com/mundialis/athen_urban-green) 
repository. Additionally the actinia process chain templates (as [jinja2](https://jinja.palletsprojects.com/en/stable/)) 
for the workflow are located in the `athen_urban_green/templates` folder.

The main output are NDVI, NDWI and categorized versions of these indices. All 
of these are published as STAC items.

## Output data

The main output layers are exported as Cloud Optimized GeoTIFFs (COG) and published as STAC items in the defined STAC catalog and collections:

- NDVI (Normalized Difference Vegetation Index)
- Categorized NDVI
- NDWI (Normalized Difference Water Index) 
- Categorized NDWI

The export directory of the COGs is defined as mounted directory in the `./docker-compose.yml` for the actinia container (`/DATA/DIRECTORY:/src/export_dir`).

Categorization thresholds for NDVI and NDWI are defined in [athen_urban_green](https://github.com/mundialis/athen_urban-green).

Used index equations:
- NDVI = (NIR - Red) / (NIR + Red)
- NDWI = (( NIR - SWIR ) / ( NIR + SWIR ))

NDVI classes (raster values in brackets):
- no vegetation (1): -1 to 0.1
- bare soil (2): 0.1 to 0.2
- sparse/stressed vegetation (3): 0.2 to 0.5
- dense/healthy vegetation (4): 0.5 to 1.0

NDWI classes (raster values in brackets):
- barren (1): -1 to -0.1
- water stress (2): 0.1 to 0.4
- no water stress (3): 0.4 to 1.0

## How to use the workflow

A detailed description of the actinia workflow for urban green monitoring can be 
found in the [athen_urban_green](https://github.com/mundialis/athen_urban-green/blob/main/README.md) repository.

### 1. Configuration

#### Environment variables
Credetentials for actinia and for an existing [CDSE](https://dataspace.copernicus.eu/) 
account need to be added to the `.env` file. The credentials for actinia can be 
chosen freely, as the user is created during container startup.

```env
ACTINIA_USER=<your_user>
ACTINIA_PW=<your_password>
EODAG_USER=<your_CDSE_user>
EODAG_PW=<your_CDSE_password>
```

**_Do not commit real credentials in `.env`._**

### 2. Building image and start containers

The actinia image is pulled and build from [athen_urban_green](https://github.com/mundialis/athen_urban-green). 
Start whole setup with:

```bash
docker compose up
```

### 3. Start Urban-Green-Monitoring service

The script in `athen_urban_green/run_service.py` starts the whole workflow.

From repository root folder:

```bash
python athen_urban_green/run_service.py
```

**Required** python dependencies for `run_service.py` are:

- `requests`
- `dotenv`
- `jinja2`

#### Create STAC collections

In order to be able to register the created STAC items, the STAC collections 
defined in `STAC_COLLECTIONS` need to exist in the STAC catalog defined in 
`STAC_CATALOG_URL`. 


#### Script parameters

Important script parameters to adapt before production runs:

**Sentinel-2 query parameters:**

- Time range (`START_TIME`, `END_TIME`, or automatic time range mode) for
  filtering Sentinel-2 scenes. 

  **Options:**  
  1. **manual time range:** Set `START_TIME` and `END_TIME` e.g. `START_TIME = "2026-04-05"` 
  and `END_TIME = "2026-04-10"`
  2. **automatic time range:** Queries given STAC collection `STAC_COLLECTION_URL` 
  for latest item and
    sets `START_TIME` accordingly and `END_TIME` to current time. For the 
    current settings, the collection `ndvi-ath` is used which is updated with 
    each workflow run. Check with names defined in `STAC_COLLECTIONS`.
- `TILE_ID`: Sentinel-2 tile identifier (MGRS tile id)  e.g. `34SGH` for Athens area
- `MAX_CLOUD_COVER`: Max. cloud cover threshold
- AOI: The workflow uses a predefined AOI for Athens (it is defined in 
[athen_urban_green](https://github.com/mundialis/athen_urban-green/tree/main/processing/input/aoi) 
by a geojson file, it can be changed if needed).


**actinia process parameters:**

It should not be necessary to change these parameters. To be able to reach 
actinia a correct actinia base URL (`ACTINIA_BASE_URL`) is required. The default
 of this setup is `http://localhost:8088/`.

**STAC parameters:**

- `STAC_CATALOG_URL`: Should link to the STAC catalog `"http://pycsw:8000/stac/"`
- `STAC_COLLECTIONS`: Names of the STAC collections, where the created items are
 registered.  
 For this workflow four collections for each product are used: 
 `"ndvi-ath,ndvi-cat-ath,ndwi-ath,ndwi-cat-ath"`
- `PRODUCT_NAMES`: Names used for the STAC items of the four products (same 
order as `STAC_COLLECTIONS`): `"NDVI,NDVI_categorized,NDWI,NDWI_categorized"`
- `STAC_ITEM_ID_PREFIX`: Defines a prefix for the STAC item IDs: e.g. 
`"athen_urban_green"` so the STAC item ID will be like this
`athen_urban_green_NDWI_categorized_20260218T091031` 
`STAC_ITEM_TITLE`: Title for STAC item. Additionally, product name and date are 
added to the title. E.g. `Urban Green Monitoring Athens- NDWI_categorized - 2026-02-18 09:10:31+00:00`
`STAC_ITEM_DESCRIPTION`: Description for STAC item. Currently it is the same 
text for all products.
 

## Troubleshooting

- Authentication failures:
  - verify `ACTINIA_USER`, `ACTINIA_PW`, `EODAG_USER`, `EODAG_PW` in
    `.env`.
- No scenes returned:
  - widen time window, increase cloud threshold or verify tile ID and AOI.
- Process polling errors:
  - inspect actinia status URL and container logs for detailed module errors.
- If STAC item already exists, the workflow currently fails. As it is designed 
for regular updates, it is expected that the same item is not created twice. 