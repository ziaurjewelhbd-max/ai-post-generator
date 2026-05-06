import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ১. পেজ কনফিগারেশন (ব্রাউজার ট্যাবে যা দেখাবে)
st.set_page_config(
    page_title="AI Product Post Generator",
    page_icon="🛍️",
    layout="centered"
)

# ২. এপিআই কি সেটআপ
# আপনি যদি Streamlit Cloud-এর 'Secrets' অপশনে কি সেভ করেন তবে প্রথম লাইনটি কাজ করবে।
# আর সরাসরি কোডে দিতে চাইলে দ্বিতীয় লাইনটি ব্যবহার করুন (তবে এটি সিকিউর নয়)।
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # এখানে আপনার কি-টি সরাসরি দেওয়া আছে যাতে আপনি দ্রুত পরীক্ষা করতে পারেন
    api_key = "AIzaSyDpkDgZ92pdCNcaVOkEAqKVkJwUUyy9oaI"

genai.configure(api_key=api_key)

# ৩. ইউজার ইন্টারফেস ডিজাইন
st.title("📸 AI Product Post Generator")
st.markdown("প্রোডাক্টের ছবি আপলোড করুন আর এআই দিয়ে আকর্ষণীয় সোশ্যাল মিডিয়া পোস্ট লিখে নিন।")

# ৪. ইমেজ আপলোডার
uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি এখানে আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # ছবি দেখানো
    image = Image.open(uploaded_file)
    st.image(image, caption='প্রিভিউ', use_container_width=True)
    
    # অতিরিক্ত কিছু অপশন (ঐচ্ছিক)
    post_language = st.radio("ক্যাপশন কোন ভাষায় চান?", ["বাংলা", "English", "Banglish (বাংলা+English)"])

    # ৫. পোস্ট জেনারেশন বাটন
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই আপনার ছবিটি দেখছে এবং লিখছে...'):
            try:
                # Gemini 1.5 Flash মডেল ব্যবহার
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # প্রম্পট বা এআই-কে দেওয়া নির্দেশ
                prompt = f"""
                You are a professional social media manager. Look at this product image carefully.
                1. Identify the product.
                2. Write an engaging Facebook post with emojis.
                3. Write a catchy Instagram caption.
                4. Provide 10 relevant and trending hashtags.
                Language: {post_language}.
                Ensure the tone is friendly and persuasive for customers.
                """
                
                # আউটপুট জেনারেট করা
                response = model.generate_content([prompt, image])
                
                # রেজাল্ট প্রদর্শন
                st.success("তৈরি হয়ে গেছে!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে। এপিআই কি সঠিক আছে কি না চেক করুন। এরর: {e}")

# ৬. ফুটার বা নিচের অংশ
st.markdown("---")
st.caption("পাওয়ারড বাই Google Gemini AI")
