# 🚀 Deploy Backend API to Render

## Step-by-Step Instructions

### 1. **Go to Render Dashboard**
- Visit: https://dashboard.render.com
- Sign in with GitHub

### 2. **Create New Web Service**
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repository: `LakshmiSravya123/Tesla`
- Click **"Connect"**

### 3. **Configure the Service**

Fill in these settings:

- **Name**: `tesla-dashboard-api`
- **Region**: Choose closest to you (e.g., Oregon, Ohio)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn server:app`
- **Instance Type**: `Free` (select Free tier)

### 4. **Add Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add these:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | Your OpenAI API key from .env file |
| `REPLICATE_API_TOKEN` | Your Replicate token from .env file |
| `PYTHON_VERSION` | `3.11.0` |

### 5. **Deploy**
- Click **"Create Web Service"**
- Wait 3-5 minutes for deployment
- You'll get a URL like: `https://tesla-dashboard-api.onrender.com`

### 6. **Update Frontend**

Once deployed, you need to update the frontend to use your API URL.

**Option A: Update HTML files locally**
```bash
# Replace API URLs in dashboard files
sed -i '' 's|window.location.origin|"https://YOUR-API-URL.onrender.com"|g' dashboard/*.html
git add dashboard/*.html
git commit -m "Update API endpoint to Render backend"
git push
```

**Option B: Use environment variable in Vercel**
1. Go to Vercel Dashboard: https://vercel.com/sravyas-projects-f5209810/tesla-sales-dashboard/settings/environment-variables
2. Add: `VITE_API_URL` = `https://YOUR-API-URL.onrender.com`
3. Redeploy

## 🎯 Your API Endpoints

Once deployed, your API will be available at:

- `https://YOUR-API-URL.onrender.com/api/health` - Health check
- `https://YOUR-API-URL.onrender.com/api/prompts` - Video prompts
- `https://YOUR-API-URL.onrender.com/api/market-data` - Tesla stock & EV market data
- `https://YOUR-API-URL.onrender.com/api/generate-video` - Generate videos
- `https://YOUR-API-URL.onrender.com/api/ai-insights` - AI analytics

## ⚠️ Important Notes

1. **Free Tier Limitations**:
   - Render free tier spins down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - 750 hours/month free

2. **Cold Starts**:
   - First API call may be slow
   - Subsequent calls are fast

3. **Keep Alive** (Optional):
   - Use a service like UptimeRobot to ping your API every 14 minutes
   - Prevents spin-down during active hours

## 🔧 Troubleshooting

If deployment fails:
1. Check build logs in Render dashboard
2. Verify all environment variables are set
3. Make sure `requirements.txt` includes `gunicorn`

## 📝 After Deployment

1. Test your API: `curl https://YOUR-API-URL.onrender.com/api/health`
2. Update frontend API URLs
3. Redeploy Vercel frontend
4. Your dashboard will now show live data! 🎉
