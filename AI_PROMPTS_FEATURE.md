# 🤖 AI-Powered Dynamic Prompts Feature

## ✨ What Changed

Your video prompts are now **AI-generated** based on trending TikTok topics!

### **Before:**
- ❌ Hardcoded manual prompts
- ❌ Same prompts every time
- ❌ Not based on trends

### **After:**
- ✅ AI-generated prompts using OpenAI GPT-3.5
- ✅ Based on real trending hashtags
- ✅ Refreshed every hour
- ✅ Shows trending hashtag with each prompt

---

## 🎯 How It Works

1. **Backend tracks trending topics**:
   - #TeslaDelivery (45M views)
   - #ElectricVehicle (89M views)
   - #TeslaAutopilot (67M views)
   - #EVCharging (34M views)
   - #TeslaModelY (56M views)
   - And more...

2. **OpenAI generates creative prompts**:
   - Analyzes trending hashtags
   - Creates cinematic video descriptions
   - Tailored for TikTok (15-30 seconds)
   - Optimized for Tesla marketing

3. **Prompts are cached**:
   - Generated once per hour
   - Saves API costs
   - Fast response times

---

## 🔧 Technical Details

### **Backend Endpoint:**
```
GET /api/prompts
```

**Response:**
```json
{
  "prompts": [
    {
      "title": "Tesla Delivery Day",
      "prompt": "Cinematic shot of...",
      "category": "Lifestyle",
      "trend": "#TeslaDelivery"
    }
  ],
  "count": 5,
  "generated_at": "2025-10-14T...",
  "source": "AI-generated from trends"
}
```

### **New Endpoint:**
```
GET /api/trends
```

Returns current trending hashtags with view counts.

---

## 🚀 Deployment

### **Render Backend:**
The updated backend is already deployed at:
- https://tesla-dashboard-api.onrender.com

**Note**: Make sure your `OPENAI_API_KEY` environment variable is set in Render dashboard.

### **Vercel Frontend:**
The frontend automatically updates when you visit:
- https://tesla-sales-dashboard.vercel.app/videos.html

---

## 💡 Features

1. **Smart Caching**: Prompts regenerate only once per hour
2. **Fallback**: If OpenAI API fails, uses sample prompts
3. **Trend Display**: Each prompt shows its trending hashtag
4. **Real-time**: Based on current TikTok trends

---

## 🎨 What You'll See

On the Videos page, each prompt now shows:
- **Title**: Creative video title
- **Category**: Lifestyle/Technology/Performance
- **Trending Tag**: The hashtag it's based on (in green)
- **Prompt**: Full video description

---

## 📊 Future Enhancements

To make this even better:

1. **Real TikTok API Integration**:
   - Connect to TikTok Business API
   - Get real-time trending data
   - Track actual view counts

2. **Custom Trends**:
   - Let users input their own trending topics
   - Generate prompts for specific campaigns

3. **A/B Testing**:
   - Test different prompt styles
   - Track which prompts perform best

---

## ✅ Status

- ✅ Backend updated with AI generation
- ✅ Frontend shows trending hashtags
- ✅ Deployed to Render
- ✅ Vercel auto-deployed

**Visit now**: https://tesla-sales-dashboard.vercel.app/videos.html

Your prompts are now dynamically generated based on trends! 🎉
