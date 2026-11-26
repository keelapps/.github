#!/usr/bin/env bash
# Remove the npm cache folder left by a Forge build.
set -e

CACHE_DIR=$1
echo "Cleaning $CACHE_DIR"
rm -rf $CACHE_DIR/*
