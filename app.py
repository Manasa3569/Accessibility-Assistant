import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import os

# -----------------------------
# SAFE IMPORT FOR VOICE
# -----------------------------
try:
    import speech_recognition as sr
    voice_available = True
except:
    voice_available = False

# -----------------------------
# SET TESSERACT PATH (Windows – Local only)
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(
    page_title="Accessibility Assistant",
    page_icon="♿",
    layout="wide"
)

st.title("♿ Accessibility Assistant")
st.write("This tool helps visually impaired users using Text, Voice, and Image input.")

# -----------------------------
# INPUT SELECTION
# -----------------------------
input_type = st.selectbox(
    "Select input type:",
    ["Text", "Voice", "Image"]
)

user_input = ""

# -----------------------------
# TEXT INPUT
# -----------------------------
if input_type == "Text":
    user_input = st.text_area("Enter your text:", height=120)

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
    image_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Convert to grayscale
        gray_img = img.convert("L")

        # OCR
        extracted_text = pytesseract.image_to_string(gray_img)

        st.subheader("Extracted Text:")
        if extracted_text.strip() == "":
            st.warning("No text detected. Please upload a clear image.")
        else:
            st.success(extracted_text)

        user_input = extracted_text

# -----------------------------
# OUTPUT ACTION
# -----------------------------
if user_input:
    st.markdown("---")
    st.subheader("Output")

    # TEXT → SPEECH
    if input_type == "Text":
        tts = gTTS(text=user_input, lang="en")
        audio_file = "output.mp3"
        tts.save(audio_file)
        st.audio(audio_file)
        st.info("Text converted to Speech")

    # VOICE → TEXT
    elif input_type == "Voice":
        st.info(f"Recognized Text: {user_input}")

    # IMAGE → TEXT
    elif input_type == "Image":
        st.info("Text successfully extracted from image.")
