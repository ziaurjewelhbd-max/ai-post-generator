import streamlit as st
import requests
import base64
from PIL import Image
import io

# ১. পেজ সেটআপ
st.set_page_config(page_title="AI Product Post Generator", layout="centered")

# ২. এপিআই কি (Secrets থেকে নেবে, না থাকলে সরাসরি কি ব্যবহার করবে)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # এখানে আপনার এপিআই কি-টি দিয়ে রাখুন যদি সিক্রেটস কাজ না করে
    api_key = "AIzaSyDpkDgZ92pdCNcaVOkEAqKVkJwUUyy9oaI"

st.title("📸 AI Social Media Post Generator")
st.markdown("আপনার হাতের কাজের বা প্রোডাক্টের ছবি দিন, এআই পোস্ট লিখে দেবে।")

# ৩. ইমেজ আপলোডার
uploaded_file = st.file_uploader("একটি ছবি আপলোড করুন", type=["jpg", "jpeg", "png"])

def generate_post_via_api(api_key, image_bytes):
    # সরাসরি Google API URL (v1 ভার্সন ব্যবহার করা হচ্ছে যাতে 404 এরর না আসে)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # ছবিকে বেস-৬৪ ফরম্যাটে রূপান্তর
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": "আপনি একজন প্রফেশনাল সোশ্যাল মিডিয়া ম্যানেজার। এই ছবিটির প্রোডাক্ট অনুযায়ী একটি সুন্দর ফেসবুক ও ইন্সটাগ্রাম পোস্ট বাংলায় লিখুন। সাথে ইমোজি এবং ১০টি ট্রেন্ডিং হ্যাশট্যাগ দিন।"},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": encoded_image
                    }
                }
            ]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if uploaded_file:
    # প্রিভিউ দেখানো
    image = Image.open(uploaded_file)
    st.image(image, caption='প্রিভিউ', use_container_width=True)
    
    if st.button("পোস্ট তৈরি করো ✨"):
        with st.spinner('এআই আপনার ছবিটি এনালাইসিস করছে...'):
            try:
                # ছবিকে প্রসেস করা
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_bytes = img_byte_arr.getvalue()
                
                # এপিআই কল করা
                result = generate_post_via_api(api_key, img_bytes)
                
                # রেজাল্ট দেখানো
                if 'candidates' in result:
                    output_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("হয়ে গেছে!")
                    st.markdown("---")
                    st.write(output_text)
                else:
                    st.error("এপিআই থেকে কোনো উত্তর পাওয়া যায়নি। আপনার এপিআই কি চেক করুন।")
                    # কারিগরি সমস্যার বিস্তারিত দেখতে চাইলে নিচের লাইনটি আনকমেন্ট করতে পারেন
                    # st.write(result) 
                    
            except Exception as e:
                st.error(f"দুঃখিত, কারিগরি সমস্যা হয়েছে: {e}")

st.markdown("---")
st.caption("Developed for Local Businesses & Creators")
