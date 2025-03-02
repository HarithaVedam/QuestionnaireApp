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
        st.error("Questions file not found!")
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

# Streamlit UI
st.title("Online Exam Platform")

student_name = st.text_input("Enter your name:")
num_questions = 5
#num_questions = st.number_input("Number of questions to attempt:", min_value=1, step=1)

if st.button("Start Exam") and student_name and num_questions:
    questions = load_questions(num_questions)
    
    if questions:
        answers = []
        for question in questions:
            answers.append(st.text_area(question))
        
        if st.button("Submit Answers"):
            save_answers(student_name, questions, answers)

#st.info("Upload a CSV file with a 'Questions' column to get started.")

# To run the app locally: `streamlit run app.py`
# For deployment: Push to GitHub and deploy via Streamlit Community Cloud!
