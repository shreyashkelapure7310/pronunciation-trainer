import streamlit as st
import random
from difflib import SequenceMatcher
from gtts import gTTS
import speech_recognition as sr
import os

st.set_page_config(page_title="AI Teacher Tejal")

recognizer = sr.Recognizer()

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# ---------- WORD DATABASE ----------

WORDS = {

"English":{
"Easy":["cat","dog","sun","book"],
"Medium":["teacher","window","garden"],
"Hard":["beautiful","technology","environment"]
},

"Hindi":{
"Easy":["घर","पानी","सूरज"],
"Medium":["विद्यालय","शिक्षक"],
"Hard":["संविधान","स्वतंत्रता"]
},

"Marathi":{
"Easy":["घर","आई","पाणी"],
"Medium":["शाळा","शिक्षक"],
"Hard":["तंत्रज्ञान","पर्यावरण"]
}

}

# ---------- PAGE 1 WELCOME ----------

if st.session_state.page == "welcome":

    st.title("Hey I am Tejal 👩‍🏫 Your AI Teacher")

    st.write("You can practice pronunciation with me 24 hours.")

    name = st.text_input("Please enter your name")

    if st.button("Next"):

        st.session_state.name = name
        st.session_state.page = "age"
        st.rerun()


# ---------- PAGE 2 AGE ----------

elif st.session_state.page == "age":

    st.title(f"Hello {st.session_state.name}")

    age = st.number_input("Enter your age", 3, 20)

    if st.button("Next"):

        st.session_state.age = age
        st.session_state.page = "class"
        st.rerun()


# ---------- PAGE 3 CLASS ----------

elif st.session_state.page == "class":

    student_class = st.selectbox(
        "Select Your Class",
        ["1-3","4-5","6-8","9-10"]
    )

    if st.button("Next"):

        st.session_state.class_level = student_class
        st.session_state.page = "language"
        st.rerun()


# ---------- PAGE 4 LANGUAGE ----------

elif st.session_state.page == "language":

    language = st.selectbox(
        "Please enter your language",
        ["English","Hindi","Marathi"]
    )

    difficulty = st.radio(
        "Select Difficulty",
        ["Easy","Medium","Hard"]
    )

    if st.button("Start Practice"):

        st.session_state.language = language
        st.session_state.level = difficulty
        st.session_state.page = "practice"
        st.rerun()


# ---------- PAGE 5 PRACTICE ----------

elif st.session_state.page == "practice":

    st.title("Pronunciation Practice")

    language = st.session_state.language
    level = st.session_state.level

    word = random.choice(WORDS[language][level])

    st.subheader("Pronounce this word")

    st.markdown(f"## {word}")

    if st.button("Start Recording"):

        try:

            with sr.Microphone() as source:

                st.info("Listening...")

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

            if accuracy >= 70:

                st.success("Great job! 🎉")

            else:

                st.warning("Accuracy below 70%. Listen correct pronunciation")

                tts = gTTS(word)

                tts.save("correct.mp3")

                audio_file = open("correct.mp3","rb")

                st.audio(audio_file.read())

                os.remove("correct.mp3")

        except:

            st.error("Could not understand speech. Try again.")
