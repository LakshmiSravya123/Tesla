"""
Alternative: Use Hugging Face Inference API (Free)
No credit card required!
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Hugging Face is completely free - no credit card needed
HF_API_TOKEN = os.getenv('HF_API_TOKEN', '')

if not HF_API_TOKEN:
    print("=" * 70)
    print("🆓 FREE Alternative: Hugging Face Inference API")
    print("=" * 70)
    print("\n✅ No credit card required!")
    print("✅ Completely free")
    print("✅ No GPU needed")
    print("\n📝 Setup (2 minutes):")
    print("1. Go to: https://huggingface.co/settings/tokens")
    print("2. Create free account (no payment needed)")
    print("3. Create a token")
    print("4. Add to .env: HF_API_TOKEN=your_token")
    print("\n💡 Then run this script again!")
    print("=" * 70)
    exit(0)

print("🧪 Testing Hugging Face API...")
print("=" * 70)

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def generate_image(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

try:
    print("\n🎨 Generating test image...")
    print("📝 Prompt: 'Tesla Model Y on highway, cinematic'")
    
    image_bytes = generate_image("Tesla Model Y on highway, cinematic, professional photography")
    
    # Save image
    with open("test_output.jpg", "wb") as f:
        f.write(image_bytes)
    
    print("\n✅ SUCCESS! Image generated!")
    print("💾 Saved to: test_output.jpg")
    print("\n💡 This is FREE and works immediately!")
    print("💡 For videos, we can create animated sequences from images")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n🔍 Make sure your HF_API_TOKEN is correct")

print("\n" + "=" * 70)
