from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import pandas as pd
import os
import random
import subprocess
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_data'
FINAL_FILE = 'final_allocations.xlsx'

ADMIN_ID = 'admin123'
ADMIN_PASSWORD = 'adminpass'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

scheduler = BackgroundScheduler()
scheduler.start()


def send_sms_job():
    try:
        subprocess.run(['python', 'sendsms.py'], check=True)
        print("SMS sent successfully.")
    except Exception as e:
        print("Error sending SMS:", str(e))


@app.route('/')
def dashboard():
    if session.get('logged_in'):
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['admin_id'] == ADMIN_ID and request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/upload_files', methods=['POST'])
def upload_files():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    timetable_file = request.files.get('timetable')
    students_file = request.files.get('students')
    supervisors_file = request.files.get('supervisors')
    classrooms_file = request.files.get('classrooms')

    if not all([timetable_file, students_file, supervisors_file, classrooms_file]):
        flash('All files are required!', 'danger')
        return redirect(url_for('dashboard'))

    timetable_path = os.path.join(UPLOAD_FOLDER, 'timetable.csv')
    students_path = os.path.join(UPLOAD_FOLDER, 'students.csv')
    supervisors_path = os.path.join(UPLOAD_FOLDER, 'supervisors.csv')
    classrooms_path = os.path.join(UPLOAD_FOLDER, 'classrooms.csv')

    timetable_file.save(timetable_path)
    students_file.save(students_path)
    supervisors_file.save(supervisors_path)
    classrooms_file.save(classrooms_path)

    try:
        timetable_df = pd.read_csv(timetable_path, encoding='ISO-8859-1')
        students_df = pd.read_csv(students_path, encoding='ISO-8859-1')
        supervisors_df = pd.read_csv(supervisors_path, encoding='ISO-8859-1')
        classrooms_df = pd.read_csv(classrooms_path, encoding='ISO-8859-1')

        timetable = timetable_df.to_dict(orient='records')
        students = students_df.to_dict(orient='records')
        supervisors = supervisors_df.to_dict(orient='records')
        classrooms = classrooms_df.to_dict(orient='records')

        allocations = []

        for exam in timetable:
            exam_branch = exam['Branch']
            paper = exam['Paper Name']
            date = exam['Date']
            time = exam['Time']

            branch_students = [s for s in students if s['Branch'] == exam_branch]

            for classroom in classrooms:
                if len(branch_students) == 0:
                    break

                capacity = int(classroom.get('Capacity', 0))
                if capacity <= 0:
                    continue

                assigned_students = branch_students[:capacity]
                branch_students = branch_students[capacity:]
                classroom['Capacity'] -= len(assigned_students)

                branch_supervisors = [s for s in supervisors if s['Branch'] == exam_branch]
                supervisor = random.choice(branch_supervisors)['Supervisor Name'] if branch_supervisors else "Not Assigned"

                allocations.append({
                    'Date': date,
                    'Time': time,
                    'Classroom': classroom['Classroom ID'],
                    'Paper': paper,
                    'Students': assigned_students,
                    'Supervisor': supervisor
                })

        output = []
        for alloc in allocations:
            student_list = ', '.join([f"{s['Student Name']} (ID: {s['Student ID']})" for s in alloc['Students']])
            output.append({
                'Date': alloc['Date'],
                'Time': alloc['Time'],
                'Classroom': alloc['Classroom'],
                'Paper': alloc['Paper'],
                'Students': student_list,
                'Supervisor': alloc['Supervisor']
            })

        pd.DataFrame(output).to_excel(os.path.join(PROCESSED_FOLDER, FINAL_FILE), index=False)

        flash('Files processed successfully. Now you can schedule SMS.', 'success')
        return redirect(url_for('schedule_sms'))

    except Exception as e:
        flash(f'Error while processing: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/schedule_sms', methods=['GET', 'POST'])
def schedule_sms():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        sms_date = request.form['sms_date']  # yyyy-mm-dd
        sms_time = request.form['sms_time']  # HH:MM (24-hour)

        try:
            # Combine date and time into datetime object
            datetime_str = f"{sms_date} {sms_time}"
            scheduled_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            # Remove any existing job with same id before scheduling new one
            if scheduler.get_job('sms_job'):
                scheduler.remove_job('sms_job')

            # Schedule SMS sending once at the specified date and time
            scheduler.add_job(send_sms_job, trigger=DateTrigger(run_date=scheduled_datetime), id='sms_job')

            flash(f'SMS scheduled for {scheduled_datetime.strftime("%Y-%m-%d %H:%M")}', 'success')
            return redirect(url_for('results'))

        except Exception as e:
            flash(f'Invalid date/time format or scheduling error: {e}', 'danger')
            return redirect(url_for('schedule_sms'))

    return render_template('schedule_sms.html')


@app.route('/results')
def results():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    file_path = os.path.join(PROCESSED_FOLDER, FINAL_FILE)
    allocations = []

    if os.path.isfile(file_path):
        df = pd.read_excel(file_path)
        allocations = df.to_dict(orient='records')

    return render_template('results.html', allocations=allocations, file_exists=os.path.isfile(file_path))


@app.route('/download')
def download_file():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory(PROCESSED_FOLDER, FINAL_FILE, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
