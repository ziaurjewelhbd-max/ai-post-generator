import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Post Generator", page_icon="🛍️")

# এপিআই কি সেটআপ
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        # যদি Secrets-এ না থাকে তবে এখানে কি-টি সরাসরি দিয়ে চেক করতে পারেন
        api_key = "AIzaSyDpkDgZ92pdCNcaVOkEAqKVkJwUUyy9oaI"
    
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Key খুঁজে পাওয়া যায়নি।")
    st.stop()

st.title("📸 AI Product Post Generator")

uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='প্রিভিউ', use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই কাজ করছে...'):
            try:
                # 'gemini-1.5-flash-latest' ব্যবহার করলে মডেল নট ফাউন্ড এরর আসবে না
                model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
                
                prompt = "Analyze this image and write an engaging Facebook and Instagram post in Bengali for this product with hashtags."
                
                # ইমেজ ইনপুট নিয়ে কন্টেন্ট জেনারেট
                response = model.generate_content([prompt, image])
                
                st.success("তৈরি হয়ে গেছে!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"মডেল লোড করতে সমস্যা হচ্ছে। এরর: {e}")
                st.info("টিপস: আপনার requirements.txt ফাইলে google-generativeai এর লেটেস্ট ভার্সন আছে কি না নিশ্চিত করুন।")
