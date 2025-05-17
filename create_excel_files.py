import pandas as pd
import os

# Create a directory for storing generated files
GENERATED_FOLDER = 'generated_files'
if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)

# Define sample data for timetable, students, supervisors, and classrooms
timetable_data = {
    'Branch': ['CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT'],
    'Date': ['2024-08-15', '2024-08-15', '2024-08-16', '2024-08-16', '2024-08-17', '2024-08-17', '2024-08-18', '2024-08-18', '2024-08-19', '2024-08-19'],
    'Time': ['09:00', '14:00', '09:00', '14:00', '09:00', '14:00', '09:00', '14:00', '09:00', '14:00'],
    'Classroom ID': ['C101', 'C102', 'C103', 'C104', 'C105', 'C106', 'C107', 'C108', 'C109', 'C110'],
    'Paper Name': ['Data Structures', 'Database Management', 'Algorithms', 'Networking', 'Operating Systems', 'Software Engineering', 'AI', 'Machine Learning', 'Data Science', 'Cloud Computing']
}

students_data = {
    'Student ID': [
        'EN21215001', 'EN21215002', 'EN21215003', 'EN21215004', 'EN21215005',
        'EN21215006', 'EN21215007', 'EN21215008', 'EN21215009', 'EN21215010',
        'EN21215011', 'EN21215012', 'EN21215013', 'EN21215014', 'EN21215015',
        'EN21215016', 'EN21215017', 'EN21215018', 'EN21215019', 'EN21215020',
        'EN21215021', 'EN21215022', 'EN21215023', 'EN21215024'
    ],
    'Student Name': [
        'Alice Smith', 'Bob Jones', 'Charlie Brown', 'Diana Prince', 'Eve Davis',
        'Frank Wright', 'Grace Lee', 'Henry Adams', 'Ivy Clark', 'Jack Hill',
        'Kathy Johnson', 'Louis Martinez', 'Mia Taylor', 'Nathan Wilson', 'Olivia Scott',
        'Paul Harris', 'Quinn Lewis', 'Rachel Walker', 'Sam Robinson', 'Tina Moore',
        'Ursula Thompson', 'Victor White', 'Wendy King', 'Xander Allen'
    ],
    'Branch': [
        'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT',
        'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT',
        'CSE', 'IT', 'CSE', 'IT'
    ],
    'Phone Number': [
        '7020454824', '555-0102', '555-0103', '555-0104', '555-0105', 
        '555-0106', '555-0107', '555-0108', '555-0109', '555-0110',
        '555-0111', '555-0112', '555-0113', '555-0114', '555-0115',
        '555-0116', '555-0117', '555-0118', '555-0119', '555-0120',
        '555-0121', '555-0122', '555-0123', '555-0124'
    ]
}

supervisors_data = {
    'Supervisor ID': [101, 102, 103, 104, 105, 106],
    'Supervisor Name': ['Dr. John Doe', 'Dr. Jane Smith', 'Dr. Emily Clark', 'Dr. Michael Brown', 'Dr. Sarah Miller', 'Dr. David Lee'],
    'Branch': ['CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT'],
    'Phone Number': [
        '555-1001', '555-1002', '555-1003', '555-1004', '555-1005', '555-1006'
    ]
}

classrooms_data = {
    'Classroom ID': ['C101', 'C102', 'C103', 'C104', 'C105'],
    'Capacity': [50, 30, 40, 35, 45]
}

# Save the data to CSV files
pd.DataFrame(timetable_data).to_csv(os.path.join(GENERATED_FOLDER, 'timetable.csv'), index=False)
pd.DataFrame(students_data).to_csv(os.path.join(GENERATED_FOLDER, 'students.csv'), index=False)
pd.DataFrame(supervisors_data).to_csv(os.path.join(GENERATED_FOLDER, 'supervisors.csv'), index=False)
pd.DataFrame(classrooms_data).to_csv(os.path.join(GENERATED_FOLDER, 'classrooms.csv'), index=False)

print("CSV files created successfully.")
