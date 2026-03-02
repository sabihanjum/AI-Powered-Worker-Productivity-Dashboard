#!/usr/bin/env bash
# Render build script for backend

set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"
