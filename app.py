import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Post Generator", page_icon="🛍️")

# এপিআই কি সেটআপ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # এখানে সরাসরি কী দিলেও কাজ করবে যদি সিক্রেটস কাজ না করে
    api_key = "আপনার_নতুন_কী_এখানে"

# ১. এপিআই কনফিগার করার সময় সরাসরি ভার্সন ফিক্স করে দেওয়া
genai.configure(api_key=api_key)

st.title("📸 AI Product Post Generator")

uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='প্রিভিউ', use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই কাজ করছে...'):
            try:
                # Gemini 1.5 Flash মডেল সরাসরি কল করা
                # কোনো 'models/' প্রিফিক্স ব্যবহার করবেন না
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                
                # প্রম্পট
                prompt = "Analyze this product image and write a catchy Facebook and Instagram post in Bengali."
                
                # ছবি থেকে কন্টেন্ট জেনারেশন
                response = model.generate_content([prompt, image])
                
                st.success("তৈরি হয়ে গেছে!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # যদি ফ্ল্যাশ মডেল কাজ না করে, আমরা ডিফল্ট 'gemini-pro-vision' ট্রাই করব (এটি পুরনো কিন্তু স্টেবল)
                try:
                    st.info("বিকল্প মডেলে চেষ্টা করা হচ্ছে...")
                    backup_model = genai.GenerativeModel(model_name='gemini-pro-vision')
                    response = backup_model.generate_content([prompt, image])
                    st.success("সফল হয়েছে (Backup Model)!")
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"দুঃখিত, এপিআই সাপোর্ট করছে না। এরর: {e2}")
