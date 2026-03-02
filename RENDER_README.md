# 🚀 Render Deployment - Complete Setup Guide

## ⚠️ Important Note

**Blueprint deployment is deprecated.** Use separate service deployment instead.

---

## 🎯 What You'll Deploy

### Backend Web Service
- **What**: Python FastAPI server
- **Purpose**: REST API, metrics computation, data storage
- **Time**: ~10 minutes
- **Cost**: Free tier available

### Frontend Static Site
- **What**: React dashboard application  
- **Purpose**: User interface for viewing metrics
- **Time**: ~5 minutes
- **Cost**: Free

**Total deployment time: ~15 minutes**

---

## 📋 Prerequisites

Before you start:
- ✅ Code pushed to GitHub repository
- ✅ Render account created (free): https://render.com
- ✅ GitHub account connected to Render

---

## 🚀 Deployment Steps

### Choose Your Guide:

#### 🎨 **Visual Guide** (Recommended for first-time users)
Step-by-step with screenshots descriptions:
→ **[VISUAL_DEPLOY_GUIDE.md](VISUAL_DEPLOY_GUIDE.md)**

#### ⚡ **Quick Reference** (For experienced users)
Copy-paste commands and settings:
→ **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)**

#### 📖 **Detailed Guide** (Complete documentation)
Full instructions with troubleshooting:
→ **[DEPLOY_SEPARATE.md](DEPLOY_SEPARATE.md)**

---

## 🏃 Quick Start (TL;DR)

### Backend
1. New → Web Service
2. Build: `pip install -r backend/requirements.txt`
3. Start: `bash backend/start_render.sh`
4. Add env: `PYTHON_VERSION = 3.11.0`
5. Deploy & copy URL

### Frontend
1. New → Static Site
2. Build: `cd frontend && npm install && npm run build`
3. Publish: `frontend/dist`
4. Add env: `VITE_API_URL = [your-backend-url]`
5. Deploy!

---

## ✅ Post-Deployment Checklist

### Backend
- [ ] Status shows "Live"
- [ ] URL returns JSON: `{"status":"healthy",...}`
- [ ] Logs show "Data seeding completed successfully!"
- [ ] API docs work: `/docs`

### Frontend
- [ ] Status shows "Live"
- [ ] Dashboard loads in browser
- [ ] Factory metrics visible (purple section at top)
- [ ] 6 worker cards displayed
- [ ] 6 workstation cards displayed
- [ ] No console errors (press F12)

---

## 🔗 Your Live URLs

Fill these in after deployment:

```
Backend API:  https://_______________________________.onrender.com
Frontend:     https://_______________________________.onrender.com
API Docs:     https://_______________________________.onrender.com/docs
```

---

## 🆘 Common Issues & Solutions

### Frontend Shows "Failed to load data"

**Cause**: Frontend can't reach backend

**Fix**:
1. Go to frontend service → Environment
2. Verify `VITE_API_URL` matches your backend URL
3. No trailing slash!
4. Manual Deploy → "Clear build cache & deploy"

### Backend Won't Start

**Cause**: Build or start command error

**Fix**:
1. Check Logs tab for specific error
2. Verify build command: `pip install -r backend/requirements.txt`
3. Verify start command: `bash backend/start_render.sh`
4. Check Python version env var: `3.11.0`

### Slow First Load (30-60 seconds)

**This is expected!**
- Free tier services sleep after 15 min of inactivity
- First request wakes service (cold start)
- Subsequent requests are fast
- Upgrade to paid tier ($7/mo) for always-on

### Database Empty After Restart

**Cause**: No persistent disk configured

**Fix**:
1. Go to backend service → Disks
2. Add disk:
   - Name: `backend-data`
   - Mount: `/opt/render/project/src/backend/data`
   - Size: 1 GB

---

## 💰 Cost Breakdown

### Free Tier (Perfect for Testing)
- Backend: Free (750 hours/month)
- Frontend: Free (unlimited)
- **Total: $0/month**

**Limitations:**
- Services sleep after 15 minutes
- Cold start delay on first request
- Shared resources

### Starter (Recommended for Production)
- Backend: $7/month (always-on, better resources)
- Frontend: Free
- **Total: $7/month**

**Benefits:**
- No cold starts
- Dedicated resources
- Better performance

---

## 🔄 Auto-Deployment

After initial setup, deployments are automatic:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Render automatically:
# 1. Detects push
# 2. Runs build
# 3. Deploys updates
# 4. Zero downtime
```

---

## 📚 Additional Resources

### Configuration Details
- **Backend Config**: [backend/RENDER_CONFIG.md](backend/RENDER_CONFIG.md)
- **Frontend Config**: [frontend/RENDER_CONFIG.md](frontend/RENDER_CONFIG.md)

### Other Deployment Options
- **Full Documentation**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Docker Compose**: [docker-compose.yml](docker-compose.yml)
- **Local Development**: [QUICKSTART.md](QUICKSTART.md)

### API Documentation
- **README**: [README.md](README.md)
- **Postman Collection**: [postman_collection.json](postman_collection.json)

---

## 🎓 Learn More

### Render Documentation
- Docs: https://docs.render.com
- Status: https://status.render.com
- Support: support@render.com

### Application Features
- Worker productivity tracking
- Workstation utilization metrics
- Factory-wide analytics
- Event ingestion API
- Real-time dashboard

---

## 🎯 Success Metrics

Your deployment is successful when:
- ✅ Both services show "Live" status
- ✅ Frontend displays complete dashboard
- ✅ Backend API responds to requests
- ✅ Data persists across restarts
- ✅ No errors in logs or console

---

## 🚀 Next Steps After Deployment

1. **Test API**: Try POST `/api/events` with sample data
2. **Monitor**: Check Metrics tab for usage stats
3. **Custom Domain**: Add your own domain (optional)
4. **Scale**: Upgrade plan if needed
5. **Share**: Give your dashboard URL to team!

---

## 📞 Need Help?

1. **Check Logs**: Dashboard → Service → Logs tab
2. **Review Guides**: See documentation links above
3. **Common Issues**: Check troubleshooting section
4. **Contact Support**: support@render.com

---

**Ready to deploy?**

👉 Start with **[VISUAL_DEPLOY_GUIDE.md](VISUAL_DEPLOY_GUIDE.md)** for step-by-step instructions!

---

**Deployment status**: ⏳ Not deployed | ✅ Deployed

*Update this status after successful deployment!*
