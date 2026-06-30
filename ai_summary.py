# ai_summary.py
import streamlit as st
from google import genai

# আপনার সাকসেসফুলি জেনারেট করা Gemini API Key
GEMINI_API_KEY = "AQ.Ab8RN6Ig_hYQJXHRS-RxSTWkW_6Bz3tZ-Y-2srr7jKAlvwQlAA"

def get_gemini_client():
    """Gemini Client ইনিশিয়েলাইজ করার হেল্পার ফাংশন"""
    if not GEMINI_API_KEY:
        return None
    try:
        # নতুন এসডিকে অনুযায়ী ক্লায়েন্ট তৈরি
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Client Initialization Error: {e}")
        return None

def analyze_memory_with_gemini(text):
    """মেমোরি সেভ করার সময় ইমোশন ও সেন্টিমেন্ট স্কোর অ্যানালাইসিস করবে"""
    client = get_gemini_client()
    if not client:
        return "Neutral", 0.0
        
    prompt = f"""
    Analyze the emotion and sentiment of this relationship journal entry.
    You must respond in exactly one line with two values separated by a comma.
    Format: <EMOTION>, <SENTIMENT_SCORE>
    
    Allowed Emotions: Love, Joy, Sadness, Conflict, Reconciliation, Long Distance, Celebration, Support, Loneliness, Neutral
    Sentiment Score: A single number between -1.0 and 1.0
    
    Example Output: Love, 0.85
    
    Journal Entry: "{text}"
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        res_text = response.text.strip()
        
        # ক্লিনআপ
        res_text = res_text.replace("*", "").replace("`", "").strip()
        
        if "," in res_text:
            parts = res_text.split(",")
            emotion = parts[0].strip()
            sentiment = float(parts[1].strip())
            return emotion, round(sentiment, 2)
            
        return "Neutral", 0.0
    except Exception as e:
        print(f"Gemini Error during generation: {e}")
        return "Neutral", 0.0

def generate_dashboard_insights(all_memories_text, insight_type="reflection"):
    """ড্যাশবোর্ডের রিফ্লেকশন, অ্যানিভার্সারি স্টোরি এবং ফিউচার ডেট সাজেশন জেনারেট করবে"""
    client = get_gemini_client()
    if not client or not all_memories_text.strip():
        return "Write more memories to unlock Gemini insights! ❤️"
        
    prompts = {
        "reflection": "Based on these relationship memories, give a deep, warm relationship reflection, highlighting the current health of the bond and gentle feedback.",
        "story": "Using these memories, craft a beautiful, romantic anniversary story. Combine the highs and lows into a sweet narrative.",
        "date_suggestion": "Analyze the mood, weather, and locations of past memories, and suggest 3 unique, thoughtful future date ideas tailored for this couple."
    }
    
    full_prompt = f"{prompts.get(insight_type, prompts['reflection'])}\n\nMemories Data:\n{all_memories_text}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
        )
        return response.text
    except Exception:
        return "Gemini could not process this right now. 😐"