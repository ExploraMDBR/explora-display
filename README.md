# explora-display

![RaspberryPi](https://img.shields.io/badge/-RaspberryPi-C51A4A?logo=raspberrypi&logoColor=white)
[![Made with Python](https://img.shields.io/badge/Python->=3.9-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

Python module for creating simple interactive kiosk displays for phygital installations. 

## Installation

```bash
pip install -i https://test.pypi.org/simple/ explora-display --extra-index-url https://pypi.org/simple
```

```python
from explora.display import display_server
```

## Development
This project uses [Poetry](https://python-poetry.org/docs/#installation) for dependencies management and packaging.

```bash
# clone reporitory
git clone <repo>
cd explora-display

# install dependecies
poetry install

# activate Python virtual environment
poetry shell

```
