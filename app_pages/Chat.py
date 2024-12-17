from openai import OpenAI
import streamlit as st

client = OpenAI()


if "messages" not in st.session_state:
    st.session_state.messages = []

def new_message(content: str):
    with (st.chat_message("user")):
        st.session_state.messages.append({"role":"user", "content": content})
        st.write(content)

    with (st.chat_message("assistant")):
        field = st.text("waiting for an answer...")
    
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user","content": content}
        ]
        )
        
        st.session_state.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        field.text(completion.choices[0].message.content)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.text(message["content"])
value = st.chat_input("Say something")
if (value and value != ""):
    new_message(value)
    value = ""