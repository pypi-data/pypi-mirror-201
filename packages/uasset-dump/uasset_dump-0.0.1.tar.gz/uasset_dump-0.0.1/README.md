# Unreal Engine Assets Dump

Command-line Interface (CLI) responsible for returning the list of the assets of an Unreal Engine project into a JSON structure.

## Installation

### Poetry

Unreal Engine Assets Dump used Poetry to declare all its dependencies.  [Poetry](https://python-poetry.org/) is a python dependency management tool to manage dependencies, packages, and libraries in your python project.

We need to install Poetry with Unreal Engine Python:

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Then, we need to create the Python virtual environment using Poetry:

```shell
poetry env use /Users/Shared/Epic\ Games/UE_5.1/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3
```

We can enter this virtual environment and install all the required dependencies:

```shell
poetry shell
poetry update
```
