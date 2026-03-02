# 📸 Visual Deployment Guide - Step by Step

This guide shows you exactly what to click in the Render dashboard.

---

## Part 1: Deploy Backend (10 minutes)

### Step 1: Create New Web Service

1. Go to https://dashboard.render.com/
2. Look for a blue button that says **"New +"** (top right)
3. Click it and select **"Web Service"**

### Step 2: Connect Repository

**You'll see a page titled "Create a new Web Service"**

1. If this is your first time:
   - Click **"Connect account"** under GitHub
   - Authorize Render to access your repositories
   
2. Find your repository:
   - Look for `AI-Powered-Worker-Productivity-Dashboard`
   - Click **"Connect"** button next to it

### Step 3: Configure Backend

**You'll now see a form with many fields. Fill them as follows:**

#### Basic Information
```
Name: worker-productivity-backend
Region: Oregon (US West)  [or closest to you]
Branch: main
Root Directory: [leave empty]
Runtime: Python 3
```

#### Build & Deploy Section
```
Build Command:
pip install -r backend/requirements.txt

Start Command:
bash backend/start_render.sh
```

#### Instance Type
```
Plan: Free
```

#### Advanced Section (Click "Advanced" to expand)

**Environment Variables:**
- Click **"Add Environment Variable"**
- Key: `PYTHON_VERSION`
- Value: `3.11.0`

**Persistent Disk (Optional but recommended):**
- Click **"Add Disk"**
- Name: `backend-data`
- Mount Path: `/opt/render/project/src/backend/data`
- Size: `1`

#### Auto-Deploy
```
✅ Auto-Deploy: Yes (keep checked)
```

### Step 4: Create Service

1. Scroll to bottom
2. Click big blue **"Create Web Service"** button
3. You'll be redirected to the service page

### Step 5: Wait for Deployment

**What to watch:**
- You'll see "In Progress" status
- Logs will scroll automatically
- Wait for these messages:
  - ✅ "Build successful"
  - ✅ "Data seeding completed successfully!"
  - ✅ "Your service is live 🎉"

**This takes 5-10 minutes**

### Step 6: Copy Backend URL

**Once deployed:**
1. At top of page, you'll see your service URL
2. It looks like: `https://worker-productivity-backend-xxxx.onrender.com`
3. **COPY THIS URL** - you need it for frontend!
4. Test it: Click the URL, should show `{"status":"healthy",...}`

---

## Part 2: Deploy Frontend (5 minutes)

### Step 7: Create Static Site

1. Go back to dashboard: https://dashboard.render.com/
2. Click **"New +"** (top right) again
3. This time select **"Static Site"**

### Step 8: Connect Same Repository

1. Find `AI-Powered-Worker-Productivity-Dashboard` again
2. Click **"Connect"**

### Step 9: Configure Frontend

**Fill in the form:**

#### Basic Information
```
Name: worker-productivity-frontend
Branch: main
Root Directory: [leave empty]
```

#### Build Settings
```
Build Command:
cd frontend && npm install && npm run build

Publish Directory:
frontend/dist
```

#### Environment Variables
**⚠️ IMPORTANT - Use YOUR backend URL from Step 6:**

- Click **"Add Environment Variable"**
- Key: `VITE_API_URL`
- Value: `https://worker-productivity-backend-xxxx.onrender.com`
  (Replace xxxx with your actual backend URL)

**Make sure there's NO trailing slash!**

#### Auto-Deploy
```
✅ Auto-Deploy: Yes (keep checked)
```

### Step 10: Create Static Site

1. Scroll to bottom
2. Click **"Create Static Site"** button
3. You'll be redirected to the service page

### Step 11: Wait for Build

**What to watch:**
- "In Progress" status
- Build logs scrolling
- Wait for: "Your site is live 🎉"

**This takes 3-5 minutes**

### Step 12: Test Your Deployment

**Once deployed:**
1. Click your frontend URL at top of page
2. It looks like: `https://worker-productivity-frontend-xxxx.onrender.com`
3. Should redirect to your dashboard
4. You should see:
   - 🏭 Factory metrics at top (purple gradient)
   - 👷 6 worker cards below
   - 🏗️ 6 workstation cards at bottom

**If you see these, congratulations! You're done! 🎉**

---

## Troubleshooting

### Backend "Live" but Frontend Shows Error

**Problem:** Dashboard says "Failed to load data"

**Solution:**
1. Go to frontend service in Render
2. Click **"Environment"** in left menu
3. Check `VITE_API_URL` value
4. Should match your backend URL exactly
5. If wrong, update it
6. Then click **"Manual Deploy"** tab
7. Click **"Clear build cache & deploy"**

### Backend Keeps Restarting

**Problem:** Backend shows "Live" then "Failed" repeatedly

**Solution:**
1. Click **"Logs"** tab
2. Look for error messages
3. Common fixes:
   - Verify build command is correct
   - Check start command has `bash backend/start_render.sh`
   - Ensure Python version is set

### First Load is Very Slow

**This is normal!**
- Free tier services sleep after 15 min
- First request takes 30-60 seconds
- Subsequent requests are fast
- Upgrade to paid for always-on

---

## Where to Find Things in Render Dashboard

### Service Page (after deployment)
```
├── Overview - Current status, URL
├── Logs - Real-time logs, errors
├── Metrics - CPU, Memory usage
├── Environment - Env variables
├── Settings - Service configuration
├── Manual Deploy - Force redeploy
└── Disk - Persistent storage (backend only)
```

### Key Locations
- **Service URL**: Top of Overview page (big link)
- **Logs**: Left sidebar → Logs tab
- **Env Variables**: Settings → Environment
- **Redeploy**: Manual Deploy → "Deploy latest commit"

---

## Quick Check After Deploy

### Backend Checklist
```
✅ Status shows "Live" (green)
✅ URL responds with JSON
✅ Logs show "Data seeding completed"
✅ /docs endpoint works
```

### Frontend Checklist
```
✅ Status shows "Live" (green)
✅ URL loads dashboard
✅ Factory metrics visible
✅ Worker cards visible
✅ Workstation cards visible
✅ No red errors in browser console (F12)
```

---

## What Each Service Does

### Backend (Web Service)
- Runs Python FastAPI server
- Hosts REST API endpoints
- Stores data in SQLite database
- Computes metrics

### Frontend (Static Site)
- Serves React application
- Shows dashboard interface
- Calls backend API
- Displays charts and metrics

---

## Update Your Deployment Later

**To deploy code changes:**
1. Make changes locally
2. Commit: `git commit -am "Update feature"`
3. Push: `git push origin main`
4. Render auto-deploys both services!
5. Check logs to confirm

**No manual steps needed!**

---

## Support

**If stuck:**
- Check service logs first (Logs tab)
- Review error messages
- Compare with this guide
- Contact Render support: support@render.com

---

**Need quick reference?** See **QUICK_DEPLOY.md** for copy-paste commands!

**Need detailed help?** See **DEPLOY_SEPARATE.md** for full instructions!
