import streamlit as st
import ollama

st.logo("https://upload.wikimedia.org/wikipedia/en/f/ff/Amity_University_logo.png")

st.sidebar.title("Bot Settings")

with st.sidebar:
    model = st.text_input("Model Name", value="gemma4", key="model_name")
    st.markdown("Make sure your model is running.")

st.title("Kartik's Local ChatBot")
st.caption("Hello from Gemma Chat Bot by Kartik")

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not model:
        st.info("Please add your model name to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = ollama.chat(model = model, messages = st.session_state.messages)
    answer = response['message']['content']

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
