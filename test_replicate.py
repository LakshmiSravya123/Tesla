"""
Quick test script for Replicate video generation
"""
import os
import replicate
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

if not REPLICATE_API_TOKEN:
    print("❌ REPLICATE_API_TOKEN not found in .env file")
    print("\n📝 Setup Instructions:")
    print("1. Go to: https://replicate.com/account/api-tokens")
    print("2. Create a free account and get your API token")
    print("3. Add to .env file: REPLICATE_API_TOKEN=r8_your_token_here")
    exit(1)

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

print("🧪 Testing Replicate API Connection...")
print("=" * 70)

try:
    print("\n🎬 Generating test video (this takes ~30-45 seconds)...")
    print("📝 Prompt: 'Tesla Model Y driving on highway, cinematic'")
    
    output = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input={
            "prompt": "Tesla Model Y driving on highway, cinematic, photorealistic",
            "num_frames": 24,
            "num_inference_steps": 25,
            "guidance_scale": 17.5,
            "width": 576,
            "height": 320
        }
    )
    
    video_url = output if isinstance(output, str) else output[0]
    
    print("\n✅ SUCCESS! Video generated!")
    print(f"🔗 Video URL: {video_url}")
    print("\n💡 You can now use generate_videos_replicate.py to generate all videos")
    print("💡 Or run server_replicate.py to start the API server")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n🔍 Troubleshooting:")
    print("1. Check your API token is correct")
    print("2. Verify you have free credits: https://replicate.com/account")
    print("3. Check rate limits (free tier has limits)")

print("\n" + "=" * 70)
