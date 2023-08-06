# `pyWAS`

*Py*thon *W*rapper for *A*nalog design *S*oftware

**Installation using [pipx](https://pypa.github.io/pipx/installation/)**:

```console
$ pipx install pywas
```

**Usage**:

```console
$ pyWAS [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `new`
* `ngspice`

## `pyWAS new`

**Usage**:

```console
$ pyWAS new [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyWAS ngspice`

**Usage**:

```console
$ pyWAS ngspice [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `config`
* `install`: Install ngspice executable in the correct...
* `run`: Should not be named "run"

### `pyWAS ngspice config`

**Usage**:

```console
$ pyWAS ngspice config [OPTIONS] KEY PATH
```

**Arguments**:

* `KEY`: [required]
* `PATH`: [required]

**Options**:

* `--help`: Show this message and exit.

### `pyWAS ngspice install`

Install ngspice executable in the correct location.

**Usage**:

```console
$ pyWAS ngspice install [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `pyWAS ngspice run`

Should not be named "run"

**Usage**:

```console
$ pyWAS ngspice run [OPTIONS] IN_FILE
```

**Arguments**:

* `IN_FILE`: [required]

**Options**:

* `--out-folder TEXT`: [default: C:\Users\Potereau\PycharmProjects\pyWES/tmp/]
* `--help`: Show this message and exit.
