# drclient
A docker registry client command line utility and Python library

[![PyPi](https://img.shields.io/pypi/v/drclient.svg?style=flat-square)](https://pypi.python.org/pypi/drclient)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)


## Overview

drclient uses the Docker registry REST API to interact with the registry not requiring a Docker daemon to be installed.


## Features

- Get information about a remote image
- Pull images from a docker registry into:
    - a local directory
    - a tar file

## Installation

```bash
pip install drclient
```

## Usage

Get information for the busybox image

```bash
drclient info busybox
```

Pull the busybox image into a temporary directory

```bash
drclient pull busybox
```

Pull the busybox image into a named directory

```bash
drclient pull busybox -d /tmp/busybox
```

Pull the busybox image into a tar file

```bash
drclient pull busybox -t /tmp/busybox.tar
```
