import streamlit as st
import pandas as pd
import random
import gspread
from google.oauth2.service_account import Credentials


QUESTIONS_FILE = 'questions.csv'
SHEET_NAME = 'Exam Results'
CREDENTIALS_FILE = 'questionnaireapp-452611-633c53c55ba7.json'

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
    
# Save answers to Google Sheets
def save_answers_to_google_sheets(student_name, questions, answers):
    # Authenticate with Google Sheets
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    
    # Open the spreadsheet
    try:
        sheet = client.open(SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        st.error(f"Spreadsheet '{SHEET_NAME}' not found. Make sure it exists and is shared with your service account.")
        return
    
    # Create a new sheet for the student (or overwrite if exists)
    try:
        worksheet = sheet.worksheet(student_name)
        sheet.del_worksheet(worksheet)  # Delete existing sheet if resubmitting
    except gspread.WorksheetNotFound:
        pass  # No existing sheet, so we can create a new one

    # Add the student's answers
    worksheet = sheet.add_worksheet(title=student_name, rows=len(questions) + 1, cols=2)
    worksheet.update([["Questions", "Answers"]] + list(zip(questions, answers)))

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
            save_answers_to_google_sheets(student_name, st.session_state.questions, st.session_state.answers)
            st.session_state.exam_started = False
            st.session_state.submission_complete = True
            