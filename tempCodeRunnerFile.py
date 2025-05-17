from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import pandas as pd
import os
import random
import subprocess


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_data'
FINAL_FILE = 'final_allocations.xlsx'

# Hardcoded admin credentials
ADMIN_ID = 'admin123'
ADMIN_PASSWORD = 'adminpass'

if not os.path.exists(UPLOAD_FOLDER):     
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route('/')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']

        if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid admin credentials. Please try again.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/upload_files', methods=['POST'])
def upload_files():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    timetable_file = request.files.get('timetable')
    students_file = request.files.get('students')
    supervisors_file = request.files.get('supervisors')
    classrooms_file = request.files.get('classrooms')

    if not (timetable_file and students_file and supervisors_file and classrooms_file):
        flash('All files must be provided!', 'danger')
        return redirect(url_for('dashboard'))

    try:
        timetable_path = os.path.join(UPLOAD_FOLDER, 'timetable.csv')
        students_path = os.path.join(UPLOAD_FOLDER, 'students.csv')
        supervisors_path = os.path.join(UPLOAD_FOLDER, 'supervisors.csv')
        classrooms_path = os.path.join(UPLOAD_FOLDER, 'classrooms.csv')

        timetable_file.save(timetable_path)
        students_file.save(students_path)
        supervisors_file.save(supervisors_path)
        classrooms_file.save(classrooms_path)

        timetable_df = pd.read_csv(timetable_path, encoding='ISO-8859-1', on_bad_lines='warn')
        students_df = pd.read_csv(students_path, encoding='ISO-8859-1', on_bad_lines='warn')
        supervisors_df = pd.read_csv(supervisors_path, encoding='ISO-8859-1', on_bad_lines='warn')
        classrooms_df = pd.read_csv(classrooms_path, encoding='ISO-8859-1', on_bad_lines='warn')

        # Allocate students to classrooms
        classrooms = classrooms_df.to_dict(orient='records')
        students = students_df.to_dict(orient='records')
        timetable = timetable_df.to_dict(orient='records')
        supervisors = supervisors_df.to_dict(orient='records')

        allocations = []
        supervisor_assignments = {}

        for exam in timetable:
            exam_branch = exam['Branch']
            classroom = next((c for c in classrooms if c['Capacity'] > 0), None)
            if classroom:
                classroom['Capacity'] -= 1
                students_in_class = [s for s in students if s['Branch'] == exam_branch]
                num_seats = min(classroom['Capacity'], len(students_in_class))
                
                # Allocate all students for the paper (or as many as fit in the classroom)
                allocated_students = students_in_class[:num_seats]
                allocations.append({
                    'Date': exam['Date'],
                    'Time': exam['Time'],
                    'Classroom': classroom['Classroom ID'],
                    'Paper': exam['Paper Name'],
                    'Students': allocated_students
                })

                # Assign a supervisor to the classroom
                supervisor = random.choice([s for s in supervisors if s['Branch'] == exam_branch])
                supervisor_assignments[classroom['Classroom ID']] = supervisor['Supervisor Name']

        # Format the data for saving to Excel
        allocation_data = []
        for alloc in allocations:
            students_list = ', '.join([f"{s['Student Name']} (ID: {s['Student ID']})" for s in alloc['Students']])
            allocation_data.append({
                'Date': alloc['Date'],
                'Time': alloc['Time'],
                'Classroom': alloc['Classroom'],
                'Paper': alloc['Paper'],
                'Students': students_list,
                'Supervisor': supervisor_assignments.get(alloc['Classroom'], 'Not Assigned')
            })

        # Save allocations to Excel
        allocation_df = pd.DataFrame(allocation_data)
        allocation_df.to_excel(os.path.join(PROCESSED_FOLDER, FINAL_FILE), index=False)

        # Run the SMS sending script (assuming it's in the project folder)
        subprocess.run(['python', 'sendsms.py'], check=True)

        return redirect(url_for('results'))

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/results')
def results():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    file_exists = os.path.isfile(os.path.join(PROCESSED_FOLDER, FINAL_FILE))
    allocations = []

    if file_exists:
        allocations_path = os.path.join(PROCESSED_FOLDER, FINAL_FILE)
        allocations_df = pd.read_excel(allocations_path)
        allocations = allocations_df.to_dict(orient='records')

    return render_template('results.html', allocations=allocations, file_exists=file_exists)

@app.route('/download')
def download_file():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    return send_from_directory(PROCESSED_FOLDER, FINAL_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
