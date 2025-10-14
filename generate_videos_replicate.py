"""
Tesla Sales Strategy - AI Video Generation with Replicate (Free, No GPU)
Uses AnimateDiff and ZeroscopeV2 models via Replicate API
"""
import os
import replicate
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Get API keys from environment
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
if not REPLICATE_API_TOKEN:
    print("⚠️  REPLICATE_API_TOKEN not found in .env file")
    print("📝 Get your free API token from: https://replicate.com/account/api-tokens")
    print("💡 Add it to your .env file: REPLICATE_API_TOKEN=your_token_here")
    exit(1)

# Initialize Replicate client
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# AI Video Prompts for Tesla Sales (optimized for short-form video generation)
VIDEO_PROMPTS = [
    {
        "id": "tesla_delivery",
        "title": "Tesla Model Y Delivery Day",
        "prompt": "Cinematic shot of excited person receiving Tesla Model Y keys at delivery center, walking to white Tesla, sitting in driver seat smiling, natural lighting, photorealistic",
        "duration": 3,
        "target": "18-34 tech enthusiasts"
    },
    {
        "id": "autopilot_demo",
        "title": "Family Autopilot Experience",
        "prompt": "Inside Tesla, family amazed as steering wheel drives itself on highway, hands off wheel, kids cheering in backseat, parents smiling, natural daylight, photorealistic",
        "duration": 3,
        "target": "25-45 family buyers"
    },
    {
        "id": "supercharger",
        "title": "Supercharger Speed Demo",
        "prompt": "Tesla Supercharger station, person plugging in charging cable, phone showing rapid charging progress, thumbs up gesture, modern outdoor setting, photorealistic",
        "duration": 3,
        "target": "EV-curious consumers"
    },
    {
        "id": "acceleration",
        "title": "Tesla Performance Test",
        "prompt": "Tesla Model Y drag race launch, intense acceleration from starting line, driver excited expression, multiple camera angles, dramatic racing cinematography, photorealistic",
        "duration": 3,
        "target": "Performance enthusiasts 20-40"
    },
    {
        "id": "interior_tech",
        "title": "Tesla Interior Tech Showcase",
        "prompt": "Person exploring Tesla touchscreen interface, minimalist dashboard, Netflix and games on screen, panoramic glass roof, clean modern aesthetic, photorealistic",
        "duration": 3,
        "target": "Tech lovers, luxury seekers"
    }
]

def generate_video_replicate(prompt_data, model="zeroscope"):
    """
    Generate video using Replicate API (Free tier available)
    
    Models:
    - zeroscope: Fast, good quality, free tier friendly
    - animatediff: Higher quality, slightly slower
    """
    try:
        print(f"\n🎬 Generating: {prompt_data['title']}")
        print(f"📝 Prompt: {prompt_data['prompt'][:80]}...")
        print(f"🎯 Target: {prompt_data['target']}")
        print(f"⏱️  Duration: {prompt_data['duration']}s")
        
        if model == "zeroscope":
            # ZeroscopeV2 - Fast and free-tier friendly
            print("🚀 Using ZeroscopeV2 XL (576x320, fast generation)")
            output = replicate.run(
                "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
                input={
                    "prompt": prompt_data['prompt'],
                    "num_frames": 24,  # ~1 second at 24fps
                    "num_inference_steps": 25,
                    "guidance_scale": 17.5,
                    "width": 576,
                    "height": 320
                }
            )
        else:
            # AnimateDiff - Higher quality alternative
            print("🎨 Using AnimateDiff (512x512, better quality)")
            output = replicate.run(
                "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48a9f",
                input={
                    "prompt": prompt_data['prompt'],
                    "num_frames": 16,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 25
                }
            )
        
        # Download the video
        video_url = output
        if isinstance(output, list):
            video_url = output[0]
        
        print(f"✅ Video generated: {video_url}")
        
        # Save video locally
        video_filename = f"generated_videos/{prompt_data['id']}.mp4"
        os.makedirs('generated_videos', exist_ok=True)
        
        print(f"💾 Downloading video...")
        response = requests.get(video_url)
        with open(video_filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Saved to: {video_filename}")
        
        return {
            "id": prompt_data["id"],
            "title": prompt_data["title"],
            "video_url": video_url,
            "local_path": video_filename,
            "prompt": prompt_data["prompt"],
            "status": "completed",
            "model": model
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "id": prompt_data["id"],
            "title": prompt_data["title"],
            "error": str(e),
            "status": "failed"
        }

def generate_all_videos(model="zeroscope"):
    """Generate all Tesla sales videos"""
    print("🚀 Tesla Sales Strategy - AI Video Generation")
    print("=" * 70)
    print(f"\n📹 Using Replicate API with {model.upper()} model")
    print("💡 Free tier available - No GPU required!\n")
    
    results = []
    
    for i, prompt_data in enumerate(VIDEO_PROMPTS, 1):
        print(f"\n[{i}/{len(VIDEO_PROMPTS)}] Processing...")
        result = generate_video_replicate(prompt_data, model=model)
        results.append(result)
        print("-" * 70)
        
        # Small delay to respect API rate limits
        if i < len(VIDEO_PROMPTS):
            print("⏳ Waiting 3 seconds before next generation...")
            time.sleep(3)
    
    print("\n✅ Video generation complete!")
    print(f"📊 Generated {len([r for r in results if r['status'] == 'completed'])}/{len(results)} videos")
    
    # Save results
    with open('generated_videos.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n💾 Results saved to: generated_videos.json")
    print("\n🎯 Next Steps:")
    print("1. Review generated videos in generated_videos/ folder")
    print("2. Post to TikTok with tracking links")
    print("3. Monitor conversions on dashboard")
    
    return results

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TESLA SALES STRATEGY - AI VIDEO GENERATION WITH REPLICATE")
    print("=" * 70 + "\n")
    
    # Generate videos using ZeroscopeV2 (fast, free-tier friendly)
    results = generate_all_videos(model="zeroscope")
    
    print("\n" + "=" * 70)
    print("✅ COMPLETE - Ready for TikTok deployment!")
    print("=" * 70)
