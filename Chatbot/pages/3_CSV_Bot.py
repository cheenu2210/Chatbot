import streamlit as st
import google.generativeai as genai
import pandas as pd

st.logo("https://upload.wikimedia.org/wikipedia/en/f/ff/Amity_University_logo.png")

st.sidebar.title("Bot Settings")

with st.sidebar:
    model_name = st.selectbox(
        "Select Your Model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        key="gemini_model"
    )
    
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")

st.title("📝 CSV Bot with Kartik")
st.caption("Chat with your uploaded CSV file.")

uploaded_file = st.file_uploader("Upload your CSV here.", type=["csv"])

if not gemini_api_key:
    st.info("Please add your Google API key to continue.")
    st.stop()

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name)

# Initializing the session state for chat
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.df = None

# If a new file is uploaded, read and store the CSV
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df

    if not any(msg["role"] == "assistant" for msg in st.session_state.messages):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Article Uploaded! You can now ask me questions about it."
        })

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask me something about the CSV file."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if st.session_state.df is not None:
        df_str = st.session_state.df.to_string()
        chat_prompt = f"""
        You are an AI assistant helping analyze a CSV file.
        Here is the CSV data:
        <csv_data>
        {df_str}
        </csv_data>
        Now my question is: {prompt}
        """

        chat = model.start_chat(history=[])
        response = chat.send_message(chat_prompt)

        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    else:
        st.error("Please upload a CSV file first.")
