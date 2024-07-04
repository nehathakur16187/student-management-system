from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Student {self.first_name} {self.last_name}>"

# Create the database and the table
with app.app_context():
    db.create_all()

# Routes for HTML templates

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob_str = request.form['dob']
        amount_due = request.form['amount_due']
        
        # Convert the dob string to a date object
        dob = date.fromisoformat(dob_str)
        
        new_student = Student(first_name=first_name, last_name=last_name, dob=dob, amount_due=amount_due)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_student.html')

@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        dob_str = request.form['dob']
        student.amount_due = request.form['amount_due']
        
        # Convert the dob string to a date object
        student.dob = date.fromisoformat(dob_str)
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_student.html', student=student)

@app.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
