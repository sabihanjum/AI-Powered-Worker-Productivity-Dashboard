#!/bin/bash
set -e

echo "📦 Installing Python dependencies..."
if [ -f backend/requirements.txt ]; then
	pip install -r backend/requirements.txt
elif [ -f requirements.txt ]; then
	pip install -r requirements.txt
else
	echo "❌ requirements.txt not found"
	exit 1
fi

echo "✅ Build complete!"
