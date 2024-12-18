from openai import OpenAI
import streamlit as st
from pathlib import Path

client = OpenAI()

value = st.text_input("Votre prompt")

if (value):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=value
    )

    file_path = Path(__file__).parent / "output.mp3"

    response.stream_to_file(file_path)

    st.audio("output.mp3", autoplay=True)