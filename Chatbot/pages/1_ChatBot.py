import streamlit as st
import google.generativeai as genai 

st.logo("https://upload.wikimedia.org/wikipedia/en/f/ff/Amity_University_logo.png")

st.sidebar.title("Bot Settings")

with st.sidebar:
    model = st.selectbox(
        "Select Your Model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        key="gemini_model"
    )
    
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")

st.title("Kartik's Gemini Bot")
st.caption("Hello from Gemini Bot by Kartik.")

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not gemini_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model)


    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
