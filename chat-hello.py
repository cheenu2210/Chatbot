import streamlit as st

st.title("hello chatbot :)")
st.caption("welcome to your first chatbot app!!!")

user_input = st.text_input("say something to your chatbot")

if user_input:
    st.write("you said:",user_input)
    st.write("Chatbot says, Hello There!!")
    