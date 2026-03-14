import streamlit as st
import speech_recognition as sr
from difflib import SequenceMatcher
from gtts import gTTS
import random
import os

st.set_page_config(page_title="AI Pronunciation Trainer", layout="centered")

recognizer = sr.Recognizer()

# ---------- MODERN UI ----------
st.markdown("""
<style>

body{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

.hero{
padding:40px;
border-radius:20px;
background: linear-gradient(135deg,#667eea,#764ba2);
color:white;
text-align:center;
margin-bottom:30px;
box-shadow:0px 10px 40px rgba(0,0,0,0.3);
}

.hero h1{
font-size:40px;
font-weight:700;
}

.card{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0px 10px 25px rgba(0,0,0,0.1);
margin-top:20px;
}

.wordbox{
font-size:38px;
font-weight:bold;
text-align:center;
padding:15px;
border-radius:12px;
background:#eef2ff;
margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- WORD DATABASE ----------

LANGUAGE_WORDS = {

"English":{
"Easy":["cat","dog","tree","sun","book"],
"Medium":["teacher","window","garden","doctor","banana"],
"Hard":["beautiful","technology","environment","knowledge"]
},

"Hindi":{
"Easy":["घर","सूरज","पानी","माता","किताब"],
"Medium":["विद्यालय","शिक्षक","परिवार","कक्षा"],
"Hard":["संविधान","पर्यावरण","स्वतंत्रता"]
},

"Marathi":{
"Easy":["घर","पाणी","आई","सूर्य"],
"Medium":["शाळा","विद्यार्थी","शिक्षक"],
"Hard":["संविधान","पर्यावरण","तंत्रज्ञान"]
},

"Sanskrit":{
"Easy":["गृह","जल","सूर्य","माता"],
"Medium":["विद्यालयः","विद्यार्थी"],
"Hard":["पर्यावरणम्","स्वतन्त्रता"]
}

}

# ---------- SESSION STATE ----------

if "page" not in st.session_state:
    st.session_state.page = "login"

if "current_word" not in st.session_state:
    st.session_state.current_word = ""

# ---------- LOGIN PAGE ----------

if st.session_state.page == "login":

    st.markdown("""
    <div class='hero'>
    <h1>AI Pronunciation Trainer</h1>
    <p>Improve Your Speaking Skills</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Enter Your Name")

    if st.button("Start Learning 🚀"):

        if name != "":
            st.session_state.name = name
            st.session_state.page = "main"
            st.rerun()

# ---------- MAIN PAGE ----------

elif st.session_state.page == "main":

    st.markdown(f"### Welcome {st.session_state.name} 👋")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    language = st.selectbox(
        "Select Language",
        ["English","Hindi","Marathi","Sanskrit"]
    )

    level = st.radio(
        "Difficulty Level",
        ["Easy","Medium","Hard"],
        horizontal=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    words = LANGUAGE_WORDS[language][level]

    if st.button("Generate Word 🎯"):
        st.session_state.current_word = random.choice(words)

    if st.session_state.current_word != "":

        word = st.session_state.current_word

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.write("### Pronounce This Word")

        st.markdown(f"<div class='wordbox'>{word}</div>", unsafe_allow_html=True)

        if st.button("🎤 Start Recording"):

            try:

                with sr.Microphone() as source:

                    st.info("Listening... Speak now")

                    recognizer.adjust_for_ambient_noise(source)

                    audio = recognizer.listen(source)

                spoken = recognizer.recognize_google(audio)

                st.write("You said:", spoken)

                accuracy = SequenceMatcher(
                    None,
                    word.lower(),
                    spoken.lower()
                ).ratio() * 100

                st.progress(int(accuracy))

                st.write(f"Accuracy: {accuracy:.2f}%")

                if accuracy >= 80:

                    st.success("Excellent Pronunciation 🎉")

                else:

                    st.warning("Try Again! Listen to correct pronunciation.")

                    tts = gTTS(word)

                    tts.save("correct.mp3")

                    audio_file = open("correct.mp3", "rb")

                    st.audio(audio_file.read())

                    os.remove("correct.mp3")

            except:
                st.error("Speech not understood. Please try again.")

        st.markdown("</div>", unsafe_allow_html=True)