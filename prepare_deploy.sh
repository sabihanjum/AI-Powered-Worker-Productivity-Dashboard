#!/usr/bin/env bash
# Prepare for Render deployment

echo "=========================================="
echo "Prepare for Render Deployment"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "⚠️  Git repository not initialized!"
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository found"
fi

# Check if remote is set
REMOTE=$(git remote -v)
if [ -z "$REMOTE" ]; then
    echo ""
    echo "⚠️  No remote repository configured!"
    echo ""
    echo "Please add a remote repository:"
    echo "  git remote add origin https://github.com/yourusername/your-repo.git"
    echo ""
else
    echo "✅ Remote repository configured"
    echo "$REMOTE"
fi

echo ""
echo "=========================================="
echo "Pre-deployment Checklist"
echo "=========================================="
echo ""
echo "✅ Backend ready:"
echo "   - FastAPI application"
echo "   - requirements.txt"
echo "   - render_start.sh"
echo ""
echo "✅ Frontend ready:"
echo "   - React application"
echo "   - package.json"
echo "   - Vite build configuration"
echo ""
echo "✅ Deployment files:"
echo "   - render.yaml (Blueprint)"
echo "   - .renderignore"
echo "   - DEPLOYMENT.md"
echo ""
echo "=========================================="
echo "Next Steps"
echo "=========================================="
echo ""
echo "1. Commit and push your code:"
echo "   git add ."
echo "   git commit -m \"Prepare for Render deployment\""
echo "   git push origin main"
echo ""
echo "2. Go to Render Dashboard:"
echo "   https://dashboard.render.com/"
echo ""
echo "3. Create new Blueprint:"
echo "   - Click 'New' → 'Blueprint'"
echo "   - Connect your repository"
echo "   - Click 'Apply'"
echo ""
echo "4. After deployment:"
echo "   - Copy backend URL"
echo "   - Update frontend VITE_API_URL"
echo "   - Redeploy frontend"
echo ""
echo "📚 See RENDER_DEPLOY.md for detailed instructions"
echo ""
