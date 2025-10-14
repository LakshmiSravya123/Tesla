#!/bin/bash

echo "🚀 Deploying Tesla Sales Dashboard to Vercel"
echo "=============================================="

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Install with: npm i -g vercel"
    exit 1
fi

echo ""
echo "📝 Step 1: Adding environment variables..."
echo ""

# Add OpenAI API Key
echo "Adding OPENAI_API_KEY..."
vercel env add OPENAI_API_KEY production <<< "$(grep OPENAI_API_KEY .env | cut -d '=' -f2-)"

# Add Replicate API Token
echo "Adding REPLICATE_API_TOKEN..."
vercel env add REPLICATE_API_TOKEN production <<< "$(grep REPLICATE_API_TOKEN .env | cut -d '=' -f2-)"

echo ""
echo "📦 Step 2: Deploying to Vercel..."
echo ""

# Deploy to production
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Visit your deployment URL"
echo "2. Test: https://your-url.vercel.app/api/health"
echo "3. Access dashboard: https://your-url.vercel.app/"
