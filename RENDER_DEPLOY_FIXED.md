# 🚀 Deploy to Render - FIXED (No Pandas Build Errors)

## ✅ Problem Solved

The pandas compilation error has been fixed! I created a **minimal server** that works perfectly on Render's free tier.

---

## 📋 Step-by-Step Deployment

### **1. Go to Render**
- Visit: https://dashboard.render.com
- Sign up/login with GitHub

### **2. Create New Web Service**
- Click **"New +"** → **"Web Service"**
- Connect repository: `LakshmiSravya123/Tesla`
- Click **"Connect"**

### **3. Configure Service**

**IMPORTANT**: Use these exact settings:

```
Name: tesla-dashboard-api
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: (leave empty)
Runtime: Python 3
Build Command: pip install --upgrade pip && pip install -r requirements-minimal.txt
Start Command: gunicorn server_minimal:app --bind 0.0.0.0:$PORT
Instance Type: Free
```

### **4. Add Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add these two:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | (paste from your .env file) |
| `REPLICATE_API_TOKEN` | (paste from your .env file) |

To get values from .env:
```bash
cat /Users/sravyalu/Salestrend/.env
```

### **5. Deploy**
- Click **"Create Web Service"**
- Wait 2-3 minutes (much faster now!)
- ✅ Deployment should succeed!

### **6. Get Your API URL**

Once deployed, you'll see:
```
Your service is live at https://tesla-dashboard-api-XXXX.onrender.com
```

**Copy this URL!** You'll need it for the next step.

---

## 🔗 Connect Frontend to Backend

Once you have your Render URL, run these commands:

```bash
cd /Users/sravyalu/Salestrend

# Replace YOUR_RENDER_URL with your actual URL
export API_URL="https://tesla-dashboard-api-XXXX.onrender.com"

# Update analytics.html
sed -i '' "s|const API = window.location.origin;|const API = '$API_URL';|" dashboard/analytics.html

# Update videos.html  
sed -i '' "s|const API = window.location.origin;|const API = '$API_URL';|" dashboard/videos.html

# Commit and push
git add dashboard/*.html
git commit -m "Connect frontend to Render backend"
git push
```

Vercel will auto-redeploy and your dashboard will show **live data**! 🎉

---

## 🧪 Test Your API

After deployment, test it:

```bash
# Health check
curl https://YOUR-URL.onrender.com/api/health

# Get prompts
curl https://YOUR-URL.onrender.com/api/prompts

# Get market data
curl https://YOUR-URL.onrender.com/api/market-data
```

---

## 📊 What's Included

The minimal server includes:

✅ **Video Prompts** - 5 Tesla-themed prompts  
✅ **Market Data** - Tesla stock & EV competitor data  
✅ **Video Generation** - Replicate API integration  
✅ **Health Check** - API status endpoint  

**What's NOT included** (to avoid pandas):
- ❌ ML predictions (scikit-learn)
- ❌ Advanced analytics (pandas)

These features will show mock data instead.

---

## ⚠️ Important Notes

1. **Free Tier Limits**:
   - Spins down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - 750 hours/month free

2. **Cold Starts**:
   - First API call may be slow
   - Keep-alive services can help (optional)

3. **Environment Variables**:
   - Make sure to add both API keys
   - Without them, video generation won't work

---

## 🆘 Troubleshooting

**If build still fails:**
1. Check you're using `requirements-minimal.txt` (not `requirements.txt`)
2. Check start command is `gunicorn server_minimal:app`
3. Verify Python version is 3.10.0

**If API returns errors:**
1. Check environment variables are set
2. Check logs in Render dashboard
3. Test health endpoint first

---

## ✨ Next Steps

After deployment:
1. Test your API endpoints
2. Update frontend with your API URL
3. Push to GitHub
4. Vercel auto-redeploys
5. Enjoy live data! 🎉

---

**Ready to deploy? Follow the steps above and let me know your Render URL when it's ready!**
