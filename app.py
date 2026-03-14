import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from difflib import SequenceMatcher
from gtts import gTTS
import random

st.set_page_config(page_title="AI Pronunciation Trainer", layout="centered")

recognizer = sr.Recognizer()

# ---------------- UI STYLE ----------------

st.markdown("""
<style>

.hero{
padding:40px;
border-radius:20px;
background: linear-gradient(135deg,#667eea,#764ba2);
color:white;
text-align:center;
margin-bottom:30px;
}

.card{
background:white;
padding:25px;
border-radius:15px;
margin-top:20px;
}

.wordbox{
font-size:36px;
font-weight:bold;
text-align:center;
padding:15px;
background:#eef2ff;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- WORD DATABASE ----------------

LANGUAGE_WORDS = {

"English":{
"Easy":["cat","dog","sun","tree","book"],
"Medium":["teacher","window","garden","doctor"],
"Hard":["technology","environment","knowledge"]
},

"Hindi":{
"Easy":["घर","सूरज","पानी"],
"Medium":["विद्यालय","परिवार"],
"Hard":["संविधान","स्वतंत्रता"]
},

"Marathi":{
"Easy":["घर","पाणी","आई"],
"Medium":["शाळा","विद्यार्थी"],
"Hard":["संविधान","पर्यावरण"]
},

"Sanskrit":{
"Easy":["गृह","जल"],
"Medium":["विद्यालयः"],
"Hard":["पर्यावरणम्"]
}

}

# ---------------- SESSION ----------------

if "page" not in st.session_state:
    st.session_state.page="login"

# ---------------- LOGIN PAGE ----------------

if st.session_state.page=="login":

    st.markdown("""
    <div class='hero'>
    <h1>AI Pronunciation Trainer</h1>
    <p>Improve your communication skills</p>
    </div>
    """,unsafe_allow_html=True)

    name=st.text_input("Enter Your Name")

    if st.button("Start Learning"):

        if name!="":
            st.session_state.name=name
            st.session_state.page="main"
            st.rerun()

# ---------------- MAIN PAGE ----------------

elif st.session_state.page=="main":

    st.markdown(f"### Welcome {st.session_state.name}")

    st.markdown("<div class='card'>",unsafe_allow_html=True)

    student_class=st.selectbox(
        "Select Class",
        ["1-3","4-5","6-8","9-10"]
    )

    language=st.text_input(
        "Tell Your Language (English / Hindi / Marathi / Sanskrit)"
    ).strip().title()

    level=st.radio(
        "Difficulty Level",
        ["Easy","Medium","Hard"],
        horizontal=True
    )

    st.markdown("</div>",unsafe_allow_html=True)

    if language in LANGUAGE_WORDS:

        words=LANGUAGE_WORDS[language][level]

        word=random.choice(words)

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        st.write("### Pronounce This Word")

        st.markdown(f"<div class='wordbox'>{word}</div>",unsafe_allow_html=True)

        audio=mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="Stop Recording",
            just_once=True
        )

        if audio:

            st.audio(audio["bytes"])

            try:

                with open("temp.webm","wb") as f:
                    f.write(audio["bytes"])

                with sr.AudioFile("temp.webm") as source:

                    audio_data=recognizer.record(source)

                    spoken=recognizer.recognize_google(audio_data)

                st.write("You said:",spoken)

                accuracy=SequenceMatcher(
                    None,
                    word.lower(),
                    spoken.lower()
                ).ratio()*100

                st.progress(int(accuracy))

                st.write(f"Accuracy: {accuracy:.2f}%")

                if accuracy>=70:

                    st.success("Good pronunciation!")

                else:

                    st.warning("Accuracy below 70%. Listen correct pronunciation")

                    tts=gTTS(word)

                    tts.save("correct.mp3")

                    audio_file=open("correct.mp3","rb")

                    st.audio(audio_file.read())

            except:

                st.error("Speech not recognized")

        st.markdown("</div>",unsafe_allow_html=True)

    elif language!="":

        st.warning("Type valid language: English, Hindi, Marathi, Sanskrit")
