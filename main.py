from openai import OpenAI
import streamlit as st

client = OpenAI(api_key="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")

value = st.text_input("Prompt")
if(value):
    txt = st.header("Waiting for api...")

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content" : "value"}
    ] 
)   
    txt.text(completion.choices[0].message.content)