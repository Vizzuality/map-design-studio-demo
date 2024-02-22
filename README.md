Map Design Studio API
==============================

This repository serves as the API for a versatile platform where designers can effortlessly create and style vector and raster map layers.

--------

## Setup

### Configuration

To be able to work, the application will need access to the database. `tipg` uses [Starlette](https://www.starlette.io/config/)'s configuration pattern, which makes use of environment variables or a `.env` file to pass variables to the application.

Example of `.env` file can be found in [.env.example](.env.example).


## Main API Gateway

This is a FastAPI-based API that serves as a gateway to the other services.
It utilizes the [TiTiler](https://developmentseed.org/titiler/) and [TiPg](https://developmentseed.org/tipg/) services to provide a unified API for accessing and styling raster and vector data.

### Local Usage

To start the FastAPI server locally first create the environment with:

``` bash
mamba env create -n map_design_studio_demo -f environment.yml
```

This will create an environment called map-design-studio-demo with a common set of dependencies.

then, to start the FastAPI server locally, run the following command in the terminal under the `src` directory:

```
python -m uvicorn app.main:app
```

### Docker
If you want to run the server within a docker container, you can use the following command to build the docker image and run the container:

```
docker-compose up --build
```

### API Routes Documentation
Once the server is running, you can send HTTP requests to the API endpoints.

   **`/layers` Endpoint**

   - URL: http://localhost:8000/layers
   - Method: GET

   Example Request:

   ```
   curl -X GET -H "Content-Type: application/json" http://localhost:8000/layers
   ```

   Response:
   ```
   [{"id":3,"name":"Country Boundaries","type":"vector","colormap_type":"categorical","url":null,"collection":"public.countries"},{"id":2,"name":"Land Cover","type":"raster","colormap_type":"categorical","url":"../data/raw/raster_data/land_cover.tif","collection":null},{"id":1,"name":"Landscape Capital Index","type":"raster","colormap_type":"continuous","url":"../data/raw/raster_data/final_lci.tif","collection":null}]
   ```

   **`/raster_tiles` Endpoint**

   - URL: http://localhost:8000/raster_tiles
   - Method: GET
   - Request Body: JSON object with the following properties:
     - `id`: ID of the raster dataset
     - `styles`: Dictionary of styles to apply to the raster dataset

   Example Request:

   ```
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
   }' http://localhost:8000/raster_tiles
   ```

   Response:
   ```
   {'url': 'http://127.0.0.1:8000/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?url=..%2Fdata%2Fraw%2Fraster_data%2Fland_cover.tif&bidx=1&colormap=%7B%220%22%3A+%22%231327FE%22%2C+%221%22%3A+%22%230B4614%22%2C+%222%22%3A+%22%230C691B%22%2C+%223%22%3A+%22%2354A51B%22%2C+%224%22%3A+%22%2376D01E%22%2C+%225%22%3A+%22%23DCCF5C%22%2C+%226%22%3A+%22%23B4FE25%22%2C+%227%22%3A+%22%23DADC4D%22%2C+%228%22%3A+%22%23C25045%22%2C+%229%22%3A+%22%23A4A4A4%22%2C+%2210%22%3A+%22%2364FFF8%22%2C+%2211%22%3A+%22%23F9FEA4%22%7D',
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

   - URL: http://localhost:8000/vector_tiles
   - Method: GET
   - Request Body: JSON object with the following properties:
     - `id`: ID of the vector dataset

   Example Request:

   ```
   curl -X GET -H "Content-Type: application/json" -d '{
      "id": 2,
   }' http://localhost:8000/vector_tiles
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

### Demo
To see our project in action, you can run a demo through [this Jupyter notebook](notebooks/03_demo_api.ipynb).
