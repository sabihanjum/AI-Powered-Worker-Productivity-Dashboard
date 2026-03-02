# Render Deployment Configuration - Backend Service

## Service Type
Web Service (Python)

## Repository
Connect your GitHub repository: AI-Powered-Worker-Productivity-Dashboard

## Basic Configuration

### Name
```
worker-productivity-backend
```

### Runtime
```
Python 3
```

### Region
```
Oregon (US West)
```
*Choose the region closest to your users*

### Branch
```
main
```

### Root Directory
```
(leave empty)
```

## Build & Deploy Commands

### Build Command
```bash
pip install -r backend/requirements.txt
```

### Start Command
```bash
bash backend/start_render.sh
```

## Environment Variables

Add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `PYTHON_VERSION` | `3.11.0` | Python runtime version |

*Note: PORT is automatically set by Render*

## Persistent Disk (Recommended)

To keep your database data across deploys:

### Add Disk
- **Name**: `backend-data`
- **Mount Path**: `/opt/render/project/src/backend/data`
- **Size**: `1` GB

## Health Check

### Health Check Path
```
/
```

### Expected Response
```json
{"status":"healthy","message":"Worker Productivity Dashboard API","version":"1.0.0"}
```

## Plan

- **Free Tier**: ✅ Suitable for testing/development
- **Starter ($7/month)**: Recommended for production (no cold starts)

## Auto Deploy

✅ Enable Auto-Deploy from `main` branch

## Deployment Steps

1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Check logs for "Data seeding completed successfully!"
4. Test the API: `https://your-app.onrender.com/`
5. Copy your backend URL for frontend configuration

## Expected Output in Logs

```
Worker Productivity Backend - Starting
✅ Modules imported successfully
📊 Initializing database schema...
✅ Database initialized
📦 Database is empty. Seeding with sample data...
Clearing existing data...
Seeding workers...
Created 6 workers
Seeding workstations...
Created 6 workstations
Generating events for the past 7 days...
Created 1456 events
Data seeding completed successfully!
✅ Database seeded successfully!
✨ Initialization complete!

🚀 Starting FastAPI server...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

## API Endpoints

After deployment, these endpoints will be available:

- `GET /` - Health check
- `GET /docs` - Interactive API documentation
- `GET /api/metrics/dashboard` - Dashboard metrics
- `POST /api/events` - Ingest single event
- `POST /api/events/batch` - Ingest batch events
- `POST /api/admin/seed-data` - Reseed database

## Troubleshooting

### Build Fails
- Check requirements.txt path: `backend/requirements.txt`
- Verify Python version: 3.11

### Start Fails
- Check start command includes `bash backend/start_render.sh`
- Verify shell script has correct permissions

### Database Errors
- Check persistent disk is mounted
- Verify app can write to disk mount path

### Import Errors
- Ensure `backend/app/__init__.py` exists
- Verify relative imports in Python files

## Performance

**Free Tier:**
- Cold start: ~30-60 seconds after 15 min inactivity
- Active response time: <100ms

**Paid Tier:**
- No cold starts
- Always-on
- Better resources

## Monitoring

View in Render Dashboard:
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory, Request rate
- **Events**: Deployment history

## Update Backend

To deploy updates:
```bash
git push origin main
# Render automatically deploys!
```

## Copy This URL

After deployment, copy your backend URL:
```
https://worker-productivity-backend.onrender.com
```

You'll need this for frontend configuration!
