# 🚀 Quick Deploy Reference - Copy & Paste Ready

## Backend Service Settings

### In Render Dashboard → New → Web Service

**Basic:**
- Name: `worker-productivity-backend`
- Runtime: `Python 3`
- Branch: `main`

**Commands:**
```
Build: pip install -r backend/requirements.txt
Start: bash backend/start_render.sh
```

**Environment:**
```
PYTHON_VERSION = 3.11.0
```

**Optional Disk:**
```
Name: backend-data
Path: /opt/render/project/src/backend/data
Size: 1 GB
```

---

## Frontend Service Settings

### In Render Dashboard → New → Static Site

**Basic:**
- Name: `worker-productivity-frontend`
- Branch: `main`

**Commands:**
```
Build: cd frontend && npm install && npm run build
Publish: frontend/dist
```

**Environment (IMPORTANT - use YOUR backend URL):**
```
VITE_API_URL = https://worker-productivity-backend.onrender.com
```

**⚠️ Replace with your actual backend URL!**

---

## Deploy Order

1. ✅ Deploy Backend FIRST
2. ✅ Copy backend URL
3. ✅ Deploy Frontend with backend URL
4. ✅ Done!

---

## Test Commands

```bash
# Test backend
curl https://YOUR-BACKEND.onrender.com/

# Expected: {"status":"healthy",...}
```

Visit frontend URL in browser - should show dashboard!

---

## Common Issues

**Frontend can't connect:**
→ Update `VITE_API_URL` then "Clear build cache & deploy"

**Backend fails to start:**
→ Check logs for error, verify start command

**Cold start slow:**
→ Normal on free tier (30-60 sec first load)

---

## Your URLs (Fill these in)

```
Backend:  https://_________________________.onrender.com
Frontend: https://_________________________.onrender.com
API Docs: https://_________________________.onrender.com/docs
```

---

Need help? See **DEPLOY_SEPARATE.md** for full instructions!
