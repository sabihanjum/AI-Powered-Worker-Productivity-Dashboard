#!/bin/bash

echo "========================================"
echo "Worker Productivity Dashboard - Setup"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Please install Docker from https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ Docker found"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose is not installed"
    exit 1
fi

echo "✓ Docker Compose found"
echo ""

echo "Starting the application..."
echo "This may take a few minutes on first run..."
echo ""

# Start Docker Compose
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Application started successfully!"
    echo "========================================"
    echo ""
    echo "Frontend:  http://localhost:3000"
    echo "Backend:   http://localhost:8000"
    echo "API Docs:  http://localhost:8000/docs"
    echo ""
    echo "To stop the application, run: docker-compose down"
    echo "To view logs, run: docker-compose logs -f"
    echo ""
else
    echo ""
    echo "ERROR: Failed to start the application"
    echo "Please check the error messages above"
    exit 1
fi
