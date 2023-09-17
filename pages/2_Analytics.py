import data
import static
import streamlit as st
import sqlite3 as db
import openai
import conversor as convo
import static
import pandas as pd


col1, col2 = st.columns(2)

with col1:
    tgLang = st.selectbox('Target Language', convo.system.LANGS)


static.general()

if static.st.session_state.is_logged_in and st.button("View Data"):
    data.analysis.init(tgLang, static.current.user.name)
    st.line_chart(pd.DataFrame({"grammar" : list(data.analysis.grammar_dict.values()),
                               "syntax" : list(data.analysis.syntax_dict.values()),
                               "vocabulary" : list(data.analysis.vocab_dict.values())}))

        

        