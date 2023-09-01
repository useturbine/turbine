#!/bin/bash

set -e

# Function to increment version number (simple version)
increment_version() {
    echo "$1" | awk -F. '{$NF = $NF + 1;} 1' OFS=.
}

# Step 1: Increment version number in setup.py
CURRENT_VERSION=$(grep -oP 'version="\K[0-9]+\.[0-9]+' setup.py)
NEW_VERSION=$(increment_version $CURRENT_VERSION)
sed -i "s/version=\"$CURRENT_VERSION/version=\"$NEW_VERSION/g" setup.py
echo "Version bumped to $NEW_VERSION"

# Step 2: Clean up dist directory
rm -rf dist
mkdir dist

# Step 3: Build the package
python setup.py sdist bdist_wheel

# Step 4: Upload the package to PyPI
twine upload dist/*

echo "Package updated and uploaded successfully!"