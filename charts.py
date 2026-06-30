# charts.py
import streamlit as st
import pandas as pd

def render_analytics_charts(all_memories):
    """ডাটাবেসের মেমোরি থেকে ইমোশন এবং সেন্টিমেন্টের সুন্দর গ্রাফ দেখাবে"""
    if not all_memories:
        st.info("Not enough data to render charts yet. Keep adding memories! ❤️")
        return

    # ডেটাকে পান্ডাস ডাটাফ্রেমে কনভার্ট করা
    df = pd.DataFrame(all_memories)

    st.subheader("📈 Relationship Insights & Trends")

    # কলাম লেআউট তৈরি
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎭 Emotion Distribution")
        if "emotion" in df.columns and not df["emotion"].dropna().empty:
            emotion_counts = df["emotion"].value_counts()
            st.bar_chart(emotion_counts)
        else:
            st.caption("No emotion data available yet.")

    with col2:
        st.markdown("#### 📊 Sentiment Score Timeline")
        if "date" in df.columns and "sentiment_score" in df.columns:
            df_sorted = df.sort_values(by="date")
            chart_data = df_sorted.set_index("date")[["sentiment_score"]]
            st.line_chart(chart_data)
        else:
            st.caption("No sentiment trend data available yet.")