# Render CLI Deployment Commands

## Installation

### Install Render CLI

**macOS:**
```bash
brew install render
```

**Linux:**
```bash
curl -sSL https://download.render.com/render-linux-x64.tar.gz | tar xz
sudo mv render /usr/local/bin/
```

**Windows (with Chocolatey):**
```bash
choco install render
```

**Or download directly:**
Visit: https://render.com/docs/cli

---

## Authentication

### Login to Render

```bash
render login
```

This will:
1. Open browser to Render login
2. Authorize CLI access
3. Save authentication token locally

---

## Deploy Entire Project

### Option 1: Deploy Both Services Together

```bash
# From project root directory
render deploy --service worker-productivity-backend
render deploy --service worker-productivity-frontend
```

---

## Individual Service Deployment

### Deploy Backend Only

```bash
render deploy \
  --service worker-productivity-backend \
  --clear-cache
```

### Deploy Frontend Only

```bash
render deploy \
  --service worker-productivity-frontend \
  --clear-cache
```

---

## Create New Services via CLI

### Create Backend Service

```bash
render create-service \
  --name worker-productivity-backend \
  --type web \
  --runtime python \
  --repo https://github.com/your-username/AI-Powered-Worker-Productivity-Dashboard.git \
  --build-command "pip install -r backend/requirements.txt" \
  --start-command "bash backend/start_render.sh" \
  --region oregon \
  --plan free
```

### Create Frontend Service

```bash
render create-service \
  --name worker-productivity-frontend \
  --type static_site \
  --repo https://github.com/your-username/AI-Powered-Worker-Productivity-Dashboard.git \
  --build-command "cd frontend && npm install && npm run build" \
  --publish-dir frontend/dist \
  --region oregon \
  --plan free
```

---

## Environment Variables via CLI

### Set Environment Variable on Backend

```bash
render env-vars set \
  --service worker-productivity-backend \
  PYTHON_VERSION=3.11.0
```

### Set Environment Variable on Frontend

```bash
render env-vars set \
  --service worker-productivity-frontend \
  VITE_API_URL=https://worker-productivity-backend.onrender.com
```

### List Environment Variables

```bash
render env-vars list --service worker-productivity-backend
```

---

## Common CLI Commands

### View Service Status

```bash
# Backend
render service-info --service worker-productivity-backend

# Frontend
render service-info --service worker-productivity-frontend
```

### View Real-time Logs

```bash
# Backend logs
render logs --service worker-productivity-backend --follow

# Frontend logs
render logs --service worker-productivity-frontend --follow

# Follow specific number of lines
render logs --service worker-productivity-backend --lines 50
```

### Restart Service

```bash
# Backend
render restart --service worker-productivity-backend

# Frontend
render restart --service worker-productivity-frontend
```

### List All Services

```bash
render services list
```

---

## Full Deployment Script

### Deploy Everything from Scratch

```bash
#!/bin/bash
set -e

echo "🔐 Logging in to Render..."
render login

echo "🚀 Creating backend service..."
render create-service \
  --name worker-productivity-backend \
  --type web \
  --runtime python \
  --repo https://github.com/sabihanjum/AI-Powered-Worker-Productivity-Dashboard.git \
  --build-command "pip install -r backend/requirements.txt" \
  --start-command "bash backend/start_render.sh" \
  --region oregon \
  --plan free

echo "⏳ Waiting for backend to deploy..."
sleep 30

echo "✅ Creating frontend service..."
render create-service \
  --name worker-productivity-frontend \
  --type static_site \
  --repo https://github.com/sabihanjum/AI-Powered-Worker-Productivity-Dashboard.git \
  --build-command "cd frontend && npm install && npm run build" \
  --publish-dir frontend/dist \
  --region oregon \
  --plan free

echo "⏳ Waiting for frontend to deploy..."
sleep 20

echo "🔧 Setting environment variables..."
render env-vars set \
  --service worker-productivity-backend \
  PYTHON_VERSION=3.11.0

BACKEND_URL=$(render service-info --service worker-productivity-backend | grep -i "url" | head -1 | awk '{print $NF}')

render env-vars set \
  --service worker-productivity-frontend \
  VITE_API_URL=$BACKEND_URL

echo ""
echo "✅ Deployment Complete!"
echo "Backend: https://worker-productivity-backend.onrender.com"
echo "Frontend: https://worker-productivity-frontend.onrender.com"
```

### Save as: `deploy.sh`

Run with:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Deploy & Redeploy on Push

### Auto-Deploy Setup

Once services are created, Render automatically deploys on GitHub push:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Render CLI automatically detects and deploys!
# Check status with:
render logs --service worker-productivity-backend --follow
```

---

## Monitor Deployments

### Watch Deployment Logs

```bash
# Real-time logs
render logs --service worker-productivity-backend --follow

# Last 100 lines
render logs --service worker-productivity-backend --lines 100

# Export logs to file
render logs --service worker-productivity-backend > backend-logs.txt
```

### Get Service URL

```bash
render service-info --service worker-productivity-backend | grep "URL"
```

---

## Clear Build Cache & Redeploy

```bash
# Backend
render deploy \
  --service worker-productivity-backend \
  --clear-cache

# Frontend
render deploy \
  --service worker-productivity-frontend \
  --clear-cache
```

---

## Delete Services (if needed)

```bash
# Delete backend
render delete-service --service worker-productivity-backend

# Delete frontend
render delete-service --service worker-productivity-frontend
```

---

## Quick Reference Card

```bash
# Login
render login

# Check status
render service-info --service worker-productivity-backend

# View logs
render logs --service worker-productivity-backend --follow

# Redeploy
render deploy --service worker-productivity-backend

# Clear cache & redeploy
render deploy --service worker-productivity-backend --clear-cache

# Set env variable
render env-vars set --service worker-productivity-backend KEY=VALUE

# List all services
render services list

# Restart service
render restart --service worker-productivity-backend
```

---

## Troubleshooting CLI Issues

### CLI Not Found

```bash
# Check if installed
which render

# If not found, reinstall:
brew reinstall render  # macOS
```

### Authentication Failed

```bash
# Clear auth and login again
rm ~/.render-auth
render login
```

### Command Takes Too Long

```bash
# Use verbose output for debugging
render deploy \
  --service worker-productivity-backend \
  --verbose
```

---

## GitHub Actions Integration (Optional)

### Auto-deploy on GitHub Push

Create `.github/workflows/render-deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Render CLI
        run: curl -sSL https://download.render.com/render-linux-x64.tar.gz | tar xz
      
      - name: Deploy Backend
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: ./render deploy --service worker-productivity-backend
      
      - name: Deploy Frontend
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: ./render deploy --service worker-productivity-frontend
```

Then add secret:
1. Go to GitHub repo Settings → Secrets
2. Add `RENDER_API_KEY` from Render dashboard

---

## Complete Workflow Example

```bash
# 1. Login
render login

# 2. Check backend status
render service-info --service worker-productivity-backend

# 3. View backend logs
render logs --service worker-productivity-backend --lines 50

# 4. Set environment variable
render env-vars set \
  --service worker-productivity-frontend \
  VITE_API_URL=https://worker-productivity-backend.onrender.com

# 5. Redeploy frontend with updates
render deploy \
  --service worker-productivity-frontend \
  --clear-cache

# 6. Watch deployment
render logs --service worker-productivity-frontend --follow

# 7. Verify deployment
render service-info --service worker-productivity-frontend
```

---

## Get Help

### Render CLI Help

```bash
render help
render help deploy
render help create-service
render help env-vars
```

### Render Documentation

- Full CLI Docs: https://render.com/docs/cli
- API Reference: https://render.com/docs/api
- Contact: support@render.com

---

## Usage Tips

1. **Always use full service names** for commands
2. **Use `--follow`** flag to watch logs in real-time
3. **Use `--clear-cache`** when environment variables change
4. **Keep authentication token safe** - it's in `~/.render-auth`
5. **Use scripts** for repeated deployments

---

## Common Patterns

### Deploy Frontend After Backend URL Changes

```bash
# 1. Get new backend URL
BACKEND_URL=$(render service-info --service worker-productivity-backend | grep URL)

# 2. Update frontend env
render env-vars set \
  --service worker-productivity-frontend \
  VITE_API_URL=$BACKEND_URL

# 3. Redeploy frontend
render deploy \
  --service worker-productivity-frontend \
  --clear-cache
```

### Quick Restart & Check

```bash
render restart --service worker-productivity-backend && \
sleep 5 && \
render logs --service worker-productivity-backend --lines 20
```

### Monitor Both Services

```bash
# In one terminal
render logs --service worker-productivity-backend --follow

# In another terminal
render logs --service worker-productivity-frontend --follow
```

---

**Ready to deploy?** Start with:
```bash
render login
render deploy --service worker-productivity-backend
```
