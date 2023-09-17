import streamlit as st
import sqlite3 as db
import data
import conversor as convo

class current:
    user = None
    

def general():
    # Sidebar
    st.sidebar.title("LangGPT")

    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'is_logged_in' not in st.session_state:  # Initialize login state
        st.session_state.is_logged_in = False


    if not st.session_state.is_logged_in:
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
                    current.user = convo.user(username, arr[2], arr[3])
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
                    c.execute("INSERT INTO userDB VALUES (?, ?, ?, ?)", (new_username, new_password, native_language, bot_name))
                    conn.commit()
                    with db.connect(new_username + ".db") as da:
                        d = da.cursor()

                    try:
                        d.execute("CREATE TABLE IF NOT EXISTS " + new_username + " ("
                                "language TEXT PRIMARY INDEX, "
                                "time DOUBLE NOT NULL, "
                                "grammar INT NOT NULL, "
                                "syntax INT NOT NULL, "
                                "vocab INT NOT NULL);")
                        da.commit()

                    except db.OperationalError as e:
                        st.sidebar.error(f"Database Error: {e}")

                    da.close()

                    st.sidebar.success("current.user registered successfully")
                    current.user = convo.user(new_username, native_language, bot_name)
                    st.session_state.is_logged_in = True
                    setattr(st.session_state, "page", "login")  # Navigate back to login
                except db.IntegrityError:  # Username already exists
                    st.sidebar.error("Username already exists. Please choose another.")
                conn.close()
