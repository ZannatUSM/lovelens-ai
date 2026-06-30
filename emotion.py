# emotion.py
import ai_summary as ai_gemini

def detect_emotion(text):
    try:
        emotion, sentiment = ai_gemini.analyze_memory_with_gemini(text)
        # নিশ্চিত করা হচ্ছে যেন কোনো স্ট্রিং এরর বা স্পেসের ঝামেলা না থাকে
        return str(emotion).strip()
    except Exception:
        return "Neutral"