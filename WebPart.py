import streamlit as st
import openai
import sqlite3

import conversor as convo

class current:
    user = None
    ctype = None


# Initialize SQLite database
def init_db():
    try:
        with sqlite3.connect("uDB.db") as conn:
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS uDB (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    nativlang TEXT NOT NULL,
                    sysname TEXT NOT NULL
                );"""
            )
            conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"Database error: {e}")


def frame():
    init_db()
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'is_logged_in' not in st.session_state:  # Initialize login state
        st.session_state.is_logged_in = False

    # Sidebar
    st.sidebar.title('LangGPT')

    # Sidebar button nav
    if st.session_state.page == "login":
        st.sidebar.button("Go to Register", on_click=lambda: setattr(st.session_state, "page", "register"), key='regButton')
    elif st.session_state.page == "register":
        st.sidebar.button("Go to Login", on_click=lambda: setattr(st.session_state, "page", "login"), key='logButton')

    # Login State
    if st.session_state.page == "login":
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Submit", key="subButton"):
            with sqlite3.connect("uDB.db") as conn:
                c = conn.cursor()
            c.execute("SELECT * FROM uDB WHERE username=? AND password=?", (username, password))
            if c.fetchone():
                st.success("Logged in successfully")
                st.session_state.is_logged_in = True  # Update login state
                current.user = convo.user(username, c[2], c[3])
            else:
                st.error("Invalid credentials")
            conn.close()

    # Registration State
    elif st.session_state.page == "register":
        st.sidebar.title("Register")
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        native_language = st.sidebar.text_input("Native Language")
        bot_name = st.sidebar.text_input("Bot Name")

        if st.sidebar.button("Register", key='regButton'):
            with sqlite3.connect("uDB.db") as conn:
                c = conn.cursor()
            try:
                c.execute("INSERT INTO uDB (username, password, nativlang, sysname) VALUES (?, ?, ?, ?)", (new_username, new_password, native_language, bot_name))
                conn.commit()
                with sqlite3.connect(new_username + ".db") as data:
                    d = data.cursor()

                try:
                    d.execute("CREATE IF NOT EXISTS " + new_username + " ("
                            "language TEXT PRIMARY KEY,"
                            "time DOUBLE NOT NULL"
                            "grammar INT NOT NULL"
                            "syntax INT NOT NULL"
                            "vocab INT NOT NULL);")
                    data.commit()

                except sqlite3.OperationalError as e:
                    st.sidebar.error(f"Database Error: {e}")

                data.close()

                st.sidebar.success("User registered successfully")
                current.user = convo.user(new_username, native_language, bot_name)
                setattr(st.session_state, "page", "login")  # Navigate back to login
            except sqlite3.IntegrityError:  # Username already exists
                st.sidebar.error("Username already exists. Please choose another.")
            conn.close()

    # Organization for the UI
    col1, col2 = st.columns(2)

    # Getting the buttons inline for better visibility
    with col1:
        tgLang = st.selectbox('Target Language', convo.system.LANGS)

    with col2:
        current.ctype = st.selectbox('Dialog Type', ['Conversation', 'Advice and corrections'])



    # Show the chat feature only if the user is logged in
    if st.session_state.is_logged_in:
        if (current.user is not None):
            st.title("LangGPT - " + current.user.sysname)
            user_input = st.text_input('Enter a sentence')
        else:
            st.title("LangGPT")
            user_input = False
    else:
        st.warning("Please log in to access the chat feature")
        user_input = False


    if current.user and current.ctype and user_input and st.button("Send"):
        # Simulate user's message
        if (current.ctype == 'Conversation'):
            current.user._converse(user_input, tgLang)
        else:
            current.user._feedback(user_input, tgLang)

        # Display Chat History
        st.write("Chat History")

        if (current.ctype == 'Conversation'):
            history = current.user.conversations[tgLang].dialog_list
        else:
            history = current.user.langchecks[tgLang].dialog_list

        for i in range (1, len(history)):
            if history[i]["role"] == "user":
                st.write(current.user.name + f": {history[i]['content']}")
            else:
                st.write(current.user.sysname + f": {history[i]['content']}")


