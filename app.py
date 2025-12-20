import streamlit as st
from PIL import Image
import pytesseract
import speech_recognition as sr
from gtts import gTTS
import os

# -----------------------------
# SET TESSERACT PATH (Windows)
# -----------------------------
pytesseract.pytesseract.tesseract_cmd  = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("Accessibility Assistant")

input_type = st.selectbox("Select input type:", ["Text", "Voice", "Image"])

user_input = ""

# -----------------------------
# TEXT INPUT
# -----------------------------
if input_type == "Text":
    user_input = st.text_input("Enter your command:")

# -----------------------------
# VOICE INPUT
# -----------------------------
elif input_type == "Voice":
    if st.button("Start Listening"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio)
                st.success(f"You said: {user_input}")
            except:
                st.error("Could not recognize audio. Try again.")

# -----------------------------
# IMAGE INPUT
# -----------------------------
elif input_type == "Image":
    image_file = st.file_uploader("Upload Image", ["png", "jpg", "jpeg"])
    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Uploaded Image")

        # Convert image to grayscale
        gray_img = img.convert("L")
        extracted_text = pytesseract.image_to_string(gray_img)

        st.subheader("Extracted Text:")
        if extracted_text.strip() == "":
            st.warning("No text detected. Please upload a clear image.")
        else:
            st.write(extracted_text)

        user_input = extracted_text

# -----------------------------
# ACTION BASED ON INPUT
# -----------------------------
if user_input:
    # For simplicity, Text input → TTS
    if input_type == "Text":
        # -----------------------------
        # TEXT TO SPEECH (Telugu)
        # -----------------------------
        tts = gTTS(text=user_input, lang='te')
        tts.save("output.mp3")
        st.audio("output.mp3")  # Streamlit audio player
        st.info("Speaking the text in Telugu...")

    # Voice input → display recognized text
    elif input_type == "Voice":
        st.info(f"Voice-to-Text result: {user_input}")

    # Image input → display extracted text
    elif input_type == "Image":
        st.info("Text extracted from image (see above).")
