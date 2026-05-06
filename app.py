import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজ সেটআপ
st.set_page_config(page_title="AI Product Post Generator", page_icon="🛍️")

# ২. নিরাপদভাবে এপিআই কি লোড করা (Streamlit Secrets থেকে)
try:
    # এটি Streamlit Cloud এর 'Secrets' অপশন থেকে কি-টি খুঁজে নেবে
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("এপিআই কি (API Key) পাওয়া যায়নি! দয়া করে Streamlit Settings-এ এটি সেট করুন।")
    st.stop()

# ৩. ইন্টারফেস
st.title("📸 AI Product Post Generator")
st.write("আপনার প্রোডাক্টের ছবি থেকে ফেসবুক ও ইন্সটাগ্রাম পোস্ট তৈরি করুন।")

uploaded_file = st.file_uploader("ছবি আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='আপনার আপলোড করা ছবি', use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই লিখছে...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "Analyze this image and write a catchy Facebook and Instagram post in Bengali for this product with hashtags."
                
                response = model.generate_content([prompt, image])
                st.success("সফলভাবে তৈরি হয়েছে!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"একটি সমস্যা হয়েছে: {e}")
