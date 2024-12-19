import streamlit as st



path = "app_pages/"
pg = st.navigation([
        st.Page(path + "Chat.py", title="1.Chat"), 
        st.Page(path + "DALL-E.py", title="2.DALL-E"),
        st.Page(path + "Article.py", title="3.Article"),
        st.Page(path + "whisper.py", title="4.Whisper"),
        st.Page(path + "tts.py", title="5.TTS"),
        st.Page(path + "Assistant.py", title="6.Assistant Vocal"),
        st.Page(path + "App_histoire.py", title="7.Application de l'histoire"),



    ]) 
pg.run()