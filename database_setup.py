#!/usr/bin/env python
"""
Database Setup Script for Hospital Management System
This script initializes the distributed database structure across two servers.
"""

import mysql.connector
from mysql.connector import Error

def create_connection(host, user, password, database=None):
    """Create a connection to the MySQL server"""
    try:
        if database:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        else:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
        print(f"Connected to MySQL Server: {host}")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Server: {host}, Error: {e}")
        return None

def execute_query(connection, query):
    """Execute a query on the MySQL server"""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        return True
    except Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        cursor.close()

def setup_server(host, user, password):
    """Set up databases on a server"""
    # Connect to MySQL server
    connection = create_connection(host, user, password)
    if not connection:
        return False
    
    return connection

def create_database(connection, database_name):
    """Create a database if it doesn't exist"""
    query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
    return execute_query(connection, query)

def setup_patients_db(connection):
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
    return execute_query(connection, query)

def setup_medical_db(connection):
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    return execute_query(connection, query)

def setup_appointments_db(connection):
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
    if not execute_query(connection, doctors_query):
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
    return execute_query(connection, appointments_query)

def setup_billing_db(connection):
    """Set up the billing database structure"""
    # Create invoices table
    query = """
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT NOT NULL,
        appointment_id INT,
        amount DECIMAL(10, 2) NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending',
        issue_date DATE NOT NULL,
        due_date DATE NOT NULL,
        payment_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    return execute_query(connection, query)

def main():
    """Main function to set up all databases"""
    # Server configurations
    servers = {
        'server1': {
            'host': 'localhost',  # Using localhost for testing
            'user': 'root',
            'password': 'root',
            'databases': ['patients_db', 'medical_db']
        },
        'server2': {
            'host': 'localhost',  # Using localhost for testing
            'user': 'root',
            'password': 'root',
            'databases': ['appointments_db', 'billing_db']
        }
    }
    
    # Set up Server 1
    print("\n=== Setting up Server 1 ===")
    server1_conn = setup_server(
        servers['server1']['host'], 
        servers['server1']['user'], 
        servers['server1']['password']
    )
    
    if server1_conn:
        # Create databases on Server 1
        for db in servers['server1']['databases']:
            print(f"\nCreating database: {db}")
            if create_database(server1_conn, db):
                # Connect to the specific database
                db_conn = create_connection(
                    servers['server1']['host'],
                    servers['server1']['user'],
                    servers['server1']['password'],
                    db
                )
                
                if db_conn:
                    # Set up database structure based on database name
                    print(f"Setting up {db} structure")
                    if db == 'patients_db':
                        setup_patients_db(db_conn)
                    elif db == 'medical_db':
                        setup_medical_db(db_conn)
                    
                    db_conn.close()
        
        server1_conn.close()
    
    # Set up Server 2
    print("\n=== Setting up Server 2 ===")
    server2_conn = setup_server(
        servers['server2']['host'], 
        servers['server2']['user'], 
        servers['server2']['password']
    )
    
    if server2_conn:
        # Create databases on Server 2
        for db in servers['server2']['databases']:
            print(f"\nCreating database: {db}")
            if create_database(server2_conn, db):
                # Connect to the specific database
                db_conn = create_connection(
                    servers['server2']['host'],
                    servers['server2']['user'],
                    servers['server2']['password'],
                    db
                )
                
                if db_conn:
                    # Set up database structure based on database name
                    print(f"Setting up {db} structure")
                    if db == 'appointments_db':
                        setup_appointments_db(db_conn)
                    elif db == 'billing_db':
                        setup_billing_db(db_conn)
                    
                    db_conn.close()
        
        server2_conn.close()
    
    print("\n=== Database setup completed ===")

if __name__ == "__main__":
    main()
