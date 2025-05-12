#!/usr/bin/env python
"""
Sample Data Insertion Script for Hospital Management System
This script inserts sample data into the distributed database structure.
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random

def create_connection(host, user, password, database):
    """Create a connection to the MySQL server"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print(f"Connected to MySQL Server: {host}, Database: {database}")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Server: {host}, Database: {database}, Error: {e}")
        return None

def execute_query(connection, query, params=None):
    """Execute a query on the MySQL server"""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        return cursor.lastrowid
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

def insert_sample_patients(connection):
    """Insert sample patients into the patients database"""
    patients = [
        ("John", "Doe", "1980-05-15", "Male", "123 Main St", "555-1234", "john.doe@email.com"),
        ("Jane", "Smith", "1975-08-22", "Female", "456 Oak Ave", "555-5678", "jane.smith@email.com"),
        ("Michael", "Johnson", "1990-03-10", "Male", "789 Pine Rd", "555-9012", "michael.j@email.com"),
        ("Emily", "Williams", "1985-11-30", "Female", "321 Cedar Ln", "555-3456", "emily.w@email.com"),
        ("David", "Brown", "1972-07-18", "Male", "654 Birch Blvd", "555-7890", "david.b@email.com")
    ]
    
    query = """
    INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone, email)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    patient_ids = []
    for patient in patients:
        patient_id = execute_query(connection, query, patient)
        if patient_id:
            patient_ids.append(patient_id)
            print(f"Added patient: {patient[0]} {patient[1]}, ID: {patient_id}")
    
    return patient_ids

def insert_sample_doctors(connection):
    """Insert sample doctors into the appointments database"""
    doctors = [
        ("Robert", "Miller", "Cardiology", "555-2468", "robert.m@hospital.com"),
        ("Sarah", "Taylor", "Neurology", "555-1357", "sarah.t@hospital.com"),
        ("James", "Anderson", "Orthopedics", "555-3690", "james.a@hospital.com"),
        ("Jennifer", "Thomas", "Pediatrics", "555-8024", "jennifer.t@hospital.com"),
        ("William", "Jackson", "Dermatology", "555-7913", "william.j@hospital.com")
    ]
    
    query = """
    INSERT INTO doctors (first_name, last_name, specialization, phone, email)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    doctor_ids = []
    for doctor in doctors:
        doctor_id = execute_query(connection, query, doctor)
        if doctor_id:
            doctor_ids.append(doctor_id)
            print(f"Added doctor: {doctor[0]} {doctor[1]}, ID: {doctor_id}")
    
    return doctor_ids

def insert_sample_appointments(connection, patient_ids, doctor_ids):
    """Insert sample appointments into the appointments database"""
    # Generate dates for the next 30 days
    today = datetime.now().date()
    dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 31)]
    
    # Generate times throughout the day
    times = ['09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00']
    
    # Generate statuses
    statuses = ['Scheduled', 'Completed', 'Cancelled']
    
    appointments = []
    for _ in range(15):  # Create 15 random appointments
        patient_id = random.choice(patient_ids)
        doctor_id = random.choice(doctor_ids)
        date = random.choice(dates)
        time = random.choice(times)
        status = random.choice(statuses)
        notes = f"Appointment for patient {patient_id} with doctor {doctor_id}"
        
        appointments.append((patient_id, doctor_id, date, time, status, notes))
    
    query = """
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    appointment_ids = []
    for appointment in appointments:
        appointment_id = execute_query(connection, query, appointment)
        if appointment_id:
            appointment_ids.append(appointment_id)
            print(f"Added appointment: Patient {appointment[0]}, Doctor {appointment[1]}, Date: {appointment[2]}, ID: {appointment_id}")
    
    return appointment_ids

def insert_sample_invoices(connection, patient_ids, appointment_ids):
    """Insert sample invoices into the billing database"""
    # Generate dates for the last 30 days
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(0, 30)]
    
    # Generate statuses
    statuses = ['Pending', 'Paid', 'Cancelled']
    
    invoices = []
    for _ in range(10):  # Create 10 random invoices
        patient_id = random.choice(patient_ids)
        appointment_id = random.choice(appointment_ids) if appointment_ids else None
        amount = round(random.uniform(50.0, 500.0), 2)
        status = random.choice(statuses)
        issue_date = random.choice(dates)
        due_date = (datetime.strptime(issue_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
        payment_date = (datetime.strptime(issue_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 25))).strftime('%Y-%m-%d') if status == 'Paid' else None
        
        invoices.append((patient_id, appointment_id, amount, status, issue_date, due_date, payment_date))
    
    query = """
    INSERT INTO invoices (patient_id, appointment_id, amount, payment_status, issue_date, due_date, payment_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    for invoice in invoices:
        invoice_id = execute_query(connection, query, invoice)
        if invoice_id:
            print(f"Added invoice: Patient {invoice[0]}, Amount: ${invoice[2]}, ID: {invoice_id}")

def insert_sample_medical_records(connection, patient_ids, doctor_ids):
    """Insert sample medical records into the medical database"""
    diagnoses = [
        "Common Cold",
        "Influenza",
        "Hypertension",
        "Type 2 Diabetes",
        "Migraine",
        "Allergic Rhinitis",
        "Bronchitis",
        "Gastroenteritis",
        "Urinary Tract Infection",
        "Osteoarthritis"
    ]
    
    treatments = [
        "Rest and fluids",
        "Antibiotics prescribed",
        "Blood pressure medication",
        "Insulin therapy",
        "Pain management",
        "Antihistamines",
        "Bronchodilators",
        "Rehydration therapy",
        "Antibiotics and increased fluid intake",
        "Physical therapy and pain management"
    ]
    
    records = []
    for _ in range(12):  # Create 12 random medical records
        patient_id = random.choice(patient_ids)
        diagnosis = random.choice(diagnoses)
        treatment = random.choice(treatments)
        notes = f"Patient responded well to treatment."
        record_date = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
        doctor_id = random.choice(doctor_ids)
        
        records.append((patient_id, diagnosis, treatment, notes, record_date, doctor_id))
    
    query = """
    INSERT INTO medical_records (patient_id, diagnosis, treatment, notes, record_date, doctor_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for record in records:
        record_id = execute_query(connection, query, record)
        if record_id:
            print(f"Added medical record: Patient {record[0]}, Diagnosis: {record[1]}, ID: {record_id}")

def main():
    """Main function to insert sample data into all databases"""
    # Server configurations
    servers = {
        'server1': {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'databases': ['patients_db', 'medical_db']
        },
        'server2': {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'databases': ['appointments_db', 'billing_db']
        }
    }
    
    patient_ids = []
    doctor_ids = []
    appointment_ids = []
    
    # Insert data into patients_db
    print("\n=== Inserting data into patients_db ===")
    patients_conn = create_connection(
        servers['server1']['host'],
        servers['server1']['user'],
        servers['server1']['password'],
        'patients_db'
    )
    
    if patients_conn:
        patient_ids = insert_sample_patients(patients_conn)
        patients_conn.close()
    
    # Insert data into appointments_db
    print("\n=== Inserting data into appointments_db ===")
    appointments_conn = create_connection(
        servers['server2']['host'],
        servers['server2']['user'],
        servers['server2']['password'],
        'appointments_db'
    )
    
    if appointments_conn:
        doctor_ids = insert_sample_doctors(appointments_conn)
        if patient_ids and doctor_ids:
            appointment_ids = insert_sample_appointments(appointments_conn, patient_ids, doctor_ids)
        appointments_conn.close()
    
    # Insert data into billing_db
    print("\n=== Inserting data into billing_db ===")
    billing_conn = create_connection(
        servers['server2']['host'],
        servers['server2']['user'],
        servers['server2']['password'],
        'billing_db'
    )
    
    if billing_conn and patient_ids:
        insert_sample_invoices(billing_conn, patient_ids, appointment_ids)
        billing_conn.close()
    
    # Insert data into medical_db
    print("\n=== Inserting data into medical_db ===")
    medical_conn = create_connection(
        servers['server1']['host'],
        servers['server1']['user'],
        servers['server1']['password'],
        'medical_db'
    )
    
    if medical_conn and patient_ids and doctor_ids:
        insert_sample_medical_records(medical_conn, patient_ids, doctor_ids)
        medical_conn.close()
    
    print("\n=== Sample data insertion completed ===")

if __name__ == "__main__":
    main()
