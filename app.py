import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import random

# Set up the Google Sheets API connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
creds = st.secrets["gcp_service_account"]

# Authorize with the credentials
credentials = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds), scope)
client = gspread.authorize(credentials)

# Load the Google Sheet (replace with your sheet name)
sheet = client.open("Exam Results").sheet1

# Load questions from the same repo
questions_file = "questions.csv"

# Load the CSV
try:
    df = pd.read_csv(questions_file)
except FileNotFoundError:
    st.error("questions.csv file not found in the repository.")
    st.stop()


def save_responses(questions, answers, student_name):
    # Save responses in a new sheet named after the student
    try:
        worksheet = client.open("QuestionnaireResponses").worksheet(student_name)
    except gspread.WorksheetNotFound:
        worksheet = client.open("QuestionnaireResponses").add_worksheet(title=student_name, rows="100", cols="2")
        worksheet.append_row(["Question", "Answer"])

    for q, a in zip(questions, answers):
        worksheet.append_row([q, a])


st.title("Python-Questionnaire")

num_questions = 5

if 'Questions' in df.columns:
    selected_questions = random.sample(df['Questions'].tolist(), num_questions)
    st.session_state.questions = selected_questions
    st.session_state.answers = [""] * len(selected_questions)
    st.session_state.student_name = st.text_input("Enter your name:")

    for i, question in enumerate(st.session_state.questions):
        st.session_state.answers[i] = st.text_area(question, st.session_state.answers[i])

    if st.button("Submit"):
        if st.session_state.student_name.strip():
            save_responses(st.session_state.questions, st.session_state.answers, st.session_state.student_name)
            st.empty()
            st.success("Thank you for submitting answers. You'll hear back from us soon!")
        else:
            st.error("Please enter your name before submitting.")
else:
    st.error("Questions column not found in the CSV file.")
