from flask import Flask, render_template, request, redirect
import csv
import random

app = Flask(__name__)

# Configurable variable for the number of questions
NUM_QUESTIONS = 3  # Teacher can change this value
QUESTIONS_FILE = 'questions.csv'

# Load questions from CSV
def load_questions():
    questions = []
    try:
        with open(QUESTIONS_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                questions.append(row[0])
    except FileNotFoundError:
        questions = ["No questions available"]
    random.shuffle(questions)  # Shuffle questions
    return questions[:NUM_QUESTIONS]


@app.route('/', methods=['GET', 'POST'])
def exam():
    questions = load_questions()
    if request.method == 'POST':
        student_name = request.form['name']
        answers = {f'Q{i + 1}': request.form.get(f'question{i + 1}') for i in range(len(questions))}
        
        # Save answers to CSV
        with open(QUESTIONS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            row = [student_name] + list(answers.values())
            writer.writerow(row)
        
        return "Thank you for submitting the exam!"

    return render_template('temp2.html', questions=questions)


if __name__ == '__main__':
    app.run(debug=True)