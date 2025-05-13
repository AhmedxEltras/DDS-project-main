"""
Database Utilities for Hospital Management System
Provides database setup, connection management, and sample data generation.
"""

import psycopg2
from psycopg2 import Error
import os
import random
from datetime import datetime, timedelta


class DatabaseBase:
    """
    Base class for database operations with common connection and query functionality.
    """
    def __init__(self, debug_mode=False):
        """Initialize the base database class"""
        self.debug_mode = debug_mode
        
        # PostgreSQL server configurations
        self.server_config = {
            'server1': {
                'host': 'localhost',
                'user': 'user1',
                'password': 'pass1',
                'port': 5433
            },
            'server2': {
                'host': 'localhost',
                'user': 'user2',
                'password': 'pass2',
                'port': 5434
            },
            'server3': {
                'host': 'localhost',
                'user': 'user3',
                'password': 'pass3',
                'port': 5435
            }
        }
    
    def create_connection(self, host, user, password, port, database=None):
        """Create a connection to the PostgreSQL server"""
        try:
            connection_config = {
                'host': host,
                'user': user,
                'password': password,
                'port': port
            }
            
            if database:
                connection_config['database'] = database
                
            connection = psycopg2.connect(**connection_config)
            
            if self.debug_mode:
                print(f"Connected to PostgreSQL Server: {host}:{port}" + 
                      (f", Database: {database}" if database else ""))
            return connection
        except Error as e:
            if self.debug_mode:
                print(f"Error connecting to PostgreSQL Server: {host}:{port}" + 
                      (f", Database: {database}" if database else "") + 
                      f", Error: {e}")
            return None
    
    def execute_query(self, connection, query, params=None):
        """Execute a query on the MySQL server"""
        cursor = connection.cursor()
        try:
            if params:
                # Convert 'None' strings to None type for SQL NULL
                if isinstance(params, list):
                    processed_params = [None if param == 'None' or param == '' else param for param in params]
                    cursor.execute(query, processed_params)
                else:
                    cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Handle different query types
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                connection.commit()
                last_id = cursor.lastrowid
                if self.debug_mode:
                    print(f"Query executed successfully. Last inserted ID: {last_id}")
                return last_id
            elif query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                if self.debug_mode:
                    print(f"Query returned {len(results)} rows")
                    if len(results) == 0:
                        print("WARNING: Query returned no results.")
                return results
            else:
                connection.commit()
                if self.debug_mode:
                    print("Query executed successfully")
                return True
        except Error as e:
            if self.debug_mode:
                print(f"Error executing query: {e}")
                print(f"Query: {query}")
                if params:
                    print(f"Parameters: {params}")
            return None
        finally:
            cursor.close()


class DatabaseManager(DatabaseBase):
    """
    Manages database connections and query execution across multiple databases
    distributed across two servers.
    """
    def __init__(self, debug_mode=False):
        """Initialize the database manager with server and database configurations"""
        super().__init__(debug_mode)
        
        # Database distribution across servers
        self.db_server_map = {
            'appointments_db': 'server1',  # Appointments DB on Server 1 (port 5433)
            'billing_db': 'server1',      # Billing DB on Server 1 (port 5433)
            'medical_db': 'server2',      # Medical DB on Server 2 (port 5434)
            'patients_db': 'server2',     # Patients DB on Server 2 (port 5434)
            # Server 3 will be used as backup
            'appointments_backup_db': 'server3',  # Backup for appointments
            'billing_backup_db': 'server3',      # Backup for billing
            'medical_backup_db': 'server3',      # Backup for medical records
            'patients_backup_db': 'server3'      # Backup for patients
        }
        
        # Database configurations
        self.config = {
            'appointments_db': {
                'database': 'appointments_db'
            },
            'billing_db': {
                'database': 'billing_db'
            },
            'medical_db': {
                'database': 'medical_db'
            },
            'patients_db': {
                'database': 'patients_db'
            },
            # Backup databases
            'appointments_backup_db': {
                'database': 'appointments_backup_db'
            },
            'billing_backup_db': {
                'database': 'billing_backup_db'
            },
            'medical_backup_db': {
                'database': 'medical_backup_db'
            },
            'patients_backup_db': {
                'database': 'patients_backup_db'
            }
        }
    
    def _get_connection(self, db_name):
        """Get a database connection for the specified database"""
        try:
            # Get the server assigned to this database
            server_name = self.db_server_map.get(db_name)
            if not server_name:
                if self.debug_mode:
                    print(f"Error: No server mapping found for {db_name}")
                return None
                
            # Get server configuration
            server_config = self.server_config.get(server_name)
            if not server_config:
                if self.debug_mode:
                    print(f"Error: Server configuration not found for {server_name}")
                return None
                
            # Get connection parameters
            host = server_config['host']
            user = server_config['user']
            password = server_config['password']
            port = server_config['port']
            
            # Create connection with database
            return self.create_connection(host, user, password, port, db_name)
        except Error as e:
            if self.debug_mode:
                print(f"Error connecting to {db_name}: {e}")
            return None

    def execute_query(self, db_name, query, params=None, sync_to_backup=True):
        """Execute a query on the specified database"""
        conn = self._get_connection(db_name)
        if not conn:
            if self.debug_mode:
                print(f"Failed to get connection for {db_name}. Cannot execute query.")
            return None
        
        try:
            if self.debug_mode:
                print(f"Executing query on {db_name}: {query[:100]}{'...' if len(query) > 100 else ''}")
                if params:
                    print(f"With parameters: {params}")
            
            result = super().execute_query(conn, query, params)
            
            # If this is a write operation and backup sync is enabled, replicate to backup
            if sync_to_backup and query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')) and not db_name.endswith('_backup_db'):
                self.sync_to_backup(db_name, query, params)
                
            return result
        finally:
            conn.close()
            
    def sync_to_backup(self, primary_db, query, params=None):
        """Synchronize a write operation to the backup database"""
        # Map primary database to its backup
        backup_map = {
            'appointments_db': 'appointments_backup_db',
            'billing_db': 'billing_backup_db',
            'medical_db': 'medical_backup_db',
            'patients_db': 'patients_backup_db'
        }
        
        backup_db = backup_map.get(primary_db)
        if not backup_db:
            if self.debug_mode:
                print(f"No backup database configured for {primary_db}")
            return
        
        # Execute the same query on the backup database
        try:
            if self.debug_mode:
                print(f"Synchronizing operation to backup database {backup_db}")
                
            self.execute_query(backup_db, query, params, sync_to_backup=False)  # Prevent infinite recursion
            
            if self.debug_mode:
                print(f"Successfully synchronized to {backup_db}")
        except Exception as e:
            if self.debug_mode:
                print(f"Error synchronizing to backup database {backup_db}: {e}")



class DatabaseSetup(DatabaseBase):
    """
    Handles database setup operations including creating databases,
    tables, and sample data.
    """
    def __init__(self, debug_mode=False):
        """Initialize the database setup with server configurations"""
        super().__init__(debug_mode)
        
        # Database distribution across servers
        self.servers = {
            'server1': {
                'host': self.server_config['server1']['host'],
                'user': self.server_config['server1']['user'],
                'password': self.server_config['server1']['password'],
                'port': self.server_config['server1']['port'],
                'databases': ['appointments_db', 'billing_db']
            },
            'server2': {
                'host': self.server_config['server2']['host'],
                'user': self.server_config['server2']['user'],
                'password': self.server_config['server2']['password'],
                'port': self.server_config['server2']['port'],
                'databases': ['medical_db', 'patients_db']
            },
            'server3': {
                'host': self.server_config['server3']['host'],
                'user': self.server_config['server3']['user'],
                'password': self.server_config['server3']['password'],
                'port': self.server_config['server3']['port'],
                'databases': ['appointments_backup_db', 'billing_backup_db', 'medical_backup_db', 'patients_backup_db']
            }
        }

    def setup_databases(self):
        """Create the databases on each server"""
        for server_name, server_info in self.servers.items():
            # Connect to the server without specifying a database
            # For PostgreSQL, connect to the 'postgres' default database
            try:
                conn = self.create_connection(
                    server_info['host'],
                    server_info['user'],
                    server_info['password'],
                    server_info['port'],
                    'postgres'  # Connect to default PostgreSQL database
                )
                
                if not conn:
                    if self.debug_mode:
                        print(f"Failed to connect to server {server_name}. Skipping database creation.")
                    continue
                    
                # Create each database assigned to this server
                for db_name in server_info['databases']:
                    try:
                        # In PostgreSQL, we need to commit after each transaction
                        conn.autocommit = True
                        cursor = conn.cursor()
                        
                        # Check if database exists in PostgreSQL
                        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                        result = cursor.fetchone()
                        
                        if not result:
                            # Create the database in PostgreSQL
                            cursor.execute(f"CREATE DATABASE {db_name}")
                            if self.debug_mode:
                                print(f"Created database {db_name} on server {server_name}")
                        else:
                            if self.debug_mode:
                                print(f"Database {db_name} already exists on server {server_name}")
                    except Error as e:
                        if self.debug_mode:
                            print(f"Error creating database {db_name} on server {server_name}: {e}")
                    finally:
                        cursor.close()
                
                conn.close()
            except Error as e:
                if self.debug_mode:
                    print(f"Error connecting to server {server_name}: {e}")

    def setup_backup_db(self, connection, source_db_name):
        """Set up a backup database with the same structure as the source database"""
        if source_db_name == 'patients_db':
            self.setup_patients_db(connection)
        elif source_db_name == 'medical_db':
            self.setup_medical_db(connection)
        elif source_db_name == 'appointments_db':
            self.setup_appointments_db(connection)
        elif source_db_name == 'billing_db':
            self.setup_billing_db(connection)
        else:
            if self.debug_mode:
                print(f"Unknown database type: {source_db_name}")
    
    def setup_database(self):
        """Set up all databases and tables"""
        # First create all database files
        self.setup_databases()
        
        # Set up Server 1 - Appointments and Billing
        if self.debug_mode:
            print("\n=== Setting up Server 1 (Appointments and Billing) ===")
        
        for db in self.servers['server1']['databases']:
            # Connect to the specific database
            db_conn = self.create_connection(
                self.servers['server1']['host'],
                self.servers['server1']['user'],
                self.servers['server1']['password'],
                self.servers['server1']['port'],
                db
            )
            
            if db_conn:
                # Set up database structure based on database name
                if self.debug_mode:
                    print(f"Setting up {db} structure")
                
                if db == 'appointments_db':
                    self.setup_appointments_db(db_conn)
                elif db == 'billing_db':
                    self.setup_billing_db(db_conn)
                
                db_conn.close()
        
        # Set up Server 2 - Medical and Patients
        if self.debug_mode:
            print("\n=== Setting up Server 2 (Medical and Patients) ===")
        
        for db in self.servers['server2']['databases']:
            # Connect to the specific database
            db_conn = self.create_connection(
                self.servers['server2']['host'],
                self.servers['server2']['user'],
                self.servers['server2']['password'],
                self.servers['server2']['port'],
                db
            )
            
            if db_conn:
                # Set up database structure based on database name
                if self.debug_mode:
                    print(f"Setting up {db} structure")
                
                if db == 'medical_db':
                    self.setup_medical_db(db_conn)
                elif db == 'patients_db':
                    self.setup_patients_db(db_conn)
                
                db_conn.close()
        
        # Set up Server 3 - Backup Server
        if self.debug_mode:
            print("\n=== Setting up Server 3 (Backup Server) ===")
        
        backup_mapping = {
            'appointments_backup_db': 'appointments_db',
            'billing_backup_db': 'billing_db',
            'medical_backup_db': 'medical_db',
            'patients_backup_db': 'patients_db'
        }
        
        for backup_db, source_db in backup_mapping.items():
            # Connect to the specific backup database
            db_conn = self.create_connection(
                self.servers['server3']['host'],
                self.servers['server3']['user'],
                self.servers['server3']['password'],
                self.servers['server3']['port'],
                backup_db
            )
            
            if db_conn:
                # Set up database structure based on source database
                if self.debug_mode:
                    print(f"Setting up {backup_db} structure (mirroring {source_db})")
                
                # Set up the backup database with the same structure as the source
                self.setup_backup_db(db_conn, source_db)
                
                db_conn.close()
        
        if self.debug_mode:
            print("\n=== Database setup completed ===")

    def setup_patients_db(self, connection):
        """Set up the patients database structure"""
        # Create patients table
        query = """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE NOT NULL,
            gender VARCHAR(10),
            address VARCHAR(255),
            phone VARCHAR(20),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, query)

    def setup_medical_db(self, connection):
        """Set up the medical database structure"""
        # Create medical_records table
        query = """
        CREATE TABLE IF NOT EXISTS medical_records (
            record_id SERIAL PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            diagnosis TEXT,
            treatment TEXT,
            notes TEXT,
            record_date DATE NOT NULL,
            doctor_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, query)

    def setup_appointments_db(self, connection):
        """Set up the appointments database structure"""
        # Create doctors table
        doctors_query = """
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            specialization VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        if not self.execute_query(connection, doctors_query):
            return False
        
        # Create appointments table
        appointments_query = """
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id SERIAL PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            status VARCHAR(20) DEFAULT 'Scheduled',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, appointments_query)

    def setup_billing_db(self, connection):
        """Set up the billing database structure"""
        # Create invoices table
        query = """
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id SERIAL PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            appointment_id INTEGER,
            amount DECIMAL(10, 2) NOT NULL,
            payment_status VARCHAR(20) DEFAULT 'Pending',
            issue_date DATE NOT NULL,
            due_date DATE NOT NULL,
            payment_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        return self.execute_query(connection, query)

    def generate_sample_data(self):
        """Generate sample data for all databases"""
        # Create database manager for executing queries
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

    def insert_sample_patients(self, db_manager):
        """Insert sample patients into the patients database"""
        if self.debug_mode:
            print("\n=== Inserting sample patients ===")
        
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
            appointment_id = db_manager.execute_query('appointments_db', query, appointment)
            if appointment_id:
                appointment_ids.append(appointment_id)
                if self.debug_mode:
                    print(f"Added appointment: Patient {appointment[0]}, Doctor {appointment[1]}, Date: {appointment[2]}, ID: {appointment_id}")
        
        return appointment_ids

    def insert_sample_invoices(self, db_manager, patient_ids, appointment_ids):
        """Insert sample invoices into the billing database"""
        if self.debug_mode:
            print("\n=== Inserting sample invoices ===")
        
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
            invoice_id = db_manager.execute_query('billing_db', query, invoice)
            if invoice_id and self.debug_mode:
                print(f"Added invoice: ID: {invoice_id}, Amount: ${invoice[2]}, Status: {invoice[3]}")

    def insert_sample_medical_records(self, db_manager, patient_ids, doctor_ids):
        """Insert sample medical records into the medical database"""
        if self.debug_mode:
            print("\n=== Inserting sample medical records ===")
        
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
            record_id = db_manager.execute_query('medical_db', query, record)
            if record_id and self.debug_mode:
                print(f"Added medical record: Patient {record[0]}, Diagnosis: {record[1]}, ID: {record_id}")


# Utility function to initialize the database
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
