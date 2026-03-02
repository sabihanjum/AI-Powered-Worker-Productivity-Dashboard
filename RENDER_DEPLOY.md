# Render Deployment Quick Start

## 🚀 Deploy to Render in 5 Minutes

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub account
4. Select repository: `AI-Powered-Worker-Productivity-Dashboard`
5. Render will detect `render.yaml` automatically
6. Click **"Apply"**

### Step 3: Get Your URLs

After deployment completes (5-10 minutes):

- **Backend API**: `https://worker-productivity-backend.onrender.com`
- **Frontend**: `https://worker-productivity-frontend.onrender.com`
- **API Docs**: `https://worker-productivity-backend.onrender.com/docs`

### Step 4: Update Frontend Environment

1. Go to your frontend service in Render dashboard
2. Click **"Environment"**
3. Add environment variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://worker-productivity-backend.onrender.com`
4. Click **"Save Changes"**
5. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Step 5: Test Your Deployment

Visit `https://worker-productivity-frontend.onrender.com` to see your live dashboard!

---

## 📝 Important Notes

### Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month free tier

### Data Persistence
- Backend includes persistent disk (1GB) for SQLite database
- Data persists across deploys and restarts

### Cold Starts
If your app seems slow on first load after inactivity, this is normal for free tier. Subsequent requests will be fast.

---

## 🔧 Troubleshooting

**Frontend shows "Failed to load data":**
- Verify backend URL in frontend environment variables
- Wait for backend to finish cold start (~30 seconds)
- Check backend logs in Render dashboard

**Backend won't start:**
- Check logs in Render dashboard
- Verify all files are committed to GitHub
- Ensure `backend/requirements.txt` exists

**Database is empty:**
- Backend automatically seeds data on first start
- Check logs to confirm seeding completed
- Use admin endpoint to re-seed: `POST /api/admin/seed-data?days=7`

---

## 📚 Full Documentation

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🎯 Quick Commands

```bash
# View backend logs (if you have Render CLI)
render logs --service worker-productivity-backend

# Manual redeploy
# Just push to GitHub - Render auto-deploys!
git push origin main
```

---

**Need help?** Check [DEPLOYMENT.md](./DEPLOYMENT.md) for complete documentation!
