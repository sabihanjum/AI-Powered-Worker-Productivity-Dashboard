# Deploy Backend and Frontend Separately on Render

## Backend Deployment

### Step 1: Create Backend Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `AI-Powered-Worker-Productivity-Dashboard`

### Step 2: Configure Backend Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `worker-productivity-backend` (or your choice)
- **Runtime**: `Python 3`
- **Region**: Choose closest to you (e.g., Oregon)
- **Branch**: `main`
- **Root Directory**: Leave blank

**Build & Deploy:**
- **Build Command**: 
  ```bash
  pip install -r backend/requirements.txt
  ```

- **Start Command**:
  ```bash
  cd backend && python -c "from app.database import init_db; from app.seed_data import seed_all_data; from app.database import get_db; init_db(); conn = get_db().__enter__(); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) as count FROM events'); count = cursor.fetchone()['count']; conn.__exit__(None, None, None); seed_all_data(7) if count == 0 else None" && uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Plan:**
- Select **"Free"** (or upgrade as needed)

**Advanced Settings (Optional but Recommended):**
- **Add Persistent Disk**:
  - Name: `backend-data`
  - Mount Path: `/opt/render/project/src/backend/data`
  - Size: 1 GB
  
**Environment Variables:**
- `PYTHON_VERSION`: `3.11.0`

### Step 3: Deploy Backend

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. **Important**: Copy your backend URL (e.g., `https://worker-productivity-backend.onrender.com`)

---

## Frontend Deployment

### Step 4: Create Frontend Static Site

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Static Site"**
3. Connect the same GitHub repository

### Step 5: Configure Frontend Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `worker-productivity-frontend` (or your choice)
- **Branch**: `main`
- **Root Directory**: Leave blank

**Build & Deploy:**
- **Build Command**:
  ```bash
  cd frontend && npm install && npm run build
  ```

- **Publish Directory**:
  ```
  frontend/dist
  ```

**Environment Variables:**
- **Key**: `VITE_API_URL`
- **Value**: `https://worker-productivity-backend.onrender.com` 
  (Replace with your actual backend URL from Step 3)

### Step 6: Deploy Frontend

1. Click **"Create Static Site"**
2. Wait for deployment (3-5 minutes)
3. Your frontend will be live!

---

## Verify Deployment

### Test Backend
```bash
# Health check
curl https://your-backend-url.onrender.com/

# Get metrics
curl https://your-backend-url.onrender.com/api/metrics/dashboard
```

### Test Frontend
Visit: `https://your-frontend-url.onrender.com`

You should see:
- Factory-wide metrics at the top
- Worker cards in the middle
- Workstation cards at the bottom

---

## Troubleshooting

### Backend Issues

**Problem: Backend fails to start**

Check logs in Render Dashboard. Common issues:

1. **ModuleNotFoundError**: 
   - Build command should be: `pip install -r backend/requirements.txt`
   - Start command should include `cd backend`

2. **Database initialization fails**:
   - Check logs for specific error
   - Verify disk is mounted correctly

**Problem: Backend starts but shows errors**

Check if port is configured correctly in start command: `--port $PORT`

### Frontend Issues

**Problem: Frontend shows "Failed to load data"**

1. Verify `VITE_API_URL` environment variable is set correctly:
   - Go to Frontend service → Environment
   - Check the value matches your backend URL
   - No trailing slash!

2. Verify backend is running:
   - Visit backend URL directly
   - Should return: `{"status":"healthy",...}`

3. Check browser console (F12) for CORS errors

**Problem: Frontend shows blank page**

1. Check build logs for errors
2. Verify Publish Directory is: `frontend/dist`
3. Ensure build command ran successfully

### Cold Starts (Free Tier)

**Expected behavior:**
- Services sleep after 15 minutes of inactivity
- First request takes 30-60 seconds to wake up
- This is normal for free tier
- Upgrade to paid plan for always-on services

---

## URLs Reference

After deployment, save these URLs:

- **Frontend Dashboard**: `https://[your-frontend-name].onrender.com`
- **Backend API**: `https://[your-backend-name].onrender.com`
- **API Documentation**: `https://[your-backend-name].onrender.com/docs`

---

## Update Frontend After Backend Changes

If you need to update the backend URL:

1. Go to Render Dashboard
2. Select your frontend service
3. Go to **Environment** tab
4. Update `VITE_API_URL` value
5. Click **"Save Changes"**
6. Go to **Manual Deploy** tab
7. Click **"Clear build cache & deploy"**

---

## Auto-Deployment

After initial setup:
- Push to GitHub automatically triggers redeployment
- Both services redeploy independently
- No downtime during updates

```bash
git add .
git commit -m "Update application"
git push origin main
# Render automatically deploys!
```

---

## Cost

**Free Tier:**
- Backend Web Service: Free (with limitations)
- Frontend Static Site: Free
- **Total: $0/month**

**Limitations:**
- Services sleep after 15 minutes
- 750 hours/month per service
- Shared resources

**Starter (Recommended for Production):**
- Backend: $7/month (always-on)
- Frontend: Free
- **Total: $7/month**

---

## Need Help?

If you encounter issues:
1. Check Render logs (Dashboard → Service → Logs)
2. Review error messages carefully
3. Contact Render support: support@render.com
4. Check status: https://status.render.com/

---

## Success Checklist

✅ Backend service shows "Live" status
✅ Backend URL returns health check response
✅ Frontend service shows "Live" status  
✅ Frontend URL loads the dashboard
✅ Dashboard displays metrics
✅ No console errors in browser
✅ API docs accessible at `/docs`

---

**Deployment Time**: 15-20 minutes for both services
