from flask import Flask, render_template, request
import csv
import random

app = Flask(__name__)

# Configurable variable for the number of questions
NUM_QUESTIONS = 3  # Teacher can change this value
QUESTIONS_FILE = 'questions.csv'

# Load and shuffle questions from CSV

def load_questions():
    questions = []
    try:
        with open(QUESTIONS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                questions.append({'index': index, 'question': row['Questions']})  # Store index with question
    except (FileNotFoundError, KeyError):
        questions = [{'index': 0, 'question': "No questions available"}]
    
    random.shuffle(questions)
    return questions[:NUM_QUESTIONS]


@app.route('/', methods=['GET', 'POST'])
def exam():
    questions = load_questions()
    if request.method == 'POST':
        student_name = request.form['name']
        answers = {}
        
        for i in range(len(questions)):
            index = request.form.get(f'index{i+1}')
            if index is not None:
                answers[int(index)] = request.form.get(f'question{i+1}')

        # Update CSV with answers mapped to original question indices
        try:
            rows = []
            with open(QUESTIONS_FILE, 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames + [student_name]
                
                for i, row in enumerate(reader):
                    if i in answers:
                        row[student_name] = answers[i]
                    rows.append(row)
            
            with open(QUESTIONS_FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        
        except Exception as e:
            return f"Error saving answers: {e}"
        
        return "Thank you for submitting the exam!"

    return render_template('temp2.html', questions=questions)


if __name__ == '__main__':
    app.run(debug=True)

