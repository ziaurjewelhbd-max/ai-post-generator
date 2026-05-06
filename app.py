import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Post Generator", page_icon="🛍️")

# এপিআই কি সেটআপ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "আপনার_কি_এখানে"

# সরাসরি কনফিগার করা
genai.configure(api_key=api_key)

st.title("📸 AI Product Post Generator")

uploaded_file = st.file_uploader("আপনার প্রোডাক্টের ছবি আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='প্রিভিউ', use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই কাজ করছে...'):
            try:
                # মডেল কল করার সময় সরাসরি জেনারেটিভ মডেল অবজেক্ট ব্যবহার
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    generation_config={"temperature": 0.7}
                )
                
                # প্রম্পট
                prompt = "Identify this product from the image and write a social media post in Bengali."
                
                # কন্টেন্ট জেনারেশন
                response = model.generate_content([prompt, image])
                
                st.success("তৈরি হয়ে গেছে!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"এরর ডিটেইলস: {e}")
                st.info("যদি এই এরর আসে, তবে বুঝতে হবে আপনার জিমেইল অ্যাকাউন্টটি গুগলের এই সার্ভিসটি ব্যবহারের জন্য এখনো পুরোপুরি প্রস্তুত নয়।")
