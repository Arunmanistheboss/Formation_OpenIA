from openai import OpenAI
import streamlit as st
from pathlib import Path

client = OpenAI()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_story" not in st.session_state:
    st.session_state.current_story = ""  
if "choices" not in st.session_state:
    st.session_state.choices = []  

def generate_story(content: str):
    with st.spinner("Waiting for API "):
        prompt_story = f"Raconte une histoire intéressante basée sur le sujet suivant en 5 lignes : {content}"
        completion_story = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_story}],
        )
    story = completion_story.choices[0].message.content
    st.session_state.current_story = story
    st.session_state.messages = [{"role": "assistant", "content": story}] 
    
    # generatoin l'image
    image_url = openai_create_image(st.session_state.current_story)

    # afficher l'histoire et l'image 
    col1, col2 = st.columns([2, 1])  
    with col1:
        st.write(st.session_state.current_story)  
    with col2:
        if "http" in image_url:
            st.image(image_url, caption="Image générée par DALL-E", use_container_width=True)  # Affiche l'image
        else:
            st.error(f"Erreur lors de la génération de l'image : {image_url}")

    # generation audio de l'histoire
    generate_audio(st.session_state.current_story)

    generate_choices()

def generate_choices():
    with st.spinner("Waiting for API "):
        prompt_choices = (
            f"Propose deux choix clairs pour continuer l'histoire (pas de résumé, uniquement les choix)."
        )
        completion_choices = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_choices}],
        )
    choices_text = completion_choices.choices[0].message.content
    st.session_state.choices = parse_choices(choices_text)

def parse_choices(choices_text):
    choices = []
    for i, line in enumerate(choices_text.split("\n")):
        if line.strip():
            choices.append({"text": line.strip(), "key": f"choice_{len(st.session_state.choices) + i}"} )
    return choices

def continue_story(choice_text):
    """Poursuivre l'histoire en fonction du choix sélectionné et générer l'image et l'audio."""
    with st.spinner("Waiting for API to continue the story..."):
        prompt_continue = (
            f"Voici le choix sélectionné : {choice_text}\n"
            f"Continue l'histoire en développant ce choix en 5 lignes."
        )
        completion_continue = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_continue}],
        )
    new_story = completion_continue.choices[0].message.content
    st.session_state.current_story += f"\n\n{new_story}"
    st.session_state.messages.append({"role": "assistant", "content": new_story})  

    image_url = openai_create_image(st.session_state.current_story)

    col1, col2 = st.columns([2, 1])  
    with col1:
        st.write(new_story)  
    with col2:
        if "http" in image_url:
            st.image(image_url, caption="Image générée par DALL-E", use_container_width=True) 
        else:
            st.error(f"Erreur lors de la génération de l'image : {image_url}")

    generate_audio(st.session_state.current_story)

    generate_choices()

def openai_create_image(prompt: str):
    """Fonction pour générer l'image à partir du texte de l'histoire."""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return str(e)

def generate_audio(text: str):
    """Génère un fichier audio à partir du texte donné."""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  
            input=text
        )

        file_path = Path(__file__).parent / "output.mp3"
        response.stream_to_file(file_path)

        st.audio(file_path, autoplay=True)

    except Exception as e:
        st.error(f"Erreur lors de la génération de l'audio : {str(e)}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.text(message["content"])

if st.session_state.current_story == "":
    value = st.chat_input("Propose un sujet pour commencer une histoire")
    if value and value.strip():
        generate_story(value.strip())
else:
    st.write("Choisissez une suite pour continuer l'histoire :")
    for choice in st.session_state.choices:
        if st.button(choice["text"], key=choice["key"]):
            continue_story(choice["text"])
            break
