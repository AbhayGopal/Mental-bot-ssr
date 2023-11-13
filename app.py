import time
import random
import streamlit as st
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Started")


st.title("Your AI Counselor")

openai.api_base = "http://localhost:1234/v1"  # point to the local server
openai.api_key = ""  # no need for an API key
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "TheBloke/codellama-13b-instruct.Q5_K_M.gguf"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How are you feeling?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
