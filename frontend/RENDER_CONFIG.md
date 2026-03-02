# Render Deployment Configuration - Frontend Service

## Service Type
Static Site

## Repository
Connect your GitHub repository: AI-Powered-Worker-Productivity-Dashboard

## Basic Configuration

### Name
```
worker-productivity-frontend
```

### Branch
```
main
```

### Root Directory
```
(leave empty)
```

## Build Settings

### Build Command
```bash
cd frontend && npm install && npm run build
```

### Publish Directory
```
frontend/dist
```

## Environment Variables

**IMPORTANT**: Set this BEFORE deploying!

| Key | Value | Description |
|-----|-------|-------------|
| `VITE_API_URL` | `https://worker-productivity-backend.onrender.com` | Your backend URL (no trailing slash) |

**⚠️ Replace with your actual backend URL from the backend deployment!**

## Plan

- **Free Tier**: ✅ Perfect for static sites (no limitations)

## Auto Deploy

✅ Enable Auto-Deploy from `main` branch

## Deployment Steps

1. **Complete backend deployment first** and get its URL
2. Click "Create Static Site"
3. Add environment variable with your backend URL
4. Wait 3-5 minutes for build
5. Visit your frontend URL!

## Expected Build Output

```
> cd frontend && npm install && npm run build

added 200 packages in 15s

> vite build

vite v5.0.12 building for production...
✓ 150 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.30 kB
dist/assets/index-a1b2c3d4.css   5.23 kB │ gzip:  1.45 kB
dist/assets/index-x1y2z3w4.js   150.12 kB │ gzip: 48.32 kB
✓ built in 3.45s
```

## Deploy Configuration

### Headers (Optional - for better caching)

Add these headers in Render dashboard:

```
/*
  Cache-Control: public, max-age=0, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable
```

### Redirects/Rewrites (Optional)

For SPA routing:
```
/*  /index.html  200
```

## What Gets Deployed

✅ Optimized React production build
✅ Minified JavaScript and CSS
✅ Compressed assets
✅ CDN distribution
✅ HTTPS enabled automatically

## Frontend Features

After deployment:
- Modern, responsive dashboard
- Real-time metrics display
- Worker/workstation filtering
- Auto-refresh functionality
- Mobile-friendly design

## Pages

- `/` - Main dashboard
- All routes handled by React Router

## API Integration

Frontend connects to backend via:
- Base URL: `VITE_API_URL` environment variable
- CORS: Already configured in backend
- Endpoints: All `/api/*` routes

## Troubleshooting

### Build Fails

**Error: Cannot find package.json**
- Build command should include: `cd frontend`
- Path: `cd frontend && npm install && npm run build`

**Error: npm install fails**
- Check `frontend/package.json` exists
- Verify Node version compatibility

### App Shows Error

**"Failed to load data"**
1. Check `VITE_API_URL` is set correctly
2. Verify backend URL is accessible
3. Check browser console for CORS errors
4. Ensure backend is running

**Blank page**
1. Check browser console (F12)
2. Verify publish directory: `frontend/dist`
3. Check build completed successfully

### Environment Variable Not Working

1. Must rebuild after changing env vars
2. Go to "Manual Deploy" tab
3. Click "Clear build cache & deploy"
4. Environment variables are embedded at build time

## Testing Deployment

### Test API Connection
Open browser console on your frontend:
```javascript
fetch('https://your-backend.onrender.com/api/metrics/dashboard')
  .then(r => r.json())
  .then(d => console.log(d))
```

### Verify Environment
Check the API calls in Network tab (F12) - should point to your backend URL.

## Update Frontend

### Update Code
```bash
git push origin main
# Auto-deploys!
```

### Update Environment Variable
1. Go to Render Dashboard
2. Select frontend service
3. Environment tab
4. Update `VITE_API_URL`
5. **Important**: Trigger manual deploy
6. Click "Clear build cache & deploy"

## Performance

**Load Time:**
- First load: ~500ms
- Cached load: ~100ms

**CDN:**
- Global distribution
- Automatic edge caching
- Brotli compression

## Custom Domain (Optional)

Add your own domain:
1. Go to Settings → Custom Domain
2. Add domain (e.g., dashboard.yourcompany.com)
3. Update DNS records as shown
4. HTTPS auto-configured

## URLs

After deployment, you'll have:

- **Dashboard**: `https://worker-productivity-frontend.onrender.com`
- This is your main application URL to share!

## Success Checklist

✅ Build completes without errors
✅ Publish directory contains index.html
✅ Environment variable `VITE_API_URL` is set
✅ Frontend URL loads the dashboard
✅ Factory metrics display at top
✅ Worker cards display
✅ Workstation cards display
✅ Dropdowns work for filtering
✅ No errors in browser console
✅ Refresh button works

## Copy This Configuration

**For Render Dashboard:**
- Build Command: `cd frontend && npm install && npm run build`
- Publish Directory: `frontend/dist`
- Environment Variable: `VITE_API_URL` = `https://YOUR-BACKEND-URL.onrender.com`

---

**Ready to deploy?** Follow the steps in [DEPLOY_SEPARATE.md](../DEPLOY_SEPARATE.md)!
