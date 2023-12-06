# Depinspect

[![Build status][status-shield]][status-url]
[![MIT License][license-shield]][license-url]

## Overview

Depinspect is an utility designed to prodive insights into linux package dependencies across multiple architectures and distributions.

## Table of contents

<ol>

  <li>
  <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
      <li><a href="#installation">Installation</a></li>
      <li><a href="#usage">Usage</a></li>
    </ul>
  </li>

  <li>
  <a href="#examples">Examples</a>
  </li>

  <li>
  <a href="#license">License</a>
  </li>
</ol>

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

## Usage

TODO

### `depinspect diff --help`

This command requires two `--package` options to be specified.

TODO

### `depinspect list-all --help`

TODO

### `depinspect update --help`

TODO

### `depinspect find-divergent --help`

TODO

## Examples

Below are common use cases.

### List stored metadata

It is helpful to see the list of available architectures and package names stored in the database for a particular distribution. The following command outputs and stores the information for ubuntu in a file called available_data.txt:

```sh
depinspect list-all ubuntu > ubuntu_available_data.txt
```

### Initialize or re-initialize the database

The tool ensures that databases exist before you can query for specific information, so it will implicitly create them for you, fetching fresh metadata. You can also manually re-initialize the database by calling:

```sh
depinspect update
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

### Find all packages with divergent dependencies

If you wish to find all packages from two architectures, whose dependenices have differences, you can do so with the following command:

```sh
depinspect find-divergent --arch ubuntu amd64 --arch ubuntu i386 > output.txt
```

The command will save the result in `output.txt`.

## License

This project is licensed under the MIT License - see the [LICENSE][license-url] for details.

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/artem-burashnikov/depinspect.svg?style=for-the-badge&color=blue
[license-url]: https://github.com/artem-burashnikov/depinspect/blob/main/LICENSE
[status-shield]: https://img.shields.io/github/actions/workflow/status/artem-burashnikov/depinspect/.github/workflows/ci.yml?branch=main&event=push&style=for-the-badge
[status-url]: https://github.com/artem-burashnikov/depinspect/blob/main/.github/workflows/ci.yml
