map-design-studio-demo
==============================

This repository serves as a hub for developing a versatile platform where designers can effortlessly create and style vector and raster map layers.

--------

## Setup

### The environment

To run the notebooks you need to create an environment with the dependencies. There are two options:

#### Docker

If you have [docker](https://docs.docker.com/engine/install/) in your system,
you run a jupyter lab server with:

``` bash
docker compose up --build
```

And if you want to get into the container, use a terminal in jupyter lab,
vscode remote development or run this command:

```shell
docker exec -it map_design_studio_demo_notebooks /bin/bash
```

#### Conda environment

Create the environment with:

``` bash
mamba env create -n map_design_studio_demo -f environment.yml
```

This will create an environment called map-design-studio-demo with a common set of dependencies.

### `git` (if needed) and pre-commit hooks

If this project is a new and standalone (not a module in a bigger project), you need to initialize git:

``` bash
git init
```

If the project is already in a git repository, you can skip this step.

To install the **pre-commit hooks**, with the environment activated and in the project root directory, run:

``` bash
pre-commit install
```

## Update the environment

If you need to update the environment installing a new package, you simply do it with:

``` bash
mamba install [package]  # or `pip install [package]` if you want to install it via pip
```

then update the environment.yml file so others can clone your environment with:

``` bash
mamba env export --no-builds -f environment.yml
```
--------

## Services

### Raster Data Service: TiTiler

[TiTiler](https://developmentseed.org/titiler/) is a set of **Python** modules that focus on creating FastAPI applications for dynamic tiling. It is used for serving and styling raster data.

#### Installation

To install from PyPI and run, make sure you have pip up to date:

```bash
python -m pip install -U pip
```
Then, install the desired TiTiler packages:
```bash
python -m pip install titiler.{package}
```
For example:
```bash
python -m pip install titiler.core
python -m pip install titiler.extensions
python -m pip install titiler.mosaic
python -m pip install titiler.application # also installs core, extensions and mosaic
```

#### Launch

Install uvicorn to run the FastAPI application locally:
```bash
python -m pip install uvicorn
```
Launch the application locally:
```bash
uvicorn titiler.application.main:app
```

Alternativelly, you can create a [create a FastAPI router](https://developmentseed.org/titiler/advanced/tiler_factories/) (`fastapi.APIRouter`) with a minimal set of endpoints.

You can run our custom app with:
```bash
python titiler_app.py
```

### Vector Data Service: TiPg

[TiPg](https://developmentseed.org/tipg/) is a **Python** package that helps create lightweight Open Geospatial Consortium (OGC) [Features](https://ogcapi.ogc.org/features/) and [Tiles](https://ogcapi.ogc.org/tiles/) API with a PostGIS Database backend. It is used for serving and styling vector data.

#### Installation

To install, first update pip:
```bash
python -m pip install pip -U
```
Then, install the TiPg package:
```bash
python -m pip install tipg
```

#### Configuration

To be able to work, the application will need access to the database. `tipg` uses [Starlette](https://www.starlette.io/config/)'s configuration pattern, which makes use of environment variables or a `.env` file to pass variables to the application.

A example `.env` would look like this:
```bash
DATABASE_URL=postgresql://username:password@0.0.0.0:5432/postgis
```

#### Launch

Install uvicorn:
```bash
pip install uvicorn
```

Launch the application:
```bash
uvicorn tipg.main:app
```

### Main API Gateway: FastAPI

This is a FastAPI-based API that serves as a gateway to the other services.
It utilizes the TiTiler and TiPg services to provide a unified API for accessing and styling raster and vector data.

1. To start the FastAPI server, use the following command:

```
python main.py
```

2. Once the server is running, you can send HTTP requests to the API endpoints.

   **`/raster_tiles` Endpoint**

   - URL: http://localhost:8088/raster_tiles
   - Method: GET
   - Request Body: JSON object with the following properties:
     - `id`: ID of the raster dataset
     - `styles`: Dictionary of styles to apply to the raster dataset

   Example Request:

      ```commandline
      curl -X GET -H "Content-Type: application/json" -d '{
        "id": 2,
        "styles": {
            "0": "#1327FE",
            "1": "#0B4614",
            "2": "#0C691B",
            "3": "#54A51B",
            "4": "#76D01E",
            "5": "#DCCF5C",
            "6": "#B4FE25",
            "7": "#DADC4D",
            "8": "#C25045",
            "9": "#A4A4A4",
            "10": "#64FFF8",
            "11": "#F9FEA4"
            }
      }' http://localhost:8088/raster_tiles
      ```

   Response:
   ```
   {'url': 'http://127.0.0.1:8080/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?url=..%2Fdata%2Fraw%2Fraster_data%2Fland_cover.tif&bidx=1&colormap=%7B%220%22%3A+%22%231327FE%22%2C+%221%22%3A+%22%230B4614%22%2C+%222%22%3A+%22%230C691B%22%2C+%223%22%3A+%22%2354A51B%22%2C+%224%22%3A+%22%2376D01E%22%2C+%225%22%3A+%22%23DCCF5C%22%2C+%226%22%3A+%22%23B4FE25%22%2C+%227%22%3A+%22%23DADC4D%22%2C+%228%22%3A+%22%23C25045%22%2C+%229%22%3A+%22%23A4A4A4%22%2C+%2210%22%3A+%22%2364FFF8%22%2C+%2211%22%3A+%22%23F9FEA4%22%7D',
    'info': {'name': 'Land Cover',
     'type': 'raster',
     'colormap_type': 'categorical',
     'path': '../data/raw/raster_data/land_cover.tif',
     'styles': {'0': '#1327FE',
      '1': '#0B4614',
      '2': '#0C691B',
      '3': '#54A51B',
      '4': '#76D01E',
      '5': '#DCCF5C',
      '6': '#B4FE25',
      '7': '#DADC4D',
      '8': '#C25045',
      '9': '#A4A4A4',
      '10': '#64FFF8',
      '11': '#F9FEA4'}}}
   ```
   **`/vector_tiles` Endpoint**

   - URL: http://localhost:8088/vector_tiles
   - Method: GET
   - Request Body: JSON object with the following properties:
     - `id`: ID of the raster dataset

   Example Request:

      ```commandline
      curl -X GET -H "Content-Type: application/json" -d '{
        "id": 2,
      }' http://localhost:8088/vector_tiles
      ```

   Response:

      ```
      {'url': 'http://127.0.0.1:8000/collections/public.countries/tiles/WebMercatorQuad/{z}/{x}/{y}',
       'layer_name': 'default',
       'info': {'name': 'Country Boundaries',
        'type': 'vector',
        'colormap_type': 'categorical',
        'collection': 'public.countries',
        'styles': None}}
      ```
