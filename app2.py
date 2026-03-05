import os
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

# Force load .env from same folder as app2.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

print("DEBUG API:", os.getenv("GOOGLE_API_KEY"))

# Read API Key
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API KEY NOT FOUND. Add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

# Configure Gemini
client = genai.Client(api_key=API_KEY)

# ---------------- GEMINI FUNCTION ----------------

def get_gemini_response(prompt, uploaded_file):

    image_bytes = uploaded_file.getvalue()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=uploaded_file.type
            ),
        ],
    )

    return response.candidates[0].content.parts[0].text

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Click_2_Cook", page_icon="🍳", layout="wide")

st.title("🍽 Click_2_Cook")
st.markdown("---")

col1, col2 = st.columns([1, 2])

# LEFT SIDE
with col1:
    st.subheader("📤 Upload Your Image")

    uploaded_file = st.file_uploader(
        "Upload a food image (JPG, JPEG, PNG, WEBP)",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        submit = st.button("🚀 Generate Recipe", use_container_width=True)


# PROMPT
system_prompt = """
You are a food image recognition and recipe generation assistant.

1. Identify the food item.
2. List ingredients with estimated quantities.
3. Provide full step-by-step recipe.
4. Provide nutrition: carbs, protein, vitamins percentage.
5. If image is not food, politely say no food detected.
"""


# RIGHT SIDE
with col2:
    st.subheader("🍴 Recipe Suggestions")

    if uploaded_file and submit:
        with st.spinner("Analyzing food..."):
            try:
                response = get_gemini_response(system_prompt, uploaded_file)

                st.success("Recipe Generated!")
                st.write(response)

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown(
    "<h6 style='text-align: center; color: grey;'>Built with ❤ by Rupesh Desai</h6>",
    unsafe_allow_html=True
)