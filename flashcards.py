import random
import streamlit as st
from conversor import *
import static

def vocabulary_list(lang, firstlang, arraylen):
    # Initialize arrays to store words in the target language and their firstlang translations
    targetlang_words = []
    firstlang_words = []

    # Generate words and translations
    for _ in range(arraylen):
        # Generate a word in the target language
        target_word = generate_translation("", firstlang, lang)  # Translate an empty string
        
        # Generate the firstlang translation of the word
        firstlang_translation = generate_translation(target_word, lang, firstlang)
        
        # Append the words and translations to their respective arrays
        targetlang_words.append(target_word)
        firstlang_words.append(firstlang_translation)

    return targetlang_words, firstlang_words

def generate_translation(word, source_lang, targetlang ):
    #openai.api_key = os.getenv("OPENAI_API_KEY")

    # Compose the prompt for translation
    prompt = f"Translate the {source_lang} word '{word}' to {targetlang}."
    
    # Generate the translation using GPT-3.5
    response = openai.Completion.create(
        engine="gpt-4",  
        prompt=prompt,
        max_tokens=100,  # Adjust as needed for longer translations
        stop=None,
        temperature=0.7,
    )
     # Extract and return the translation from the response
    translation = response.choices[0].text.strip()
    return translation


def practice_flashcards(tglanglist, flanglist, indexnum):

    displayvalue = tglanglist[indexnum]
    st.header(displayvalue) 

    col1, col2 = st.columns(2)

    with col1:
        flip = st.button("Flip", displayvalue = flanglist[indexnum])

    with col2:
        next = st.button("Next", static.fc_index_list.remove(indexnum))


def main():
    print()

if __name__ == "__main__":
    main()
