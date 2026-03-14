import streamlit as st
import random
from gtts import gTTS
import os

st.set_page_config(page_title="AI Pronunciation Trainer")

st.title("AI Pronunciation Trainer")

# -------- Name --------
name = st.text_input("Enter Your Name")

if name:
    st.success(f"Welcome {name}")

# -------- Class --------
student_class = st.selectbox(
    "Select Your Class",
    ["1-3","4-5","6-8","9-10"]
)

# -------- Language --------
language = st.selectbox(
    "Select Language",
    ["English","Hindi","Marathi","Sanskrit"]
)

# -------- AI Word Pools --------

AI_WORDS = {

"English":[
"cat","dog","tree","sun","book","apple","teacher","window",
"garden","banana","science","language","computer","beautiful",
"technology","environment","knowledge","education","communication"
],

"Hindi":[
"घर","पानी","सूरज","किताब","विद्यालय","शिक्षक","परिवार",
"कक्षा","विद्यार्थी","संविधान","पर्यावरण","स्वतंत्रता"
],

"Marathi":[
"घर","पाणी","आई","सूर्य","शाळा","शिक्षक",
"विद्यार्थी","अभ्यास","तंत्रज्ञान","पर्यावरण"
],

"Sanskrit":[
"गृह","जल","सूर्य","माता","विद्यालयः","विद्यार्थी",
"पर्यावरणम्","स्वतन्त्रता"
]

}

# -------- Complexity Control (AI Logic) --------

def generate_word(lang, student_class):

    words = AI_WORDS[lang]

    if student_class == "1-3":
        filtered = [w for w in words if len(w) <= 4]

    elif student_class == "4-5":
        filtered = [w for w in words if 4 < len(w) <= 6]

    elif student_class == "6-8":
        filtered = [w for w in words if 6 < len(w) <= 9]

    else:
        filtered = [w for w in words if len(w) > 8]

    return random.choice(filtered)

# -------- Generate Word --------

if st.button("Generate AI Word"):

    word = generate_word(language, student_class)

    st.session_state.word = word

# -------- Show Word --------

if "word" in st.session_state:

    word = st.session_state.word

    st.subheader("Pronounce This Word")

    st.markdown(f"## {word}")

    # correct pronunciation
    tts = gTTS(word)

    tts.save("word.mp3")

    audio_file = open("word.mp3","rb")

    st.audio(audio_file.read())

    os.remove("word.mp3")
