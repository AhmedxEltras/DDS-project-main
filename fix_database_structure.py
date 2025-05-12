#!/usr/bin/env python
"""
Database Structure Fix Script for Hospital Management System
This script fixes the structure of tables in the distributed database.
"""

import mysql.connector
from mysql.connector import Error

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

def fix_billing_db(connection):
    """Fix the structure of the invoices table in billing_db"""
    # Check if status column exists
    check_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'billing_db' 
    AND TABLE_NAME = 'invoices' 
    AND COLUMN_NAME = 'status'
    """
    
    cursor = connection.cursor()
    cursor.execute(check_query)
    status_exists = cursor.fetchone() is not None
    
    # Check if payment_status column exists
    check_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'billing_db' 
    AND TABLE_NAME = 'invoices' 
    AND COLUMN_NAME = 'payment_status'
    """
    
    cursor.execute(check_query)
    payment_status_exists = cursor.fetchone() is not None
    
    if status_exists and not payment_status_exists:
        # Rename status to payment_status
        query = "ALTER TABLE invoices CHANGE status payment_status VARCHAR(20)"
        execute_query(connection, query)
        print("Renamed 'status' column to 'payment_status' in invoices table")
    elif not status_exists and not payment_status_exists:
        # Add payment_status column
        query = "ALTER TABLE invoices ADD COLUMN payment_status VARCHAR(20) DEFAULT 'Pending'"
        execute_query(connection, query)
        print("Added 'payment_status' column to invoices table")
    else:
        print("The 'payment_status' column already exists in invoices table")
    
    cursor.close()

def fix_medical_db(connection):
    """Fix the structure of the medical_records table in medical_db"""
    # Check if doctor_id column exists
    check_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'medical_db' 
    AND TABLE_NAME = 'medical_records' 
    AND COLUMN_NAME = 'doctor_id'
    """
    
    cursor = connection.cursor()
    cursor.execute(check_query)
    doctor_id_exists = cursor.fetchone() is not None
    
    if not doctor_id_exists:
        # Add doctor_id column
        query = "ALTER TABLE medical_records ADD COLUMN doctor_id INT"
        execute_query(connection, query)
        print("Added 'doctor_id' column to medical_records table")
    else:
        print("The 'doctor_id' column already exists in medical_records table")
    
    cursor.close()

def main():
    """Main function to fix database structure"""
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
    
    # Fix billing_db
    print("\n=== Fixing billing_db structure ===")
    billing_conn = create_connection(
        servers['server2']['host'],
        servers['server2']['user'],
        servers['server2']['password'],
        'billing_db'
    )
    
    if billing_conn:
        fix_billing_db(billing_conn)
        billing_conn.close()
    
    # Fix medical_db
    print("\n=== Fixing medical_db structure ===")
    medical_conn = create_connection(
        servers['server1']['host'],
        servers['server1']['user'],
        servers['server1']['password'],
        'medical_db'
    )
    
    if medical_conn:
        fix_medical_db(medical_conn)
        medical_conn.close()
    
    print("\n=== Database structure fixes completed ===")

if __name__ == "__main__":
    main()
