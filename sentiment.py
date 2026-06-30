# sentiment.py
import ai_summary as ai_gemini

def analyze_sentiment(text):
    try:
        emotion, sentiment = ai_gemini.analyze_memory_with_gemini(text)
        # নিশ্চিত করা হচ্ছে যেন আউটপুট সবসময় একটি পিওর ফ্লোট (Float) নাম্বার হয়
        return float(sentiment)
    except Exception:
        return 0.0