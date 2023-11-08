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
    depinspect [OPTIONS]
    ```

## Usage

```ignorelang
Usage: depinspect [OPTIONS]

Options:
  -p1, --package1 <TEXT TEXT TEXT>...
                                  Provide the first distribution, architecture
                                  and package name separated by whitespaces.
                                  Order of arguments matters. Example:
                                  --package1 i386 ubuntu apt

  -p2, --package2 <TEXT TEXT TEXT>...
                                  Provide the second distribution,
                                  architecture and package name separated by
                                  whitespaces. Order of arguments matters.
                                  Example: --package2 ubuntu amd64 grub-common

  -l, --list                      List all available distributions,
                                  architectures and package names.

  -u, --update                    Forcefully re-initialize database. This
                                  removes old database, fetches all defined
                                  metadata and stores it in a new database.

  --help                          Show this message and exit.
```

## Examples

Below are common use cases.

### List stored metadata

It is helpful to see the list of available distributions, architectures and package names stored in the database. If the database already exists, then the following command outputs and stores this information in a file called available_data.txt:

```sh
depinspect --list > available_data.txt
```

If the database doesn't exist, `--list` will also implicitly call the initialization process.

### Initialize or re-initialize the database

The tool ensures that the database exists before you can query it for specific information, so it will implicitly create one for you. You can also manually re-initialize the database by calling:

```sh
depinspect --update
```

This will remove the old database file and start the initialization process, which consists of fetching metadata from pre-defined URL sources, parsing text files and storing parsed data in a new database.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
