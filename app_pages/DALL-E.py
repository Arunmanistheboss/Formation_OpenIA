from openai import OpenAI
import streamlit as st


def openai_create_image(prompt: str):
    try:

        client = OpenAI()


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


prompt = st.text_input("Entrez une description pour générer une image")

if st.button("Générer l'image"):
    if prompt:

        image_url = openai_create_image(prompt)

        if "http" in image_url:
            st.image(image_url, caption="Image générée par DALL-E", use_container_width=True)
        else:
            st.error(f"Erreur : {image_url}")
    else:
        st.warning("Veuillez entrer une description pour générer une image.")
