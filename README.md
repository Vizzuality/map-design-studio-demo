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
