# [GeoVisio](https://gitlab.com/geovisio/api) Command Line Interface (cli)

![GeoVisio logo](https://gitlab.com/geovisio/api/-/raw/develop/images/logo_full.png)

Command Line Interface tool to interact with a [Geovisio](https://gitlab.com/geovisio/api) instance.

[[_TOC_]]


## Features

This tool allows you to:

- Upload a sequence of pictures on a GeoVisio API

It is under __heavy development__, new features will appear in a near future 😉


## Install

GeoVisio CLI can be installed using two methods:

- From [PyPI](https://pypi.org/project/geovisio_cli/), the Python central package repository
- Using this [Git repository](https://gitlab.com/geovisio/cli)

### From PyPI

Just launch this command:

```bash
pip install geovisio_cli
```

After this you should be able to use the CLI tool with the name `geovisio`:

```bash
geovisio --help
```

Alternatively, you can use [pipx](https://github.com/pypa/pipx) if you want all the script dependencies to be in a custom virtual env.

You need to [install pipx](https://pypa.github.io/pipx/installation/), then:

```bash
pipx install geovisio_cli
```

### From Git repository

Download the repository:

```bash
git clone https://gitlab.com/geovisio/cli.git geovisio_cli
cd geovisio_cli/
```

To avoid conflicts, it's considered a good practice to create a _[virtual environment](https://docs.python.org/3/library/venv.html)_ (or virtualenv). To do so, launch the following commands:

```bash
# Create the virtual environment in a folder named "env"
python3 -m venv env

# Launches utilities to make environment available in your Bash
source ./env/bin/activate
```

Then, install the GeoVisio CLI dependencies using pip:

```bash
pip install -e .
```

You can also install the `dev` dependencies if necessary (to have lints, format, tests, ...):

```bash
pip install -e .[dev]
```

Then, you can use the `geovisio` command:
```bash
geovisio --help
```


## Usage

All details of available commands are listed in [USAGE.md](./USAGE.md) documentation.

### Upload pictures

The picture upload command is available under the `upload` subcommand:

```bash
geovisio upload --help
```

If you want to upload pictures from a `my_sequence` directory to a GeoVisio instance (running locally in this example), launch this command:

```bash
geovisio upload --path ./my_sequence --api-url http://localhost:5000/
```

You can also add a `--wait` flag to wait for geovisio to process all the pictures.

#### Authentication

If the GeoVisio API requires a login for the upload, the user/password can either be set:
* with command-line arguments (`--user` / `--password`)
* with environment variables (`GEOVISIO_USER` / `GEOVISIO_PASSWORD`)

If no information is set but required by the GeoVisio instance, they will be asked interactively. This is the best way to enter the password so it will not be stored in the command-line history.

Note: the password is not stored, and sent directly to geovisio. If the future, this will be removed in favor of API keys when geovisio will support those.

### Collection status

Prints the status of a collection.

```bash
geovisio collection-status --id <some collection id> --api-url http://localhost:5000
```

You can alternatively give the location of the sequence (its full url) like:

```bash
geovisio collection-status --location http://localhost:5000/api/collections/dae288b2-9e8d-4896-af39-d35ce6bc9d4e
```

You can also add a `--wait` flag to wait for geovisio to process all the pictures.

## Development

### Tests

Tests are run using PyTest. By default, our tests use a [Docker Compose](https://docs.docker.com/compose/) environment (located in `./tests/integration/docker-compose-geovisio.yml`) to set-up a temporary GeoVisio API to run onto. If you have Docker Compose enabled and running on your machine, you can simply run this command to launch tests:

```bash
pytest
```

If you don't have Docker Compose, or want to use an existing GeoVisio test instance (to speed up tests), you can pass the `--external-geovisio-url` option to pytest:

```bash
pytest --external-geovisio-url=http://localhost:5000
```

### Documentation

High-level documentation is handled by [Typer](https://typer.tiangolo.com/). You can update the generated `USAGE.md` file using this command:

```bash
make docs
```

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Note that before opening a pull requests, you may want to check formatting and tests of your changes:

```bash
make ci
```


## License

Copyright (c) GeoVisio team 2022-2023, [released under MIT license](./LICENSE).
