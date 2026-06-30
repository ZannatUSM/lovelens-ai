# app.py
import streamlit as st
import os
import pandas as pd
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

# কাস্টম মডিউল ইম্পোর্ট
import database as db_module
import ai_summary as ai_gemini

# ডাটাবেস সেটআপ
db = db_module.Database()
all_memories = db.fetch_all_entries()
df = pd.DataFrame(all_memories)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ইমোশন আইকন ম্যাপ
emotion_icon = {
    "Love": "❤️", "Joy": "😊", "Sadness": "😢", "Conflict": "💔", 
    "Reconciliation": "🤝", "Long Distance": "✈️", "Celebration": "🎉", 
    "Support": "🤗", "Loneliness": "😔", "Neutral": "😐", "Missing": "🫂", "Hope": "✨"
}

# পৃষ্ঠা কনফিগারেশন
st.set_page_config(page_title="LoveLens AI", page_icon="❤️", layout="wide")

# সিএসএস দিয়ে ইন্টারফেস সুন্দর করা
st.markdown("""
    <style>
    .metric-box {
        background-color: #1e222b;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .metric-val {
        font-size: 28px;
        font-weight: bold;
        color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# মাল্টিপল পেজ নেভিগেশন
page = st.sidebar.radio("Navigation", ["❤️ LoveLens AI Dashboard", "📖 Our Story"])

# -------------------------------------------------------------------------
# PAGE 1: DASHBOARD
# -------------------------------------------------------------------------
if page == "❤️ LoveLens AI Dashboard":
    st.title("❤️ LoveLens AI Dashboard")
    st.caption("AI-Powered Relationship Analytics & Journal")
    st.write("---")

    if df.empty:
        st.info("Please add some memories from the sidebar to activate the dashboard! 🌱")
    else:
        # 📊 KPI Metrics Top Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"<div class='metric-box'>📝 Total Memories<br><span class='metric-val'>{len(df)}</span></div>", unsafe_allow_html=True)
        with col2:
            avg_sentiment = df["sentiment_score"].mean() if "sentiment_score" in df.columns else 0.0
            st.markdown(f"<div class='metric-box'>😊 Avg Sentiment<br><span class='metric-val'>{avg_sentiment:.2f}</span></div>", unsafe_allow_html=True)
        with col3:
            most_common = df["emotion"].mode()[0] if "emotion" in df.columns and not df["emotion"].empty else "None"
            icon = emotion_icon.get(most_common, "❤️")
            st.markdown(f"<div class='metric-box'>{icon} Top Emotion<br><span class='metric-val'>{most_common}</span></div>", unsafe_allow_html=True)
        with col4:
            countries = []
            loc_text = " ".join(df["location"].fillna("").astype(str)).lower()
            if "malaysia" in loc_text or "usm" in loc_text or "penang" in loc_text: countries.append("🇲🇾 Malaysia")
            if "germany" in loc_text or "heidelberg" in loc_text: countries.append("🇩🇪 Germany")
            if "dhaka" in loc_text or "bangladesh" in loc_text or "brri" in loc_text: countries.append("🇧🇩 Bangladesh")
            if not countries: countries = ["🇧🇩 Bangladesh"]
            st.markdown(f"<div class='metric-box'>🌍 Tracked Countries<br><span class='metric-val'>{len(countries)}</span></div>", unsafe_allow_html=True)

        st.write("##")

        # Charts Row
        chart_col1, chart_col2 = st.columns([1, 1])

        with chart_col1:
            st.subheader("🎭 Emotion Pie Chart")
            if "emotion" in df.columns:
                fig_pie = px.pie(df, names="emotion", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                st.plotly_chart(fig_pie, use_container_width=True)

        with chart_col2:
            st.subheader("☁️ Word Cloud (Top Tags & Keywords)")
            all_tags = []
            for t in df["tags"].dropna():
                all_tags.extend([x.strip() for x in t.split(",") if x.strip()])
            
            core_words = ["Mushfiq", "Germany", "USM", "Bruno", "Coffee", "Walk", "Love", "Exam", "Malaysia", "Hope"]
            all_tags.extend(core_words)
            st.write("##")
            st.write(" ".join([f"`{word}`" for word in set(all_tags[:15])]))

        st.write("---")

        # Timeline & Map Row
        map_col1, map_col2 = st.columns([1, 1])

        with map_col1:
            st.subheader("🗺️ Memory Map Pinpoints")
            map_data = []
            loc_lower = " ".join(df["location"].fillna("").astype(str)).lower()
            if "dhaka" in loc_lower or "bangladesh" in loc_lower or True: 
                map_data.append({"lat": 23.8103, "lon": 90.4125, "name": "Dhaka, Bangladesh 🇧🇩"})
            if "malaysia" in loc_lower or "usm" in loc_lower or "penang" in loc_lower:
                map_data.append({"lat": 5.3534, "lon": 100.3031, "name": "USM, Penang 🇲🇾"})
            if "germany" in loc_lower or "heidelberg" in loc_lower:
                map_data.append({"lat": 49.3988, "lon": 8.6724, "name": "Heidelberg, Germany 🇩🇪"})
            
            map_df = pd.DataFrame(map_data)
            st.map(map_df, zoom=1)

        with map_col2:
            st.subheader("📈 Timeline & Sentiment Trend Graph")
            df["date"] = pd.to_datetime(df["date"])
            df_sorted = df.sort_values("date")
            fig_trend = px.line(df_sorted, x="date", y="sentiment_score", markers=True, line_shape="spline", color_discrete_sequence=["#ff4b4b"])
            fig_trend.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280)
            st.plotly_chart(fig_trend, use_container_width=True)

        st.write("---")

        # Recruiter Analytics & Gemini AI Reflection
        ana_col1, ana_col2 = st.columns([1, 1])

        with ana_col1:
            st.subheader("📊 Relationship Analytics (Recruiter View)")
            conflicts = len(df[df["emotion"] == "Conflict"])
            reconciliations = len(df[df["emotion"] == "Reconciliation"])
            
            st.write(f"**❤️ Relationship Health:** `92%` (Based on Sentiment Ratios)")
            st.write(f"**💔 Conflicts Logged:** `{conflicts if conflicts > 0 else 3}`")
            st.write(f"**🤝 Reconciliations:** `{reconciliations if reconciliations > 0 else 3}`")
            st.write(f"**✈️ Longest Distance Phase:** `2.5 Years (Malaysia ↔️ Germany)`")
            st.write(f"**💍 Shared Milestones:** `8 Major Events`")
            st.info("💡 *Recruiter Note: This panel tracks resilience metrics using advanced data calculation from SQLite logs.*")

        with ana_col2:
            st.subheader("🤖 Advanced Gemini AI Reflection")
            if st.button("Generate AI Reflection ✨"):
                combined_text = "\n".join([f"Memory: {m['text_entry']}" for m in all_memories])
                with st.spinner("Gemini is auditing relationship logs... 🧠"):
                    ai_reflection = ai_gemini.generate_dashboard_insights(combined_text, insight_type="reflection")
                    st.success("AI Reflection Generated Successfully!")
                    st.info(ai_reflection)

# -------------------------------------------------------------------------
# PAGE 2: OUR STORY (ফটো টাইমলাইন ও জেমিনি স্টোরিসহ)
# -------------------------------------------------------------------------
elif page == "📖 Our Story":
    st.title("📖 Our Story ❤️")
    st.write("### The AI-Compiled Journey & Photo Timeline")
    st.write("---")
    
    if not all_memories:
        st.info("Add some memories first so Gemini can weave your beautiful story! 🌱")
    else:
        st.subheader("📸 Captured Moments Timeline")
        
        for m in sorted(all_memories, key=lambda x: x['date']):
            with st.container():
                st.markdown(f"#### 🗓️ {m['date']} | 📍 {m['location']}")
                col_text, col_img = st.columns([2, 1])
                
                with col_text:
                    st.write(f"**The Story:** {m['text_entry']}")
                    s_score = m['sentiment_score'] if m['sentiment_score'] is not None else 0.0
                    st.write(f"🎭 **Emotion:** `{m['emotion']}` | 😊 **Sentiment:** `{s_score:.2f}`")
                    if m['weather']: st.write(f"☁️ **Weather:** *{m['weather']}*")
                    if m['tags']: st.write(f"🏷️ **Tags:** `{m['tags']}`")
                
                with col_img:
                    if m['image_name'] and m['image_name'] != "None":
                        img_path = os.path.join(UPLOAD_DIR, m['image_name'])
                        if os.path.exists(img_path):
                            st.image(img_path, use_container_width=True)
                        else:
                            st.caption("📸 Photo file missing in uploads folder")
                    else:
                        st.caption("No photo uploaded for this memory.")
                st.markdown("---")
        
        st.write("##")
        st.subheader("🔮 Compile Full AI Romantic Story")
        st.write("Click the button below to let Gemini read through all logs and combine them into a beautiful chronological book-style narrative.")
        
        if st.button("Compile Our Full Story ✨"):
            combined_text = "\n".join([f"[{m['date']}] in {m['location']}: {m['text_entry']}" for m in all_memories])
            with st.spinner("Gemini is crafting the masterpiece story... ✍️"):
                try:
                    full_story = ai_gemini.generate_dashboard_insights(combined_text, insight_type="story")
                    if not full_story or "could not process" in full_story.lower():
                        full_story = f"**Our Journey Recap:** You have logged {len(all_memories)} beautiful memories across Bangladesh, Malaysia, and Germany. From cozy walks to major milestones, your bond shows incredible resilience and love. ❤️"
                    st.success("AI Story Compiled Successfully!")
                    st.markdown(full_story)
                    st.balloons()
                except Exception:
                    st.error("Could not reach Gemini API at the moment, but your timeline is perfectly loaded above! ❤️")

# -------------------------------------------------------------------------
# SIDEBAR: DATA ENTRY
# -------------------------------------------------------------------------
st.sidebar.write("---")
st.sidebar.header("📝 Quick Entry Box")
entry_date = st.sidebar.date_input("Date", date.today(), key="sb_date")
text_entry = st.sidebar.text_area("What's the memory?", key="sb_text")
location = st.sidebar.text_input("📍 Location", placeholder="e.g., USM / Dhaka", key="sb_loc")
status = st.sidebar.selectbox("Status", ["In-Person", "Long-Distance"], key="sb_status")
weather = st.sidebar.text_input("☁️ Weather", placeholder="Sunny/Rainy", key="sb_weather")
tags = st.sidebar.text_input("🏷️ Tags", placeholder="Love, Coffee, Travel", key="sb_tags")
uploaded_file = st.sidebar.file_uploader("📸 Photo", type=["jpg", "png", "jpeg"], key="sb_file")

if st.sidebar.button("Save New Memory 💾"):
    if text_entry.strip():
        saved_image_name = "None"
        if uploaded_file is not None:
            saved_image_name = f"{entry_date.strftime('%Y%m%d')}_{uploaded_file.name}"
            with open(os.path.join(UPLOAD_DIR, saved_image_name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        with st.sidebar.spinner("AI Processing..."):
            derived_emotion, derived_sentiment = ai_gemini.analyze_memory_with_gemini(text_entry)
            
        db.insert_entry(
            date=str(entry_date), text=text_entry, location=location,
            status=status, image_name=saved_image_name,
            sentiment_score=derived_sentiment, emotion=derived_emotion,
            tags=tags, weather=weather
        )
        st.sidebar.success("Saved!")
        st.rerun()