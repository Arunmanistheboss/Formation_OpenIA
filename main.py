import streamlit as st



path = "app_pages/"
pg = st.navigation([
        st.Page(path + "Chat.py", title="1.Chat"), 
        st.Page(path + "DALL-E.py", title="2.DALL-E"),
        st.Page(path + "Article.py", title="3.Article"),


    ]) 
pg.run()