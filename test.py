import pandas as pd
from twilio.rest import Client
import os

# Twilio credentials (replace these with your actual Twilio credentials)
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PH_NO') # Your Twilio phone number in E.164 format
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_ACCOUNT_SID')

# Directory for generated files
GENERATED_FOLDER = 'generated_files'

# Initialize Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Read the CSV files
students_df = pd.read_csv(os.path.join(GENERATED_FOLDER, 'students.csv'))
supervisors_df = pd.read_csv(os.path.join(GENERATED_FOLDER, 'supervisors.csv'))
classrooms_df = pd.read_csv(os.path.join(GENERATED_FOLDER, 'classrooms.csv'))
timetable_df = pd.read_csv(os.path.join(GENERATED_FOLDER, 'timetable.csv'))

# Function to send SMS using Twilio
def send_sms(phone_number, message):
    # Ensure phone number is in E.164 format (e.g., +919876543210)
    phone_number = str(phone_number)  # Convert phone number to string
    if not phone_number.startswith('+'):
        phone_number = '+91' + phone_number  # Assuming the country code is India

    try:
        message = client.messages.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,  # Your Twilio phone number
            body=message
        )
        print(f"Message sent to {phone_number}: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")

# Function to send notifications to students and supervisors
def send_notifications():
    for idx, student in students_df.iterrows():
        student_name = student['Student Name']
        student_phone = student['Phone Number']
        student_branch = student['Branch']
        
        # Get the corresponding exam details from the timetable
        exam_details = timetable_df[timetable_df['Branch'] == student_branch].iloc[0]
        exam_date = exam_details['Date']
        exam_time = exam_details['Time']
        classroom = exam_details['Classroom ID']
        paper_name = exam_details['Paper Name']
        
        # Prepare the student message
        student_message = f"Hello {student_name}, your exam for {paper_name} is on {exam_date} at {exam_time} in classroom {classroom}. Best of luck!"

        # Send SMS to the student
        send_sms(student_phone, student_message)

    for idx, supervisor in supervisors_df.iterrows():
        supervisor_name = supervisor['Supervisor Name']
        supervisor_phone = supervisor['Phone Number']
        
        # Prepare the supervisor message
        supervisor_message = f"Hello {supervisor_name}, you are assigned as the supervisor for the exam in classroom. Please check the schedule for your assigned paper."

        # Send SMS to the supervisor
        send_sms(supervisor_phone, supervisor_message)

# Example of sending notifications to students and supervisors
send_notifications()
print("Messages sent successfully.")
