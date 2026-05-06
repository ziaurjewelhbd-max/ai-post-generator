import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Post Generator", page_icon="🛍️")

# এপিআই কি সেটআপ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "AIzaSyDpkDgZ92pdCNcaVOkEAqKVkJwUUyy9oaI"

# কনফিগারেশন - এখানে আমরা ভার্সনটি ফিক্সড করে দেওয়ার চেষ্টা করছি
genai.configure(api_key=api_key)

st.title("📸 AI Social Media Post Generator")

uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='প্রিভিউ', use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই কাজ করছে...'):
            try:
                # সমাধান: সরাসরি লেটেস্ট মডেল নেম এবং ভার্সন এনফোর্স করা
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                
                # প্রম্পট
                prompt = "Identify this product from the image and write an engaging Facebook and Instagram post in Bengali with hashtags."
                
                # কন্টেন্ট জেনারেশন
                response = model.generate_content([prompt, image])
                
                st.success("সফল হয়েছে!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error("দুঃখিত, আপনার বর্তমান গুগল অ্যাকাউন্টটি এই এপিআই ভার্সন সাপোর্ট করছে না।")
                st.markdown("---")
                st.warning("⚠️ **এটি সমাধানের একমাত্র উপায়:**")
                st.write("আপনার বর্তমান জিমেইল বাদে অন্য একটি নতুন বা ভিন্ন জিমেইল দিয়ে [Google AI Studio](https://aistudio.google.com/) তে লগইন করুন এবং একটি নতুন API Key জেনারেট করে সেটি এখানে বসান।")
