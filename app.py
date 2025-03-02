import streamlit as st
import pandas as pd
import random

QUESTIONS_FILE = 'questions.csv'

# Load questions from CSV
def load_questions(num_questions):
    try:
        df = pd.read_csv(QUESTIONS_FILE)
        if 'Questions' not in df.columns:
            st.error("CSV file must have a 'Questions' column.")
            return []

        questions = df['Questions'].dropna().tolist()
        random.shuffle(questions)
        return questions[:num_questions]
    except FileNotFoundError:
        st.error("Questions file not found! Please contact the administrator.")
        st.stop()
        return []

# Save answers to CSV
def save_answers(student_name, questions, answers):
    df = pd.read_csv(QUESTIONS_FILE)
    if student_name in df.columns:
        st.warning(f"Answers for {student_name} already exist. Overwriting...")

    for i, question in enumerate(questions):
        df.loc[df['Questions'] == question, student_name] = answers[i]
    df.to_csv(QUESTIONS_FILE, index=False)
    st.success("Answers saved successfully!")

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'exam_started' not in st.session_state:
    st.session_state.exam_started = False
if 'submission_complete' not in st.session_state:
    st.session_state.submission_complete = False

# Streamlit UI
st.title("Online Exam Platform")
if st.session_state.submission_complete:
    # Show thank-you message after submission
    st.success("Thank you for submitting answers. You'll hear back from us soon!")
else:
    student_name = st.text_input("Enter your name:")
    #num_questions = st.number_input("Number of questions to attempt:", min_value=1, step=1)
    num_questions = 5

# Start the exam
if st.button("Start Exam") and student_name and num_questions:
    st.session_state.questions = load_questions(num_questions)
    st.session_state.answers = [""] * len(st.session_state.questions)
    st.session_state.exam_started = True

# Display questions and collect answers
if st.session_state.exam_started and st.session_state.questions:
    for i, question in enumerate(st.session_state.questions):
        st.session_state.answers[i] = st.text_area(question, value=st.session_state.answers[i], key=f"answer_{i}")

    if st.button("Submit Answers"):
        save_answers(student_name, st.session_state.questions, st.session_state.answers)
        st.session_state.exam_started = False
        st.session_state.submission_complete = True
        st.session_state.questions = []
        st.session_state.answers = []

