# Clean
rm -rf dist build */*.egg-info *.egg-info

# Build
python -m build

# Publish
twine upload dist/*

# Github release: do manually
