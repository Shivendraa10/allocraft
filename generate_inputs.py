import pandas as pd
import os

# Create a directory for storing generated files
GENERATED_FOLDER = 'generated_files'
if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)

# Define sample data
timetable_data = {
    'Branch': ['CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT'],
    'Date': ['2024-08-15', '2024-08-15', '2024-08-16', '2024-08-16', '2024-08-17', '2024-08-17'],
    'Time': ['09:00', '14:00', '09:00', '14:00', '09:00', '14:00'],
    'Classroom ID': ['C101', 'C102', 'C103', 'C104', 'C105', 'C106'],
    'Paper Name': ['Data Structures', 'Database Management', 'Algorithms', 'Networking', 'Operating Systems', 'Software Engineering']
}
students_data = {
    'Student ID': [
        'EN21215001', 'EN21215002', 'EN21215003', 'EN21215004', 'EN21215005', 'EN21215006',
        'EN21215007', 'EN21215008', 'EN21215009', 'EN21215010', 'EN21215011', 'EN21215012',
        'EN21215013', 'EN21215014', 'EN21215015', 'EN21215016', 'EN21215017', 'EN21215018',
        'EN21215019', 'EN21215020', 'EN21215021', 'EN21215022', 'EN21215023', 'EN21215024'
    ],
    'Student Name': [
        'Alice Smith', 'Bob Jones', 'Charlie Brown', 'Diana Prince', 'Eve Davis', 'Frank Wright',
        'Grace Lee', 'Henry Adams', 'Ivy Clark', 'Jack Hill', 'Kathy Johnson', 'Louis Martinez',
        'Mia Taylor', 'Nathan Wilson', 'Olivia Scott', 'Paul Harris', 'Quinn Lewis', 'Rachel Walker',
        'Sam Robinson', 'Tina Moore', 'Ursula Thompson', 'Victor White', 'Wendy King', 'Xander Allen'
    ],
    'Branch': [
        'CSE', 'CSE', 'IT', 'IT', 'CSE', 'IT',
        'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT',
        'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT',
        'CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT'
    ],
    'Phone Number': [
        '9876543210', '9876543211', '9876543212', '9876543213', '9876543214', '9876543215',
        '9876543216', '9876543217', '9876543218', '9876543219', '9876543220', '9876543221',
        '9876543222', '9876543223', '9876543224', '9876543225', '9876543226', '9876543227',
        '9876543228', '9876543229', '9876543230', '9876543231', '9876543232', '9876543233'
    ]
}
supervisors_data = {
    'Supervisor ID': [101, 102, 103, 104, 105, 106],
    'Supervisor Name': ['Dr. John Doe', 'Dr. Jane Smith', 'Dr. Emily Clark', 'Dr. Michael Brown', 'Dr. Sarah Miller', 'Dr. David Lee'],
    'Branch': ['CSE', 'IT', 'CSE', 'IT', 'CSE', 'IT'],
    'Phone Number': ['9988776655', '9988776656', '9988776657', '9988776658', '9988776659', '9988776660']
}
classrooms_data = {
    'Classroom ID': ['C101', 'C102', 'C103', 'C104', 'C105'],
    'Capacity': [50, 30, 40, 35, 45]
}

# Save to CSV files
pd.DataFrame(timetable_data).to_csv(os.path.join(GENERATED_FOLDER, 'timetable.csv'), index=False)
pd.DataFrame(students_data).to_csv(os.path.join(GENERATED_FOLDER, 'students.csv'), index=False)
pd.DataFrame(supervisors_data).to_csv(os.path.join(GENERATED_FOLDER, 'supervisors.csv'), index=False)
pd.DataFrame(classrooms_data).to_csv(os.path.join(GENERATED_FOLDER, 'classrooms.csv'), index=False)

print("CSV files created successfully.")
