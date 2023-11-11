# Depinspect

[![Build status](https://github.com/artem-burashnikov/depinspect/actions/workflows/ci.yml/badge.svg)](https://github.com/artem-burashnikov/depinspect/actions/workflows/ci.yml?branch=dev)
[![License: MIT Licence](https://img.shields.io/badge/license-MIT-blue)](https://github.com/artem-burashnikov/depinspect/blob/main/LICENSE)

## Overview

Depinspect is an utility designed to prodive insights into linux package dependencies across multiple architectures and distributions.

## Features

TODO

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
    ddepinspect [OPTIONS] COMMAND [ARGS]...
    ```

## Usage

```ignorelang
Usage: depinspect [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  diff    Find a difference and similarities in dependencies of two...
  list    List all available distributions, architectures and...
  update  Forcefully re-initialize database.This removes old database,...
```

### Commands

- `depinspect diff --help`

This command requires two `--package` options to be specified.

```ignorelang
Usage: depinspect diff [OPTIONS]

  Find a difference and similarities in dependencies of two packagesfrom
  different distributions and architectures.

Options:
  -p, --package <TEXT TEXT TEXT>...
                                  Provide distribution, architecture and
                                  package name separated by whitespaces. Order
                                  of arguments matters.
                                  
                                  Example: --package ubuntu i386 apt
  --help                          Show this message and exit.
```

- `depinspect list --help`

```ignorelang
Usage: depinspect list [OPTIONS]

  List all available distributions, architectures and packages.This implicitly
  initializez a new database.

Options:
  --help  Show this message and exit.
```

- `depinspect update --help`

```ignorelang
Usage: depinspect update [OPTIONS]

  Forcefully re-initialize database. This removes old database, fetches all
  defined metadata and stores it in a new database.

Options:
  --help  Show this message and exit.
```

## Examples

Below are common use cases.

### List stored metadata

It is helpful to see the list of available distributions, architectures and package names stored in the database. If the database already exists, then the following command outputs and stores this information in a file called available_data.txt:

```sh
depinspect list > available_data.txt
```

If the database doesn't exist, `list` will also implicitly call the initialization process.

### Initialize or re-initialize the database

The tool ensures that the database exists before you can query it for specific information, so it will implicitly create one for you. You can also manually re-initialize the database by calling:

```sh
depinspect update
```

This will remove the old database file and start the initialization process, which consists of fetching metadata from pre-defined URL sources, parsing text files and storing parsed data in a new database.

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
======================================
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
======================================
libgcc-s1 (>= 4.2)

These dependencies are exclusive to:
ubuntu - amd64 - apt
======================================
libgcc-s1 (>= 3.3.1)
```

Which first tells you the shared dependencies for specified packages and then lists exclusive dependencies for each of them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
