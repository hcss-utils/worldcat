# `worldcat`: A Python package for parsing WorldCatDissertations database


# Installation - development

Create a virtual environment, for example using `venv`:

```shell
$ python -m venv venv-worldcat
$ source venv-worldcat/bin/activate
$ cd worldcat
$ python -m pip install -e .[dev]

```

Note that the last command installs a development environment, as it also installs packages needed for development, like `black` (for code formatting), `pytest` (for unit testing) and `wheel` (for creating wheel files from the package).


# Testing

Running the tests requires to run the following command in the root folder (of course in the virtual environment):

```shell
(venv-worldcat) > pytest
```

## How to build a Python package?

To build the package, you need to go to the root folder of the package and run the following command:

```shell
(venv-worldcat) > python setup.py sdist bdist_wheel
```

Note that this assumes you have `wheel` installed in your virtual environment, and `makepackage` does this for you.

The built package is now located in the dist/ folder.

# Usage

Refer to [`examples/run.py`](examples/run.py) or use CLI:

```console
(venv-worldcat) > parse --help
```
