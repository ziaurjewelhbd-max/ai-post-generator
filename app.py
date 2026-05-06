import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. এপিআই কি সেটআপ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "AIzaSyDpkDgZ92pdCNcaVOkEAqKVkJwUUyy9oaI"

genai.configure(api_key=api_key)

# ২. পেজ ডিজাইন
st.title("📸 AI Social Media Post Generator")

uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি দিন", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো"):
        with st.spinner("এআই আপনার ছবি নিয়ে কাজ করছে..."):
            try:
                # মডেলটির নাম সঠিকভাবে এখানে দেওয়া হলো
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # প্রম্পট
                prompt = "Analyze this product image and write a detailed Facebook and Instagram post in Bengali with emojis and hashtags."
                
                # রেজাল্ট জেনারেশন
                response = model.generate_content([prompt, image])
                
                st.success("হয়ে গেছে!")
                st.markdown(response.text)
                
            except Exception as e:
                # যদি এখনো এরর আসে, আমরা অন্য একটি সাপোর্ট মডেল ট্রাই করব
                try:
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content([prompt, image])
                    st.success("হয়ে গেছে (Pro Model)!")
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Error: {e2}")
