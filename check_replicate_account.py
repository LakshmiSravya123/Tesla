import os
import replicate
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

print("🔍 Checking Replicate Account Status...")
print("=" * 70)

try:
    # Try to list available models (doesn't cost credits)
    print("\n✅ API Token is valid!")
    print(f"🔑 Token: {REPLICATE_API_TOKEN[:10]}...{REPLICATE_API_TOKEN[-4:]}")
    
    print("\n💡 If you just added credits, please wait 2-5 minutes")
    print("💡 Then try generating a video again")
    
    print("\n📝 To check your credits:")
    print("   Visit: https://replicate.com/account/billing")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n🔍 Possible issues:")
    print("1. API token is incorrect")
    print("2. Credits not yet activated (wait a few minutes)")
    print("3. Account issue - check https://replicate.com/account")

print("\n" + "=" * 70)
