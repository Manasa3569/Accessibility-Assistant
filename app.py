import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import os

# -----------------------------
# Optional: Speech Recognition
# -----------------------------
try:
    import speech_recognition as sr
    voice_available = True
except:
    voice_available = False

# -----------------------------
# SET TESSERACT PATH (Windows local only)
# -----------------------------
# Only needed if running locally on Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Accessibility Assistant", page_icon="♿", layout="wide")
st.title("♿ Accessibility Assistant")
st.write("A tool to help visually impaired users with Text, Voice, and Image input.")

# -----------------------------
# INPUT SELECTION
# -----------------------------
input_type = st.selectbox("Select input type:", ["Text", "Voice", "Image"])
user_input = ""

# -----------------------------
# TEXT INPUT
# -----------------------------
if input_type == "Text":
    user_input = st.text_area("Enter your command:", height=100)

# -----------------------------
# VOICE INPUT
# -----------------------------
elif input_type == "Voice":
    if not voice_available:
        st.error("Voice input is NOT supported on Streamlit Cloud.")
    else:
        if st.button("Start Listening"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening...")
                audio = recognizer.listen(source)
                try:
                    user_input = recognizer.recognize_google(audio)
                    st.success(f"You said: {user_input}")
                except:
                    st.error("Could not recognize audio")

# -----------------------------
# IMAGE INPUT
# -----------------------------
elif input_type == "Image":
    image_file = st.file_uploader("Upload Image", ["png", "jpg", "jpeg"])
    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Convert image to grayscale and OCR
        gray_img = img.convert("L")
        extracted_text = pytesseract.image_to_string(gray_img)

        st.subheader("Extracted Text:")
        if extracted_text.strip() == "":
            st.warning("No text detected. Please upload a clear image.")
        else:
            st.success(extracted_text)

        user_input = extracted_text

# -----------------------------
# ACTION BASED ON INPUT
# -----------------------------
if user_input:
    st.markdown("---")
    st.subheader("Output:")

    # Text input → TTS
    if input_type == "Text":
        tts = gTTS(text=user_input, lang='te')
        tts_file = "output.mp3"
        tts.save(tts_file)
        st.audio(tts_file)
        st.info("Speaking the text in Telugu...")

    # Voice input → display recognized text
    elif input_type == "Voice":
        st.info(f"Voice-to-Text result: {user_input}")

    # Image input → display extracted text
    elif input_type == "Image":
        st.info("Text extracted from image above.")
