# Depinspect

[![Build status][status-shield]][status-url]
[![MIT License][license-shield]][license-url]

## Overview

**Depinspect** is an utility that offers an abstraction layer which simplifies the retrieval of package-related information across different distributions and architectures.

### Project structure

Below is the default project structure.

```ignorelang
depinspect/
├── depinspect
│   ├── __init__.py
│   ├── cli.py
│   ├── constants.py
│   ├── files.py
│   ├── helper.py
│   ├── printer.py
│   └── validator.py
│   ├── archives
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   └── fetcher.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── fedora/
│   │   └── ubuntu/
│   ├── distributions
│   │   ├── __init__.py
│   │   ├── fedora.py
│   │   ├── ubuntu.py
│   │   ├── loader.py
│   │   ├── mapping.py
│   │   └── package.py
├── tests
│   └── ...
├── poetry.lock
├── pyproject.toml
├── LICENSE
└── README.md
```

## Features

- **Data Aggregation:** Gathers information about packages from multiple distributions and their corresponding releases.

- **Unified Access:** Provides a streamlined and unified access point for stored metadata.

- **Modular Architecture:** Employs a modular design for simpler extendability, allowing easy integration of new features.

- **CLI Support:** Includes a Command-Line Interface (CLI) for a quick overview of divergent dependencies and other relevant information.

## Table of contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

## Getting Started

### Prerequisites

- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3.10+ with pip 19.0+](https://wiki.python.org/moin/BeginnersGuide/Download)
- [pipx](https://pypa.github.io/pipx/#install-pipx) - to install and run Python applications in isolated environments

### Installation

Open the terminal and follow these steps:

1. Clone the repository:

    ```sh
    git clone git@github.com:artem-burashnikov/depinspect.git
    ```

2. Navigate to the project root:

    ```sh
    cd depinspect
    ```

3. Install `Poetry` in an isolated environment with:

    ```sh
    pipx install poetry
    ```

    `pipx` can also run Poetry from a temporary environment without installing it explicitly. See pipx [documentation](https://pypa.github.io/pipx/docs/) for details.

4. Install all required dependencies with:

    **Note**: Running the command will automatically create a virtual environment and install all dependencies in an isolated manner. For details see Poetry [documentation](https://python-poetry.org/docs/cli/#install).

    ```sh
    poetry install
    ```
  
5. After the installation is complete, you can use the tool by running this command from within a virtual environment:

    ```sh
    depinspect [OPTIONS] COMMAND [ARGS]...
    ```

6. Make sure to load the initial metadata before querying with:

    ```sh
    depinspect update
    ```

## Usage

Tool command line has the following interface:

```ignorelang
Usage: depinspect [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  diff            Compare two packages.
  find-divergent  List all packages that have divergent dependencies.
  list-all        List stored architectures and packages for a given distro.
  update          Update metadata stored in databases.
```

For any command the `--help` option is available and prints the synopsis. The specific options are described below.

### `depinspect update`

Metadata is stored in `SQlite` databases.

In order to refresh the information, `depinspect update` can be manually called.

The command have to also be called to initialize databases when using the tool for the first time.

### `depinspect diff`

Find a difference and similarities in dependencies of two packages. This command requires two sets of parameters each under `-p` flag to be specified.

**Options**:

- **-p \<TEXT TEXT TEXT>**

  Flag accepts `distribution`, `architecture` and `name` parameters in that specific order. This is a required option. Two such options need to be specified for invocation. See examples for usage.

### `depinspect list-all`

This command outputs the list of distinct architctures and package names for a specified distribution.

**Options**:

- **--distro**

  The choice of one of currently supported distributions. This is a required option. You can see the list of currently supported distributions by runnunig

  ```sh
  depinspect list-all --help
  ```

### `depinspect find-divergent`

For a specified distribution and two architectures this command lists all packages that have divergent dependencies between those architectures.

**Options**:

- **--distro**

  Same as in `depinspect list-all`.

- **--arch**

  Two supported architectures need to be specified under this flag. This is a required option. You can see the list of currently supported architectures by runnunig. See examples for usage.

  ```sh
  depinspect find-divergent --help

## Examples

Below are common use cases.

### Initialize or update the metadata in databases

The metadata is stored in SQLite databases which need to be initialized befora the queries will yield any significant results. Updates don't start automatically, so if you don't see any output try running the command first. You can start the update with:

```sh
depinspect update
```

### List stored metadata

It is helpful to see the list of available architectures and package names stored in the database for a particular distribution. The following command outputs and stores the information for ubuntu in a file called `available_data.txt`:

```sh
depinspect list-all --distro=ubuntu > ubuntu_available_data.txt
```

### Find differnces and similarities between two packages

By running

```sh
depinspect diff -p ubuntu i386 apt -p ubuntu amd64 apt
```

You get the following output:

```ignorelang
These dependencies are present in both:
ubuntu - i386 - apt
ubuntu - amd64 - apt
================================================================================
adduser
gpgv | gpgv2 | gpgv1
libapt-pkg6.0 (>= 2.4.5)
libc6 (>= 2.34)
libgnutls30 (>= 3.7.0)
libseccomp2 (>= 2.4.2)
libstdc++6 (>= 11)
libsystemd0
ubuntu-keyring

These dependencies are exclusive to:
ubuntu - i386 - apt
================================================================================
libgcc-s1 (>= 4.2)

These dependencies are exclusive to:
ubuntu - amd64 - apt
================================================================================
libgcc-s1 (>= 3.3.1)
```

Which first tells you the shared dependencies for specified packages and then lists exclusive dependencies for each of them.

### Find all packages with divergent dependencies

If you wish to find all packages for two architectures, whose dependenices have differences, you can do so with the following command:

```sh
depinspect find-divergent --distro=ubuntu --arch amd64 i386 > divergent_packages.txt
```

The result will be saved in `divergent_packages.txt`.

## License

This project is licensed under the MIT License - see the [LICENSE][license-url] for details.

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/artem-burashnikov/depinspect.svg?style=for-the-badge&color=blue
[license-url]: https://github.com/artem-burashnikov/depinspect/blob/main/LICENSE
[status-shield]: https://img.shields.io/github/actions/workflow/status/artem-burashnikov/depinspect/.github/workflows/ci.yml?branch=main&event=push&style=for-the-badge
[status-url]: https://github.com/artem-burashnikov/depinspect/blob/main/.github/workflows/ci.yml
