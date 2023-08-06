# `h-cli`

**Usage**:

```console
$ h-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --verbose TEXT`: :mag: `LOG_LEVEL` one of: DEBUG, INFO, WARNING, ERROR, CRITICAL  [default: INFO]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `converter`: :rocket: manipulates files and etc.
* `dedub`: :two_men_holding_hands: dedublicates...

## `h-cli converter`

:rocket: manipulates files and etc.

**Usage**:

```console
$ h-cli converter [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `heic-to-jpg`: :camera: images from :green_apple: heic to...
* `img-to-pdf`: :camera: images into :memo: pdf

### `h-cli converter heic-to-jpg`

:camera: images from :green_apple: heic to jpg

**Usage**:

```console
$ h-cli converter heic-to-jpg [OPTIONS] IMAGES_FOLDER
```

**Arguments**:

* `IMAGES_FOLDER`: Path to folder with images  [required]

**Options**:

* `--help`: Show this message and exit.

### `h-cli converter img-to-pdf`

:camera: images into :memo: pdf

**Usage**:

```console
$ h-cli converter img-to-pdf [OPTIONS] IMAGES_FOLDER [PDF_FILE]
```

**Arguments**:

* `IMAGES_FOLDER`: Path to folder with images  [required]
* `[PDF_FILE]`: Result file name  [default: result.pdf]

**Options**:

* `--help`: Show this message and exit.

## `h-cli dedub`

:two_men_holding_hands: dedublicates something.

**Usage**:

```console
$ h-cli dedub [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `img-dedub`: deal with dublicated :camera: images

### `h-cli dedub img-dedub`

deal with dublicated :camera: images

**Usage**:

```console
$ h-cli dedub img-dedub [OPTIONS] DIRS...
```

**Arguments**:

* `DIRS...`: Path to dirs with images  [required]

**Options**:

* `--delete / --no-delete`: [default: no-delete]
* `--help`: Show this message and exit.
