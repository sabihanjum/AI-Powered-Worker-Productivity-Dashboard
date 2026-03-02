#!/bin/bash
set -e

echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "✅ Build complete!"
