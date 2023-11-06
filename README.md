# Depinspect

[![Build status](https://github.com/artem-burashnikov/depinspect/actions/workflows/ci.yml/badge.svg)](https://github.com/artem-burashnikov/depinspect/actions/workflows/ci.yml?branch=dev)
[![License: MIT Licence](https://img.shields.io/badge/license-MIT-blue)](https://github.com/artem-burashnikov/depinspect/blob/main/LICENSE)

## Overview

Depinspect is an analyzer system which is an utility designed to prodive insights into linux package dependencies across multiple architectures and distributions.

## Features

TODO

## Getting Started

### Prerequisites

It is recommended but not required to use [Poetry >=1.6.1](https://python-poetry.org/) to run the tool.

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

3. If you are using Poetry, then install all required dependencies with:

    ```bash
    poetry install
    ```

4. After the installation is complete, you can use the tool by running this command inside the project root directory:

    ```bash
    poetry run depinspect [OPTIONS]
    ```

### Usage

```ignorelang
Usage: depinspect [OPTIONS]

Options:
  --package1 <TEXT TEXT>...  Provide the first package name alog with an
                             architecture separated by whitespace. Example:
                             --package1 package1_name arch_1  [required]
  --package2 <TEXT TEXT>...  Provide the second package name alog with an
                             architecture separated by whitespace. Example:
                             --package2 package2_name arch_2  [required]
  --help                     Show this message and exit.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
