import streamlit as st
from PIL import Image
import openai
import os
from googletrans import Translator
from gtts import gTTS

# --- Configuration ---
openai.api_key = "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"  # Add your OpenAI API Key here

# --- App Setup ---
st.set_page_config(page_title="GenAI MedAssist", layout="wide")
st.title("🩺 GenAI MedAssist: Multilingual Medical Analyzer with Voice & Vision")
st.markdown("""
Analyze wounds or medications via image or text and receive human-friendly instructions in your preferred language with voice output.
""")

# --- Initialize Translator ---
translator = Translator()

# --- Helper Functions ---
def translate_text(text, target_language):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"Translation error: {e}"

def generate_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

def generate_audio(text, language_code):
    try:
        tts = gTTS(text, lang=language_code)
        audio_fp = "output.mp3"
        tts.save(audio_fp)
        return audio_fp
    except Exception as e:
        return None

# --- Input Section ---
option = st.radio("Select input type:", ["Text", "Image"])
lang_option = st.selectbox("Choose output language", [
    ("English", "en"),
    ("Kannada", "kn"),
    ("Hindi", "hi"),
    ("Telugu", "te"),
    ("Spanish", "es"),
    ("French", "fr"),
    ("German", "de")
])
selected_language, lang_code = lang_option

input_text = ""
image = None
if option == "Text":
    input_text = st.text_area("Enter symptoms or medicine description")
elif option == "Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300)
        input_text = "This is an image of a wound or medicine. Analyze the image content and provide helpful guidance."

# --- Run Analysis ---
if st.button("🧠 Analyze") and (input_text.strip() or image):
    with st.spinner("Analyzing..."):
        ai_output = generate_ai_response(f"Act like a helpful assistant. Analyze and explain:\n{input_text}")

        st.subheader("📝 AI Analysis")
        st.write(ai_output)

        st.subheader("🌐 Translation to " + selected_language)
        translated = translate_text(ai_output, lang_code)
        st.write(translated)

        st.subheader("🔊 Audio Instructions")
        audio_path = generate_audio(translated, lang_code)
        if audio_path:
            audio_file = open(audio_path, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
        else:
            st.error("⚠️ Failed to generate voice. Please try again.")
else:
    st.info("Please input text or upload an image and click 'Analyze'.")
