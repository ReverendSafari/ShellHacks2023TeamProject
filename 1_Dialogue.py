import data
import streamlit as st
import openai
import conversor as convo
import sqlite3 as db

if __name__ == "__main__":
    data.init_db()

    if (not data.analysis.is_null()):
        data.analysis.nullify()
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'is_logged_in' not in st.session_state:  # Initialize login state
        st.session_state.is_logged_in = False

        # Organization for the UI
    col1, col2 = st.columns(2)

        # Getting the buttons inline for better visibility
    with col1:
        tgLang = st.selectbox('Target Language', convo.system.LANGS)

    with col2:
        data.current.ctype = st.selectbox('Dialog Type', ['Conversation', 'Advice and corrections'])


    st.sidebar.title('LangGPT')

    if not st.session_state.is_logged_in:
        # Sidebar

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
                with db.connect("userDB.db") as conn:
                    c = conn.cursor()
                c.execute("SELECT * FROM userDB WHERE username=? AND password=?", (username, password))
                arr = c.fetchone()

                if arr:
                    st.success("Logged in successfully")
                    st.session_state.is_logged_in = True  # Update login state
                    data.current.user = convo.user(username, arr[2], arr[3])
                else:
                    st.error("Invalid credentials")
                conn.close()

        # Registration State
        elif st.session_state.page == "register":
            st.sidebar.title("Register")
            new_username = st.sidebar.text_input("New Username")
            new_password = st.sidebar.text_input("New Password", type="password")
            native_language = st.sidebar.selectbox('Native Language', convo.system.LANGS)
            bot_name = st.sidebar.text_input("Bot Name")

            if st.sidebar.button("Register"):
                with db.connect("userDB.db") as conn:
                    c = conn.cursor()
                try:
                    c.execute("INSERT INTO userDB (username, password, nativlang, sysname) VALUES (?, ?, ?, ?)", (new_username, new_password, native_language, bot_name))
                    conn.commit()
                    with db.connect(new_username + ".db") as data:
                        d = data.cursor()

                    try:
                        d.execute("CREATE TABLE IF NOT EXISTS " + new_username + " ("
                                "language TEXT PRIMARY KEY, "
                                "time DOUBLE NOT NULL, "
                                "grammar INT NOT NULL, "
                                "syntax INT NOT NULL, "
                                "vocab INT NOT NULL);")
                        data.commit()

                    except db.OperationalError as e:
                        st.sidebar.error(f"Database Error: {e}")

                    data.close()

                    st.sidebar.success("User registered successfully")
                    data.current.user = convo.user(new_username, native_language, bot_name)
                    st.session_state.is_logged_in = True
                    setattr(st.session_state, "page", "login")  # Navigate back to login
                except db.IntegrityError:  # Username already exists
                    st.sidebar.error("Username already exists. Please choose another.")
                conn.close()


        # Show the chat feature only if the user is logged in
    if st.session_state.is_logged_in:
        if (data.current.user is not None):
            st.title("LangGPT - " + data.current.user.sysname)
            user_input = st.text_input('Enter a sentence')
        else:
            st.title("LangGPT")
            user_input = False

    else:
        st.warning("Please log in to access the chat feature")
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
