import streamlit as st
import openai
import data
import conversor as convo
import sqlite3 as db
import static



data.init_db()

if (not data.analysis.is_null()):
    data.analysis.nullify()

    # Organization for the UI
col1, col2 = st.columns(2)

    # Getting the buttons inline for better visibility
with col1:
    tgLang = st.selectbox('Target Language', convo.system.LANGS)

with col2:
    data.current.ctype = st.selectbox('Dialog Type', ['Conversation', 'Advice and corrections'])

static.general()


    # Show the chat feature only if the user is logged in
if static.st.session_state.is_logged_in:
    if (data.current.user is not None):
        st.title("LangGPT - " + data.current.user.sysname)
        user_input = st.text_input('Enter a sentence')
    else:
        st.title("LangGPT")
        user_input = False
    
    if  data.current.user and data.current.ctype and st.button("Send") and user_input:
        # Simulate user's message
        if (data.current.ctype == 'Conversation'):
            data.current.user._converse(user_input, tgLang)
        else:
            data.current.user._feedback(user_input, tgLang)

        # Display Chat History
        st.write("Chat History")

        if (data.current.ctype == 'Conversation'):
            history = data.current.user.conversations[tgLang].dialog_list
        else:
            history = data.current.user.langchecks[tgLang].dialog_list

        for i in range (1, len(history)):
            if history[i]["role"] == "user":
                st.write(data.current.user.name + f": {history[i]['content']}")
            else:
                st.write(data.current.user.sysname + f": {history[i]['content']}")   

else:
    st.warning("Please log in to access the chat feature")
    user_input = False
