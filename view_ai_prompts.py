# AI Video Generation Prompts for Tesla Sales Strategy

prompts = [
    {
        "scenario": "Young professional receiving Tesla Model Y delivery",
        "target": "18-34 tech enthusiasts",
        "ai_prompt": """
Create a 15-second TikTok video:
- Scene: Excited person getting keys to new Tesla Model Y
- Style: Authentic UGC, natural lighting, handheld camera
- Music: Upbeat trending TikTok sound
- Text overlay: "POV: Your dream car just arrived 🔥"
- Camera: Close-up of face showing genuine excitement, pan to car
- Emotion: Pure joy, disbelief, celebration
- End with: Person sitting in driver seat, huge smile
Use generic diverse face for broad appeal.
"""
    },
    {
        "scenario": "Family experiencing autopilot for first time",
        "target": "25-45 family-oriented buyers",
        "ai_prompt": """
Create a 20-second TikTok video:
- Scene: Family in Tesla, hands-free driving on highway
- Style: POV from backseat, showing reactions
- Music: Futuristic electronic beat
- Text overlay: "When the car drives itself 🤯"
- Camera: Switch between steering wheel (hands off) and amazed faces
- Emotion: Wonder, amazement, safety
- End with: Kids cheering, parents smiling
Show diverse family for maximum relatability.
"""
    },
    {
        "scenario": "Owner showing Supercharger experience",
        "target": "EV-curious consumers",
        "ai_prompt": """
Create a 18-second TikTok video:
- Scene: Plugging in at Tesla Supercharger station
- Style: Time-lapse of charging, educational
- Music: Chill electronic background
- Text overlay: "15 mins = 200 miles of range ⚡"
- Camera: Close-up of plug connecting, wide shot of station, phone app showing charge
- Emotion: Convenience, speed, modern tech
- End with: Thumbs up, "easier than gas station"
Use generic person to appeal to all demographics.
"""
    },
    {
        "scenario": "Tesla acceleration vs gas car comparison",
        "target": "Performance enthusiasts 20-40",
        "ai_prompt": """
Create a 25-second TikTok video:
- Scene: Side-by-side drag race, Tesla vs luxury gas car
- Style: Cinematic slow-motion, multiple angles
- Music: Intense bass drop on acceleration
- Text overlay: "0-60 in 3.5 seconds 💨"
- Camera: Split screen showing both cars, then Tesla pulling ahead
- Emotion: Adrenaline, superiority, power
- End with: Tesla far ahead, driver smirking
Generic driver face for wide appeal.
"""
    },
    {
        "scenario": "Interior tech showcase with minimalist design",
        "target": "Tech lovers, luxury seekers",
        "ai_prompt": """
Create a 20-second TikTok video:
- Scene: Sitting in Tesla, exploring touchscreen features
- Style: Clean, modern, Apple-style aesthetic
- Music: Minimal electronic, sophisticated
- Text overlay: "No buttons. Just vibes. 🎮"
- Camera: Close-ups of screen, panoramic glass roof, minimalist interior
- Emotion: Luxury, simplicity, future-forward
- End with: Swipe through Netflix, gaming, climate controls
Use diverse generic person for inclusivity.
"""
    }
]

print("🎬 AI VIDEO GENERATION PROMPTS FOR SORA2/RUNWAY/PIKA")
print("=" * 70)
print("\nThese prompts are designed for AI video tools like:")
print("- OpenAI Sora2")
print("- Runway Gen-2")
print("- Pika Labs")
print("- Synthesia")
print("\n" + "=" * 70 + "\n")

for i, p in enumerate(prompts, 1):
    print(f"\n{'='*70}")
    print(f"PROMPT #{i}: {p['scenario']}")
    print(f"{'='*70}")
    print(f"Target Audience: {p['target']}")
    print(f"\nAI PROMPT TO USE:")
    print(p['ai_prompt'])
    print(f"\n{'='*70}\n")

print("\n💡 HOW TO USE THESE PROMPTS:")
print("1. Copy any prompt above")
print("2. Paste into Sora2, Runway, or Pika Labs")
print("3. Generate the video")
print("4. Add to TikTok with tracking link from campaign_tracking")
print("5. Monitor conversions via the dashboard")
print("\n✅ All prompts use 'generic faces' for broad demographic appeal")
