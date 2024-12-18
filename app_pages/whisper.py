from openai import OpenAI
import streamlit as st
from pathlib import Path

client = OpenAI()

audio = st.audio_input("Dites quelque chose")

if (audio):
    file_path = Path(__file__).parent.parent / "input.mp3"

    with open(file_path, "wb") as file:
        file.write(audio.getbuffer())

    with open(file_path, "rb") as file:
        translation = client.audio.translations.create(
        model="whisper-1",
        file=file
        )
    
        st.write(translation.text)   

