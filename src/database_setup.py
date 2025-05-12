#!/usr/bin/env python
"""
Hospital Management System Database Setup
This module provides functions for setting up and initializing the database.
"""

import mysql.connector
from mysql.connector import connect, Error
import argparse
import sys
import os
import random
from datetime import datetime, timedelta

class DatabaseSetup:
    """
    Handles database setup operations including creating databases,
    tables, and sample data.
    """
    def __init__(self, debug_mode=False):
        """Initialize the database setup with server configurations"""
        self.debug_mode = debug_mode
        
        # Server configurations
        self.servers = {
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
    
    def create_connection(self, host, user, password, database=None):
        """Create a connection to the MySQL server"""
        try:
            connection_config = {
                'host': host,
                'user': user,
                'password': password
            }
            
            if database:
                connection_config['database'] = database
                
            connection = connect(**connection_config)
            
            if self.debug_mode:
                print(f"Connected to MySQL server at {host}" + (f", database {database}" if database else ""))
                
            return connection
        except Error as e:
            if self.debug_mode:
                print(f"Error connecting to MySQL server: {e}")
            return None
    
    def execute_query(self, connection, query, params=None):
        """Execute a query on the MySQL server"""
        try:
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # If the query is a SELECT statement, return the results
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                cursor.close()
                return result
            # If the query is an INSERT statement, return the last inserted ID
            elif query.strip().upper().startswith('INSERT'):
                connection.commit()
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
            # For other queries, just commit the transaction
            else:
                connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows
                
        except Error as e:
            if self.debug_mode:
                print(f"Error executing query: {e}")
                print(f"Query: {query}")
                if params:
                    print(f"Parameters: {params}")
            return None
    
    def setup_database(self):
        """Set up all databases and tables"""
        if self.debug_mode:
            print("=== Setting up databases ===")
            
        # Set up databases on server1
        server1_config = self.servers['server1']
        server1_conn = self.create_connection(server1_config['host'], server1_config['user'], server1_config['password'])
        
        if not server1_conn:
            if self.debug_mode:
                print("Failed to connect to server1")
            return False
            
        # Create databases on server1
        for db in server1_config['databases']:
            query = f"CREATE DATABASE IF NOT EXISTS {db}"
            if not self.execute_query(server1_conn, query):
                if self.debug_mode:
                    print(f"Failed to create database {db} on server1")
                server1_conn.close()
                return False
            elif self.debug_mode:
                print(f"Created database {db} on server1")
                
        # Set up tables in each database on server1
        for db in server1_config['databases']:
            db_conn = self.create_connection(server1_config['host'], server1_config['user'], server1_config['password'], db)
            
            if not db_conn:
                if self.debug_mode:
                    print(f"Failed to connect to database {db} on server1")
                server1_conn.close()
                return False
                
            if db == 'patients_db':
                if not self.setup_patients_db(db_conn):
                    if self.debug_mode:
                        print(f"Failed to set up patients_db on server1")
                    db_conn.close()
                    server1_conn.close()
                    return False
                elif self.debug_mode:
                    print(f"Set up patients_db on server1")
            elif db == 'medical_db':
                if not self.setup_medical_db(db_conn):
                    if self.debug_mode:
                        print(f"Failed to set up medical_db on server1")
                    db_conn.close()
                    server1_conn.close()
                    return False
                elif self.debug_mode:
                    print(f"Set up medical_db on server1")
                    
            db_conn.close()
            
        server1_conn.close()
        
        # Set up databases on server2
        server2_config = self.servers['server2']
        server2_conn = self.create_connection(server2_config['host'], server2_config['user'], server2_config['password'])
        
        if not server2_conn:
            if self.debug_mode:
                print("Failed to connect to server2")
            return False
            
        # Create databases on server2
        for db in server2_config['databases']:
            query = f"CREATE DATABASE IF NOT EXISTS {db}"
            if not self.execute_query(server2_conn, query):
                if self.debug_mode:
                    print(f"Failed to create database {db} on server2")
                server2_conn.close()
                return False
            elif self.debug_mode:
                print(f"Created database {db} on server2")
                
        # Set up tables in each database on server2
        for db in server2_config['databases']:
            db_conn = self.create_connection(server2_config['host'], server2_config['user'], server2_config['password'], db)
            
            if not db_conn:
                if self.debug_mode:
                    print(f"Failed to connect to database {db} on server2")
                server2_conn.close()
                return False
                
            if db == 'appointments_db':
                if not self.setup_appointments_db(db_conn):
                    if self.debug_mode:
                        print(f"Failed to set up appointments_db on server2")
                    db_conn.close()
                    server2_conn.close()
                    return False
                elif self.debug_mode:
                    print(f"Set up appointments_db on server2")
            elif db == 'billing_db':
                if not self.setup_billing_db(db_conn):
                    if self.debug_mode:
                        print(f"Failed to set up billing_db on server2")
                    db_conn.close()
                    server2_conn.close()
                    return False
                elif self.debug_mode:
                    print(f"Set up billing_db on server2")
                    
            db_conn.close()
            
        server2_conn.close()
        
        if self.debug_mode:
            print("=== Database setup completed successfully ===")
            
        return True
    
    def setup_patients_db(self, connection):
        """Set up the patients database structure"""
        # Create patients table
        query = """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE NOT NULL,
            gender VARCHAR(10),
            address VARCHAR(255),
            phone VARCHAR(20),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, query)
    
    def setup_medical_db(self, connection):
        """Set up the medical database structure"""
        # Create medical_records table
        query = """
        CREATE TABLE IF NOT EXISTS medical_records (
            record_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            diagnosis TEXT,
            treatment TEXT,
            notes TEXT,
            record_date DATE NOT NULL,
            doctor_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, query)
    
    def setup_appointments_db(self, connection):
        """Set up the appointments database structure"""
        # Create doctors table
        doctors_query = """
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            specialization VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        if not self.execute_query(connection, doctors_query):
            return False
        
        # Create appointments table
        appointments_query = """
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            status VARCHAR(20) DEFAULT 'Scheduled',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, appointments_query)
    
    def setup_billing_db(self, connection):
        """Set up the billing database structure"""
        # Create invoices table
        query = """
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            appointment_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            payment_status VARCHAR(20) DEFAULT 'Pending',
            issue_date DATE NOT NULL,
            due_date DATE NOT NULL,
            payment_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, query)
    
    def generate_sample_data(self):
        """Generate sample data for all databases"""
        # Create database manager for executing queries
        from src.models.database_utils import DatabaseManager
        db_manager = DatabaseManager(debug_mode=self.debug_mode)
        
        # Insert sample patients
        patient_ids = self.insert_sample_patients(db_manager)
        
        # Insert sample doctors
        doctor_ids = self.insert_sample_doctors(db_manager)
        
        if patient_ids and doctor_ids:
            # Insert sample appointments
            appointment_ids = self.insert_sample_appointments(db_manager, patient_ids, doctor_ids)
            
            # Insert sample invoices
            self.insert_sample_invoices(db_manager, patient_ids, appointment_ids)
            
            # Insert sample medical records
            self.insert_sample_medical_records(db_manager, patient_ids, doctor_ids)
            
            if self.debug_mode:
                print("\n=== Sample data generation completed ===")
                
            return True
        else:
            if self.debug_mode:
                print("Failed to generate sample data")
            return False
    
    def insert_sample_patients(self, db_manager):
        """Insert sample patients into the patients database"""
        if self.debug_mode:
            print("\n=== Inserting sample patients ===")
            
        # Sample patient data
        patients = [
            ('John', 'Doe', '1980-05-15', 'Male', '123 Main St', '555-1234', 'john.doe@email.com'),
            ('Jane', 'Smith', '1975-08-22', 'Female', '456 Oak Ave', '555-5678', 'jane.smith@email.com'),
            ('Michael', 'Johnson', '1990-03-10', 'Male', '789 Pine Rd', '555-9012', 'michael.j@email.com'),
            ('Emily', 'Williams', '1985-11-28', 'Female', '321 Cedar Ln', '555-3456', 'emily.w@email.com'),
            ('Robert', 'Brown', '1972-07-04', 'Male', '654 Maple Dr', '555-7890', 'robert.b@email.com')
        ]
        
        query = """
        INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        patient_ids = []
        for patient in patients:
            patient_id = db_manager.execute_query('patients_db', query, patient)
            if patient_id:
                patient_ids.append(patient_id)
                if self.debug_mode:
                    print(f"Added patient: {patient[0]} {patient[1]}, ID: {patient_id}")
        
        return patient_ids
    
    def insert_sample_doctors(self, db_manager):
        """Insert sample doctors into the appointments database"""
        if self.debug_mode:
            print("\n=== Inserting sample doctors ===")
            
        # Sample doctor data
        doctors = [
            ('David', 'Miller', 'Cardiology', '555-2468', 'david.m@hospital.com'),
            ('Sarah', 'Taylor', 'Neurology', '555-1357', 'sarah.t@hospital.com'),
            ('James', 'Anderson', 'Orthopedics', '555-3690', 'james.a@hospital.com'),
            ('Lisa', 'Wilson', 'Pediatrics', '555-4812', 'lisa.w@hospital.com'),
            ('Thomas', 'Moore', 'Dermatology', '555-5926', 'thomas.m@hospital.com')
        ]
        
        query = """
        INSERT INTO doctors (first_name, last_name, specialization, phone, email)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        doctor_ids = []
        for doctor in doctors:
            doctor_id = db_manager.execute_query('appointments_db', query, doctor)
            if doctor_id:
                doctor_ids.append(doctor_id)
                if self.debug_mode:
                    print(f"Added doctor: {doctor[0]} {doctor[1]}, ID: {doctor_id}")
        
        return doctor_ids
    
    def insert_sample_appointments(self, db_manager, patient_ids, doctor_ids):
        """Insert sample appointments into the appointments database"""
        if self.debug_mode:
            print("\n=== Inserting sample appointments ===")
            
        # Generate random appointments
        appointments = []
        today = datetime.now().date()
        
        for _ in range(15):
            patient_id = random.choice(patient_ids)
            doctor_id = random.choice(doctor_ids)
            
            # Random date within 30 days (past or future)
            days_offset = random.randint(-15, 15)
            appointment_date = today + timedelta(days=days_offset)
            
            # Random time between 9 AM and 5 PM
            hour = random.randint(9, 16)
            minute = random.choice([0, 15, 30, 45])
            appointment_time = f"{hour:02d}:{minute:02d}:00"
            
            # Random status
            status = random.choice(['Scheduled', 'Completed', 'Cancelled', 'No-show'])
            
            appointments.append((patient_id, doctor_id, appointment_date, appointment_time, status, ''))
        
        query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        appointment_ids = []
        for appointment in appointments:
            appointment_id = db_manager.execute_query('appointments_db', query, appointment)
            if appointment_id:
                appointment_ids.append(appointment_id)
                if self.debug_mode:
                    print(f"Added appointment: Patient {appointment[0]}, Doctor {appointment[1]}, ID: {appointment_id}")
        
        return appointment_ids
    
    def insert_sample_invoices(self, db_manager, patient_ids, appointment_ids):
        """Insert sample invoices into the billing database"""
        if self.debug_mode:
            print("\n=== Inserting sample invoices ===")
            
        # Generate random invoices
        invoices = []
        today = datetime.now().date()
        
        for _ in range(10):
            patient_id = random.choice(patient_ids)
            appointment_id = random.choice(appointment_ids) if appointment_ids else None
            
            # Random amount between $50 and $500
            amount = round(random.uniform(50, 500), 2)
            
            # Random status
            status = random.choice(['Pending', 'Paid', 'Cancelled'])
            
            # Random dates
            days_offset = random.randint(-30, 0)
            issue_date = today + timedelta(days=days_offset)
            due_date = issue_date + timedelta(days=30)
            
            # Payment date only if status is Paid
            payment_date = None
            if status == 'Paid':
                payment_days_offset = random.randint(1, 20)
                payment_date = issue_date + timedelta(days=payment_days_offset)
            
            invoices.append((patient_id, appointment_id, amount, status, issue_date, due_date, payment_date))
        
        query = """
        INSERT INTO invoices (patient_id, appointment_id, amount, payment_status, issue_date, due_date, payment_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for invoice in invoices:
            invoice_id = db_manager.execute_query('billing_db', query, invoice)
            if invoice_id and self.debug_mode:
                print(f"Added invoice: Patient {invoice[0]}, Amount: ${invoice[2]}, ID: {invoice_id}")
    
    def insert_sample_medical_records(self, db_manager, patient_ids, doctor_ids):
        """Insert sample medical records into the medical database"""
        if self.debug_mode:
            print("\n=== Inserting sample medical records ===")
            
        # Sample diagnoses and treatments
        diagnoses = ['Common Cold', 'Influenza', 'Hypertension', 'Diabetes', 'Allergic Rhinitis', 
                    'Bronchitis', 'Urinary Tract Infection', 'Gastroenteritis', 'Migraine', 'Osteoarthritis']
        
        treatments = ['Rest and fluids', 'Antibiotics prescribed', 'Antihistamines', 
                     'Physical therapy and pain management', 'Antibiotics and increased fluid intake',
                     'Insulin therapy', 'Rehydration therapy', 'Pain management']
        
        # Generate random medical records
        records = []
        today = datetime.now().date()
        
        for _ in range(12):
            patient_id = random.choice(patient_ids)
            doctor_id = random.choice(doctor_ids)
            
            diagnosis = random.choice(diagnoses)
            treatment = random.choice(treatments)
            notes = "Patient responded well to treatment."
            
            # Random date within 60 days (past)
            days_offset = random.randint(-60, 0)
            record_date = today + timedelta(days=days_offset)
            
            records.append((patient_id, diagnosis, treatment, notes, record_date, doctor_id))
        
        query = """
        INSERT INTO medical_records (patient_id, diagnosis, treatment, notes, record_date, doctor_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for record in records:
            record_id = db_manager.execute_query('medical_db', query, record)
            if record_id and self.debug_mode:
                print(f"Added medical record: Patient {record[0]}, Diagnosis: {record[1]}, ID: {record_id}")


def initialize_database(setup_tables=True, add_sample_data=True, debug_mode=False):
    """
    Initialize the database with tables and sample data
    
    Args:
        setup_tables (bool): Whether to create database tables
        add_sample_data (bool): Whether to add sample data
        debug_mode (bool): Whether to print debug information
    """
    db_setup = DatabaseSetup(debug_mode=debug_mode)
    
    if setup_tables:
        db_setup.setup_database()
    
    if add_sample_data:
        db_setup.generate_sample_data()
    
    if debug_mode:
        print("\nSetup completed successfully!")
        print("\nTo run the application, use the following command:")
        print("python src/main.py")


def main():
    """Main function to set up the Hospital Management System database"""
    parser = argparse.ArgumentParser(description='Hospital Management System Database Setup')
    
    parser.add_argument('--no-tables', action='store_true',
                        help='Skip creating database tables')
    
    parser.add_argument('--no-sample-data', action='store_true',
                        help='Skip generating sample data')
    
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode with verbose output')
    
    args = parser.parse_args()
    
    # Initialize the database
    initialize_database(
        setup_tables=not args.no_tables,
        add_sample_data=not args.no_sample_data,
        debug_mode=args.debug
    )


if __name__ == "__main__":
    main()
