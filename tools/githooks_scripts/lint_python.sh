#!/bin/sh

set -e

echo "Installing latest dependencies..."
python -m pip install -r requirements/testing/requirements.txt
python -m pip install -r requirements/app/requirements.txt

echo "Running flake8 in src"
python -m flake8 --max-line-length 120 --max-complexity 10 src

echo "Running pylint in src"
python -m pylint src --max-line-length=120 --disable=C0114 --fail-under=9.5

echo "Running ruff in src"
python -m ruff format src

echo "Running black in src"
python -m black src

echo "Running pydocstyle in src"
python -m pydocstyle --ignore D100,D104,D107,D212 src