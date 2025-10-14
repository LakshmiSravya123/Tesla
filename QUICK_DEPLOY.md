# 🚀 Quick Deploy Guide - Backend + Frontend

## Current Status
✅ **Frontend**: Deployed on Vercel at https://tesla-sales-dashboard.vercel.app  
⏳ **Backend**: Not deployed yet (needed for live data)

---

## 🎯 Deploy Backend in 5 Minutes

### **Option 1: Render (Recommended - Free)**

1. **Go to Render**: https://dashboard.render.com/register
   - Sign up with GitHub

2. **Create Web Service**:
   - Click **"New +"** → **"Web Service"**
   - Select repository: `LakshmiSravya123/Tesla`
   - Click **"Connect"**

3. **Configure**:
   ```
   Name: tesla-dashboard-api
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn server:app
   Instance Type: Free
   ```

4. **Add Environment Variables**:
   - Click **"Advanced"** → **"Add Environment Variable"**
   - Add your API keys from `.env` file:
     - `OPENAI_API_KEY` = (your key)
     - `REPLICATE_API_TOKEN` = (your key)

5. **Deploy**:
   - Click **"Create Web Service"**
   - Wait 3-5 minutes
   - Copy your URL: `https://tesla-dashboard-api-XXXX.onrender.com`

6. **Update Frontend**:
   ```bash
   # In your terminal:
   cd /Users/sravyalu/Salestrend
   
   # Update config.js with your Render URL
   sed -i '' 's|https://tesla-dashboard-api.onrender.com|https://YOUR-ACTUAL-URL.onrender.com|g' dashboard/config.js
   
   # Update HTML files to use config
   # (I'll do this in next step)
   
   git add .
   git commit -m "Connect frontend to Render backend"
   git push
   ```

---

### **Option 2: Railway (Alternative - Free)**

1. **Go to Railway**: https://railway.app
2. **New Project** → **Deploy from GitHub**
3. Select `LakshmiSravya123/Tesla`
4. Add environment variables (same as above)
5. Railway will auto-detect Python and deploy

---

### **Option 3: Heroku (Paid but reliable)**

1. **Go to Heroku**: https://heroku.com
2. Create new app
3. Connect GitHub repo
4. Add buildpack: `heroku/python`
5. Add environment variables
6. Deploy

---

## 📊 What You'll Get

Once backend is deployed:

✅ **Live Tesla Stock Data** - Real-time TSLA price from Alpha Vantage  
✅ **EV Market Data** - Competitor stock prices  
✅ **AI Video Generation** - Generate videos via Replicate API  
✅ **AI Analytics** - ML-powered insights  
✅ **TikTok Trends** - Real trending hashtags  

---

## 🔧 After Backend Deployment

1. **Test your API**:
   ```bash
   curl https://YOUR-API-URL.onrender.com/api/health
   ```

2. **Update frontend** (I'll help with this)

3. **Redeploy Vercel** (automatic via GitHub)

4. **Done!** 🎉

---

## 💡 Tips

- **Free Tier**: Render free tier spins down after 15 min of inactivity
- **First Load**: May take 30 seconds to wake up
- **Keep Alive**: Use UptimeRobot.com to ping every 14 minutes (optional)

---

## 🆘 Need Help?

Just let me know which platform you want to use and I'll guide you through it!
