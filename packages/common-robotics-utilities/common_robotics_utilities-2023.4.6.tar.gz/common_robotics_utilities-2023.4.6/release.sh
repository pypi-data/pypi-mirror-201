#!/bin/bash
python setup.py bdist
python setup.py bdist_wheel
python setup.py sdist
twine check dist/*
