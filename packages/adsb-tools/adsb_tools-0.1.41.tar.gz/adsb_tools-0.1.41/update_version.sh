#!/bin/bash

echo "one"

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Please provide an argument: major, minor, or patch"
  exit 1
fi


echo "two"

# Check if the argument is valid
case "$1" in
  major|minor|patch) ;;
  *) echo "Invalid argument: $1. Please use major, minor, or patch"
     exit 2 ;;
esac
echo "three"

# Check if the pyproject.toml file exists
if [ ! -f pyproject.toml ]; then
  echo "pyproject.toml file not found"
  exit 3
fi


echo "four"

# Read the current version from the file
version=$(grep -oP '(?<=version = ")[^"]*' pyproject.toml)


echo "five"

# Split the version into major, minor, and patch components
IFS='.' read -r -a components <<< "$version"
major=${components[0]}
minor=${components[1]}
patch=${components[2]}

# Increment the appropriate component based on the argument
case "$1" in
  major) ((major++))
         minor=0
         patch=0 ;;
  minor) ((minor++))
         patch=0 ;;
  patch) ((patch++)) ;;
esac

# Construct the new version string
new_version="$major.$minor.$patch"

# Replace the version in the file with the new version
sed -i "s/version = \"$version\"/version = \"$new_version\"/" pyproject.toml

# Print a confirmation message
echo "Updated version from $version to $new_version"
