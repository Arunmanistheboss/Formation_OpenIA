from openai import OpenAI
import streamlit as st

client = OpenAI()

value = st.chat_input("Thème de l'article")

with st.chat_message("user"):
    if (value):
        txt = st.text("Waiting for API")

        prompt = "Écris un article sur le sujet suivant : '"+value+"'. L'article doit comporter au 2 paragraphe."

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        txt.text(completion.choices[0].message.content)

        article_image = "illustrate this article:"+completion.choices[0].message.content

        image = client.images.generate(
                prompt=value,
                model="dall-e-2",
                n=2,
                size="512x512")

        st.image(image.data[0].url)
        st.image(image.data[1].url)