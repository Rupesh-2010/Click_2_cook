from dotenv import load_dotenv
import os
from PIL import Image
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get Gemini API response
def get_gemini_response(prompt, image_bytes):
    try:
        response = model.generate_content([prompt, image_bytes])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to process uploaded image into bytes
def input_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded.")

# Streamlit UI Setup
st.set_page_config(page_title="Recipe Generator", page_icon="🍳", layout="wide")
st.title("🍽 Click_2_Cook")
st.markdown("---")

# Layout Design with Columns
col1, col2 = st.columns([1, 2])

# Left Section - Image Upload and Submission
with col1:
    st.subheader("📤 Upload Your Image")
    uploaded_file = st.file_uploader(
        "Upload an image of a dish or invoice (JPG, JPEG, PNG, WEBP):", 
        type=['jpg', 'jpeg', 'png', 'webp']
    )

    # Display "Generate Recipe Above" button only after image is uploaded
    if uploaded_file:
        generate_button = st.button("🚀 Generate Recipe", key="generate_btn_top", use_container_width=True)

    # Display uploaded image
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="✅ Uploaded Image", use_column_width=True)

    # Submit Button with styling below the image
    submit = st.button("🚀 Generate Recipe", key="submit_btn", use_container_width=True)

# System Prompt
system_prompt = """
You are a food image recognition and recipe generation assistant. Your goal is to analyze an image of a prepared dish and:

1. *Identify the main ingredients and their quantities.*
2. *Suggest a recipe for the dish based on the identified ingredients.*
3. *Consider the user's dietary preferences, allergies, or any additional information provided.*
4. *Also tell the amount of carbohydrate, protein as well as vitamins present in percentage.*

Use your knowledge of food identification, recipe databases, and dietary restrictions to provide accurate and helpful suggestions. Be informative, engaging, and offer variations or substitutions when possible.
"""

# Right Section - Output or Response
with col2:
    st.subheader("🍴 Recipe Suggestions:")

    # Handle both Generate Recipe buttons
    if uploaded_file:
        if generate_button or submit:
            with st.spinner("⏳ Analyzing the image and generating your recipe..."):
                image_data = input_image(uploaded_file)  # Convert to bytes
                response = get_gemini_response(system_prompt, image_data)

            # Check if response contains food-related information or an apology
            if response and "Error" not in response:
                if "ingredient" in response.lower() or "recipe" in response.lower():
                    st.success("🎉 Here's the result!")
                    st.write(response)
                else:
                    st.error("❌ Apologize, no food item present in the image.")
            else:
                st.error(f"❌ Failed to generate a response. Error: {response}")
    else:
        # Show warning only if the "Generate Recipe Below" button was clicked but no image was uploaded
        if submit:
            st.warning("⚠ Please upload an image first to generate a recipe.")

# Footer Section
st.markdown("---")
st.markdown(
    "<h6 style='text-align: center; color: grey;'>Built with ❤ by Click_2_Cook team | 2024</h6>", 
    unsafe_allow_html=True
)
