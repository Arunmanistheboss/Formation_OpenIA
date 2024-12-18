from openai import OpenAI  
import streamlit as st  
from pathlib import Path  


client = OpenAI()


audio = st.audio_input("Dites quelque chose")

if (audio):
    file_path = Path(__file__).parent / "input.mp3"

    with open(file_path, "wb") as file:
        file.write(audio.getbuffer())  

    txt = st.text("Waiting for API")

    with open(file_path, "rb") as file:
        audiotranscript = client.audio.transcriptions.create(
            model="whisper-1",  
            file=file
        )

    st.subheader("Texte transcrit :")
    st.write(audiotranscript.text)  

    completion = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[{"role": "user", "content": audiotranscript.text}]  
    )

    output = completion.choices[0].message.content

    st.subheader("Réponse générée par GPT :")
    st.write(output)  

    response = client.audio.speech.create(
        model="tts-1",  
        voice="alloy",  
        input=output  
    )

    file_path = Path(__file__).parent / "output.mp3"

    response.stream_to_file(file_path)

    st.audio(file_path, autoplay=True)  
