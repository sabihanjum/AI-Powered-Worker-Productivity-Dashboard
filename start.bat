@echo off
echo ========================================
echo Worker Productivity Dashboard - Setup
echo ========================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker found!
echo.

echo Checking Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose is not installed or not in PATH
    pause
    exit /b 1
)

echo Docker Compose found!
echo.

echo Starting the application...
echo This may take a few minutes on first run...
echo.

docker-compose up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Application started successfully!
    echo ========================================
    echo.
    echo Frontend:  http://localhost:3000
    echo Backend:   http://localhost:8000
    echo API Docs:  http://localhost:8000/docs
    echo.
    echo To stop the application, run: docker-compose down
    echo To view logs, run: docker-compose logs -f
    echo.
    pause
) else (
    echo.
    echo ERROR: Failed to start the application
    echo Please check the error messages above
    pause
    exit /b 1
)
