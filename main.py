import flask
from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return render_template('temp1.html',q1 = 'First Question')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        question1 = request.form['question1']
        question2 = request.form['question2']
        question3 = request.form['question3']
        
        # Save responses to CSV
        with open('responses.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, question1, question2, question3])
        
        return "Thank you for submitting your responses!"


if __name__ == '__main__':
    app.run(debug=True)
