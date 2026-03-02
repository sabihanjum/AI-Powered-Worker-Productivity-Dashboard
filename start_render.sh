#!/usr/bin/env bash
set -e

echo "==========================================="
echo "Worker Productivity Backend - Starting"
echo "==========================================="
echo "📁 Current directory: $(pwd)"

if [ -f backend/render_start.py ]; then
  echo "🚀 Using backend/render_start.py"
  exec python backend/render_start.py
elif [ -f render_start.py ]; then
  echo "🚀 Using render_start.py"
  exec python render_start.py
else
  echo "❌ Could not find render start script"
  exit 1
fi
