import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

st.logo("https://upload.wikimedia.org/wikipedia/en/f/ff/Amity_University_logo.png")

st.sidebar.title("Bot Settings")

with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")


st.title("Create with Kartik")
st.caption("Create attractive images with Gemini on Kartik ImagenBot.")

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

for msg in st.session_state.messages:
    if "image_b64" in msg:
        with st.chat_message(msg["role"]):
            if msg["content"]:
                st.write(msg["content"])
            img_bytes = base64.b64decode(msg["image_b64"])
            st.image(Image.open(BytesIO(img_bytes)))
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not gemini_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()

    client = genai.Client(api_key=gemini_api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1
            )
        )

        generated_text = "Here is your generated image:"
        image_b64 = None

        if response.generated_images:
            generated_image = response.generated_images[0]
            image_b64 = base64.b64encode(generated_image.image.image_bytes).decode('utf-8')

        with st.chat_message("assistant"):
            if generated_text:
                st.write(generated_text)
            if image_b64:
                st.image(Image.open(BytesIO(base64.b64decode(image_b64))))

        message_dict = {"role": "assistant", "content": generated_text}
        if image_b64:
            message_dict["image_b64"] = image_b64
        st.session_state.messages.append(message_dict)

    except Exception as e:
        st.error(f"Error generating image: {e}")
