# Quick Start Guide

## Get Started in 3 Minutes

### Option 1: Docker (Recommended)

```bash
# 1. Start the application
docker-compose up --build

# 2. Open your browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

That's it! The database will be automatically populated with sample data.

### Option 2: Local Development

#### Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database and seed data
python -m app.seed_data

# Start the server
python -m app.main
```

Backend will run at http://localhost:8000

#### Frontend

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at http://localhost:3000

## Testing the API

### Using the Interactive Docs

Visit http://localhost:8000/docs for Swagger UI with interactive API testing.

### Using curl

```bash
# Get dashboard metrics
curl http://localhost:8000/api/metrics/dashboard

# List all workers
curl http://localhost:8000/api/workers

# Ingest a new event
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2026-03-02T14:30:00Z",
    "worker_id": "W1",
    "workstation_id": "S1",
    "event_type": "working",
    "confidence": 0.95,
    "count": 0
  }'

# Refresh dummy data
curl -X POST http://localhost:8000/api/admin/seed-data?days=7
```

## Viewing the Dashboard

1. Open http://localhost:3000
2. You'll see:
   - Factory-wide metrics at the top
   - Worker metrics in cards
   - Workstation metrics below
3. Use the dropdowns to filter by specific worker or workstation
4. Click "🔄 Refresh Data" to regenerate dummy data

## Sample Data

The application comes pre-loaded with:
- **6 Workers**: W1-W6 (John Smith, Sarah Johnson, etc.)
- **6 Workstations**: S1-S6 (Assembly, QC, Packaging, Inspection)
- **7 Days of Events**: ~2000-3000 events representing realistic factory activity

## Troubleshooting

### Backend won't start
- Ensure port 8000 is not in use
- Check Python version (requires 3.11+)
- Verify all dependencies installed: `pip install -r requirements.txt`

### Frontend won't start
- Ensure port 3000 is not in use
- Check Node version (requires 18+)
- Try: `rm -rf node_modules && npm install`

### Dashboard shows "Failed to load data"
- Make sure backend is running at http://localhost:8000
- Check backend logs for errors
- Verify database is initialized: Look for `factory_productivity.db` file

### Docker issues
- Ensure Docker daemon is running
- Try: `docker-compose down && docker-compose up --build`
- Check logs: `docker-compose logs -f`

## Next Steps

- Explore the API documentation at http://localhost:8000/docs
- Ingest custom events via the API
- Modify seed_data.py to generate different patterns
- Customize the dashboard in frontend/src/App.jsx

## Need Help?

Check the main README.md for comprehensive documentation including:
- Architecture details
- Database schema
- Metric definitions
- Scaling strategies
- ML operations considerations
