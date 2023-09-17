import streamlit as st
import openai
import sqlite3
import conversor as convo

class current:
    lang = None
    ctype = None

class analysis:
    lang = None
    grammar_dict = {}
    syntax_dict = {}
    vocab_dict = {}

    def is_null():
        return analysis.lang is None
    
    def nullify():
        analysis.lang = None
        analysis.grammar_dict = {}
        analysis.syntax_dict = {}
        analysis.vocab_dict = {}
    
    def init(lang, name):
        analysis.lang = lang
        analysis.analyze(name)

    def analyze(name):
        with sqlite3.connect(name + ".db") as data:
            d = data.cursor()
            d.execute("SELECT * FROM " + name + " WHERE language=?", (analysis.lang,))
            arr = d.fetchall()
        data.close()
        
        for tup in arr:
            if (analysis.lang == tup[0]):
                timestamp = int((tup[1]) / 10000000)

                analysis.grammar_dict[timestamp] = tup[2]
                analysis.syntax_dict[timestamp] = tup[3]
                analysis.vocab_dict[timestamp] = tup[4]
    
                

# Initialize SQLite database
def init_db():
    try:
        with sqlite3.connect("userDB.db") as conn:
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS userDB (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    nativlang TEXT NOT NULL,
                    sysname TEXT NOT NULL
                );"""
            )
            conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"Database error: {e}")


