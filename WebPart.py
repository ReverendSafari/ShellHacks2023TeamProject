import streamlit as st
import sqlite3

# Initialize SQLite DB
# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );"""
    )
    conn.commit()
    conn.close()

init_db()

# Check if we are on the registration page or login page
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["login"])[0]

# Sidebar
st.sidebar.title('LangGPT')

# Organization for the UI
col1, col2, col3 = st.columns(3)

# Getting the buttons inline for better visibility
with col1:
    ntLang = st.selectbox('Native language', ['english', 'spanish', 'french'])

with col2:
    tgLang = st.selectbox('Target Language', ['english', 'spanish', 'french'])

with col3:
    name = st.text_input('Enter a name for the bot')

user_input = st.text_input('Start your conversation here')

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "login"

# Sidebar button nav
if st.session_state.page == "login":
    st.sidebar.button("Go to Register", on_click=lambda: setattr(st.session_state, "page", "register"), key='regButton')
elif st.session_state.page == "register":
    st.sidebar.button("Go to Login", on_click=lambda: setattr(st.session_state, "page", "login"), key='logButton')

#Login State
if st.session_state.page == "login":
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Submit", key="subButton"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            st.success("Logged in successfully")
            # set other session states or perform other actions here
        else:
            st.error("Invalid credentials")
        conn.close()
    

#Registration State
elif st.session_state.page == "register":
    st.sidebar.title("Register")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Register", key='regButton'):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            st.sidebar.success("User registered successfully")
            setattr(st.session_state, "page", "login")  # Navigate back to login
        except sqlite3.IntegrityError:  # Username already exists
            st.sidebar.error("Username already exists. Please choose another.")
        conn.close()