# `geovisio`

GeoVisio command-line client

**Usage**:

```console
$ geovisio [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `collection-status`: Print the status of a collection.
* `test-process`: (For testing) Generates a JSON file with...
* `upload`: Processes and sends a given sequence on...

## `geovisio collection-status`

Print the status of a collection.

Either a --location should be provided, with the full location url of the collection
or only the --id combined with the --api-url

**Usage**:

```console
$ geovisio collection-status [OPTIONS]
```

**Options**:

* `--id TEXT`: Id of the collection
* `--api-url TEXT`: GeoVisio endpoint URL
* `--location TEXT`: Full url of the collection
* `--wait / --no-wait`: wait for all pictures to be ready  [default: no-wait]
* `--help`: Show this message and exit.

## `geovisio test-process`

(For testing) Generates a JSON file with metadata used for upload

**Usage**:

```console
$ geovisio test-process [OPTIONS]
```

**Options**:

* `--path PATH`: Local path to your sequence folder  [required]
* `--help`: Show this message and exit.

## `geovisio upload`

Processes and sends a given sequence on your GeoVisio API

**Usage**:

```console
$ geovisio upload [OPTIONS]
```

**Options**:

* `--path PATH`: Local path to your sequence folder  [required]
* `--api-url TEXT`: GeoVisio endpoint URL  [required]
* `--user TEXT`: GeoVisio user name if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the username will be asked during run.  [env var: GEOVISIO_USER]
* `--password TEXT`: GeoVisio password if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the password will be asked during run.
Note: is is advised to wait for prompt without using this variable.  [env var: GEOVISIO_PASSWORD]
* `--wait / --no-wait`: wait for all pictures to be ready  [default: no-wait]
* `--help`: Show this message and exit.
