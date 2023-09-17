import data
import static
import streamlit as st
import sqlite3 as db
import openai
import conversor as convo
import static


col1, col2 = st.columns(2)

# Getting the buttons inline for better visibility
with col1:
    tgLang = st.selectbox('Target Language', convo.system.LANGS)


static.general()

if static.st.session_state.is_logged_in:
    if data.analysis.is_null() or data.analysis.lang != tgLang:
        data.analysis.init(tgLang, data.current.user.name)

    with col2:
        st.line_chart(data.analysis.grammar_dict)
        st.line_chart(data.analysis.syntax_dict)
        st.line_chart(data.analysis.vocab_dict)
        

        