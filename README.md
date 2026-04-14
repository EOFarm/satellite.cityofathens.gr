# Urban Green Monitoring

# How to use the workflow
actinia workflow for monitoring is in: https://github.com/mundialis/athen_urban-green

## 1. Configuration

### environment variables
Create `.env` with actinia and [CDSE](https://dataspace.copernicus.eu/)
credentials:

```env
ACTINIA_USER=<your_user>
ACTINIA_PW=<your_password>
EODAG_USER=<your_CDSE_user>
EODAG_PW=<your_CDSE_password>
```

**_Do not commit real credentials in `.env`._**

### create collections

### update paths
* to collection in `run_service.py` (STAC_COLLECTION_URL)
* to data storage in `docker-compose.yml` (/home/LOCAL/DIRECTORY:/src/data_tmp)

## 2. Build the image and start containers
The actinia image is pulled and build from [athen_urban_green](https://github.com/mundialis/athen_urban-green)

```bash
docker compose up
```

## Run processing

### Run Service

The script in `athen_urban_green/run_service.py` starts the whole workflow.

From repository root folder:

```bash
python athen_urban_green/run_service.py
```

Important script parameters to adapt before production runs:

- Time range (`START_TIME`, `END_TIME`, or automatic time range mode) for
  filtering Sentinel-2 scenes. Options:
  - autmatic time range mode: Queries given STAC collection for latest item and
    sets `START_TIME` accordingly and `END_TIME` to current time.
- AOI: By default, the script uses a predefined AOI for Athens 
- `TILE_ID`: Sentinel-2 tile identifier e.g. `34SGH` for Athens area
- Max. cloud cover threshold (`MAX_CLOUD_COVER`)
- Actinia base URL, processing endpoint and GRASS location settings
- STAC catalog URL and collection names
- STAC item metadata settings (e.g. collection extent update, item asset
  metadata)

**Note for a local setup**: Adding STAC item to a collection only works if you
have write access to the collection.

Required python depencies for `run_service.py` are:

- `requests`
- `dotenv`
- `jinja2`

## Troubleshooting

- Authentication failures:
  - verify `ACTINIA_USER`, `ACTINIA_PW`, `EODAG_USER`, `EODAG_PW` in
    `docker/.env`.
- No scenes returned:
  - widen time window, increase cloud threshold, verify tile ID and AOI.
- Process polling errors:
  - inspect actinia status URL and container logs for detailed module errors.
