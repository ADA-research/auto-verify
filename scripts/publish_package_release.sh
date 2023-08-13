#!/bin/bash
# TODO: Test this script

# Clean
rm -rf dist build */*.egg-info *.egg-info

# Build
python -m build

# Publish
twine upload dist/*

# TODO: Github tagged release
