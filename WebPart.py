import streamlit as st
import openai
import sqlite3

from Main import system


# Initialize SQLite database
def init_db():
    try:
        with sqlite3.connect("userDB.db") as conn:
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS userDB (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    ntLang TEXT,
                    tgLang TEXT
                );"""
            )

            conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"Database error: {e}")

init_db()
# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'is_logged_in' not in st.session_state:  # Initialize login state
    st.session_state.is_logged_in = False

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
        with sqlite3.connect("userDB.db") as conn:
            c = conn.cursor()
        c.execute("SELECT * FROM userDB WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            st.success("Logged in successfully")
            st.session_state.is_logged_in = True  # Update login state
        else:
            st.error("Invalid credentials")
        conn.close()

# Registration State
elif st.session_state.page == "register":
    st.sidebar.title("Register")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Register", key='regButton'):
        with sqlite3.connect("userDB.db") as conn:
            c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO userDB (username, password, ntLang, tgLang) VALUES (?, ?, ?, ?)",
                (new_username, new_password, ntLang, tgLang)
            )
            conn.commit()
            st.sidebar.success("User registered successfully")
            setattr(st.session_state, "page", "login")  # Navigate back to login
        except sqlite3.IntegrityError:  # Username already exists
            st.sidebar.error("Username already exists. Please choose another.")
        conn.close()


# Show the chat feature only if the user is logged in
if st.session_state.is_logged_in:
    st.title("Chat Feature")
    user_input = st.text_input('Start your conversation here')
else:
    st.warning("Please log in to access the chat feature")
    user_input = False
# Initialize
chat_history = []

if user_input:
    # Simulate user's message
    chat_history.append({"role": "user", "content": user_input})

    # Generate a response using your model (Here you would call the method from the system class)
    # For demonstration, I'm assuming a method called generate_response exists
    ai_response = "Print this test string"

    # Simulate AI's message
    chat_history.append({"role": "AI", "content": ai_response})

# Display Chat History
st.write("## Chat History")
for message in chat_history:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"AI: {message['content']}")


