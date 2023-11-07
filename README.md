# Depinspect

[![Build status](https://github.com/artem-burashnikov/depinspect/actions/workflows/ci.yml/badge.svg)](https://github.com/artem-burashnikov/depinspect/actions/workflows/ci.yml?branch=dev)
[![License: MIT Licence](https://img.shields.io/badge/license-MIT-blue)](https://github.com/artem-burashnikov/depinspect/blob/main/LICENSE)

## Overview

Depinspect is an analyzer system which is an utility designed to prodive insights into linux package dependencies across multiple architectures and distributions.

## Features

TODO

## Getting Started

### Prerequisites

- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3.10+](https://wiki.python.org/moin/BeginnersGuide/Download)
- [pipx](https://pypa.github.io/pipx/#install-pipx)
- [Poetry >=1.7.0](https://python-poetry.org/).

    Can be installed with [pipx](https://python-poetry.org/docs/#installing-with-pipx) by running:

    ```sh
    pipx install poetry
    ```

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

3. Install all required dependencies with:

    ```sh
    poetry install
    ```

4. After the installation is complete, you can use the tool by running this command inside the project root directory:

    ```sh
    poetry run depinspect [OPTIONS]
    ```

### Usage

```ignorelang
Usage: depinspect [OPTIONS]

Options:
  -p1, --package1 <TEXT TEXT>...  Provide the first package name alog with an
                                  architecture separated by whitespace. Example:
                                  --package1 package1-name arch1

  -p2, --package2 <TEXT TEXT>...  Provide the second package name alog with an
                                  architecture separated by whitespace. Example:
                                  --package2 package2-name arch2

  -u, --update                    Forcefully re-initialize database. This removes
                                  old database, fetches all defined metadata and
                                  stores it in a new database.
                                  
  --help                          Show this message and exit.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
