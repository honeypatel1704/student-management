!pip install flask
!pip install pymongo
!pip install python-dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
     

app = Flask(__name__)
     

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['student_db']
students = db['students']
     

@app.route('/')
def home():
    return render_template('base.html')
     

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_data = {
            'name': request.form['name'],
            'father_name': request.form['father_name'],
            'mother_name': request.form['mother_name'],
            'birthdate': datetime.strptime(request.form['birthdate'], '%Y-%m-%d'),
            'address': request.form['address'],
            'student_phone': request.form['student_phone'],
            'father_phone': request.form['father_phone'],
            'enrollment_number': request.form['enrollment_number'],
            'class': request.form['class'],
            'batch': request.form['batch'],
            'email': request.form['email'],
            'linkedin': request.form.get('linkedin', ''),
            'github': request.form.get('github', ''),
            'created_at': datetime.now()
        }
        students.insert_one(student_data)
        return redirect(url_for('home'))
    return render_template('add_student.html')
     

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = {}
        if request.form['search_term']:
            query['$or'] = [
                {'name': {'$regex': request.form['search_term'], '$options': 'i'}},
                {'enrollment_number': request.form['search_term']}
            ]
        results = list(students.find(query))
        return render_template('search.html', results=results)
    return render_template('search.html', results=None)
     

@app.route('/student/')
def student_details(enrollment_number):
    student = students.find_one({'enrollment_number': enrollment_number})
    if student:
        # Convert date to string for display
        student['birthdate'] = student['birthdate'].strftime('%Y-%m-%d')
        return render_template('student_details.html', student=student)
    return "Student not found", 404
     

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
