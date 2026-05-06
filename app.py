import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Post Generator", page_icon="🛍️")

# এপিআই কি সেটআপ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "AIzaSyDpkDgZ92pdCNcaVOkEAqKVkJwUUyy9oaI"

genai.configure(api_key=api_key)

st.title("📸 AI Product Post Generator")

uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='প্রিভিউ', use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই কাজ করছে...'):
            try:
                # এখানে কোনো 'models/' বা ভার্সন না দিয়ে সরাসরি নাম ব্যবহার করছি
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # প্রম্পটটিকে আরও সহজ করা হয়েছে
                prompt = "Identify this product and write an engaging social media post in Bengali."
                
                # কন্টেন্ট জেনারেট
                response = model.generate_content([prompt, image])
                
                st.success("তৈরি হয়ে গেছে!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # যদি এরর আসে, আমরা বর্তমান এভেলেবেল মডেলগুলো একবার চেক করে নেব
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে।")
                st.write(f"এরর ডিটেইলস: {e}")
