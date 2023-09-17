import random
import streamlit as st
from conversor import *
import static

class flash_set:
    translator = None
    generator = None

    question_side = []
    answer_side = []
    index = 0
    length = 20

    def __init__(self, inlang, outlang):
        self.translator = dialog.translator(inlang, outlang)
        self.generator = dialog(inlang)
        self.generator.dialog_list = system.syscommand("GEN", "Every time that you are activated, your job is to come up with any one word or short phrase in " + inlang + " which would be useful to put on a flashcard. Be sure to strictly return the generated word or phrase without any excess.")
        
        for i in range(20):
            self.answer_side.append(self.generator.respond_to_prompt("Generate a word or short phrase in " + inlang))
            self.question_side.append(self.translator.respond_to_prompt(self.answer_side[i]))
        
        static.current.flashcards = self
    
    def done(self):
        return self.index >= self.length
    



col1, col2 = st.columns(2)

with col1:
    tgLang = st.selectbox('Target Language', system.LANGS)


static.general()


if static.st.session_state.is_logged_in:
    if static.current.flashcards is None:
        flash_set(static.current.user.first_language, tgLang)
    elif static.current.flashcards.done():
        st.title("All done! Would you like to load some more?")
        if (st.button("Yes!")):
            flash_set(static.current.user.first_language, tgLang) 
    else:
        static.current.flashcards.practice()

        displayvalue = static.current.flaschards.question_side[static.current.flashcards.index]
        st.header(displayvalue) 

        col1, col2 = st.columns(2)

        with col1:
            flip = st.button("Flip", displayvalue = static.current.flashcards.answer_side[static.current.flashcards.index])

        with col2:
            if st.button("Next"):
                static.current.flashcards.index += 1
                displayvalue = static.current.flashcards.question_side[static.current.flashcards.index]

        