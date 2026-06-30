# timeline.py
import streamlit as st
import os

def display_timeline(raw_data, UPLOAD_DIR, emotion_icon):
    """ডাটাবেস থেকে আসা মেমোরিগুলোকে সুন্দর ফেসবুক-স্টাইল কার্ডে দেখাবে"""
    st.markdown("## ❤️ Timeline")
    
    if not raw_data:
        st.info("No memories added yet. Start adding your beautiful moments from the sidebar! 👇")
        return

    # মেমোরিগুলোকে লেটেস্ট ডেট অনুযায়ী উল্টো করে সাজানো (Newest First)
    sorted_data = sorted(raw_data, key=lambda x: x["date"], reverse=True)

    for row in sorted_data:
        with st.container():
            # কার্ডের মতো ব্যাকগ্রাউন্ড তৈরি করার জন্য সিম্পল স্টাইলিং
            st.markdown(
                f"""
                <div style="
                    background-color: #1e1e2e; 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin-bottom: 20px;
                    border: 1px solid #313244;
                ">
                    <h3 style="color: #f5c2e7; margin-top: 0;">💖 {row['date']}</h3>
                    <p style="font-size: 16px; line-height: 1.6; color: #cdd6f4;">{row['text_entry']}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # মেটাডেটা কলাম (লোকেশন, স্ট্যাটাস, ওয়েদার ইত্যাদি)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"📍 Location: {row['location']}")
            with col2:
                st.caption(f"Status: {row['status']}")
            with col3:
                st.caption(f"☁️ Weather: {row['weather']}")
                
            # এআই অ্যানালাইসিস রো (ইমোশন ও সেন্টিমেন্ট স্কোর)
            current_emotion = row.get("emotion", "Neutral")
            icon = emotion_icon.get(current_emotion, "😐")
            sentiment_score = row.get("sentiment_score", 0.0)
            
            st.markdown(f"**{icon} Emotion:** {current_emotion} | **📊 Sentiment Score:** {sentiment_score}")
            
            # 🖼️ ইমেজ রেন্ডারিং (বুলেটপ্রুফ লজিক - Float/NaN এরর আটকাবে)
            image_name = row.get("image_name")
            if isinstance(image_name, str) and image_name.strip() and image_name.lower() != 'none':
                image_path = os.path.join(UPLOAD_DIR, image_name)
                if os.path.exists(image_path):
                    st.image(image_path, width=500)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.divider()