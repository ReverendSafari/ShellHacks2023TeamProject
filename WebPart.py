import streamlit as st

ntLang = st.selectbox('Native language', ['english', 'spanish', 'french'])
tgLang = st.selectbox('Target Language', ['english', 'spanish', 'french'])
name = st.text_input('Enter a name for the bot')
st.title('LangGPT')
user_input = st.text_input('Enter you prompt here')

