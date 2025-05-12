"""
Database Utilities for Hospital Management System
Provides database setup, connection management, and sample data generation.
"""

from mysql.connector import connect, Error
import random
from datetime import datetime, timedelta

# This is the main DatabaseManager class that will be imported by the application
class DatabaseManager:
    """
    Manages database connections and query execution across multiple databases
    distributed across two servers.
    """
    def __init__(self, debug_mode=False):
        """Initialize the database manager with server and database configurations"""
        self.debug_mode = debug_mode
        
        # Define the two servers
        self.servers = {
            'server1': {
                'host': 'localhost',  # Using localhost for testing
                'user': 'root',
                'password': 'root'
            },
            'server2': {
                'host': 'localhost',  # Using localhost for testing
                'user': 'root',
                'password': 'root'
            }
        }
        
        # Database distribution across servers
        self.db_server_map = {
            'patients_db': 'server1',     # Patients DB on Server 1
            'medical_db': 'server1',      # Medical DB on Server 1
            'appointments_db': 'server2', # Appointments DB on Server 2
            'billing_db': 'server2'       # Billing DB on Server 2
        }
        
        # Database configurations
        self.config = {
            'patients_db': {
                'database': 'patients_db'
            },
            'appointments_db': {
                'database': 'appointments_db'
            },
            'billing_db': {
                'database': 'billing_db'
            },
            'medical_db': {
                'database': 'medical_db'
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
            server_config = self.servers.get(server_name)
            if not server_config:
                if self.debug_mode:
                    print(f"Error: Server configuration not found for {server_name}")
                return None
                
            # Combine server config with database config
            connection_config = {**server_config, **self.config[db_name]}
            
            # Connect to the database on the assigned server
            if self.debug_mode:
                print(f"Connecting to {db_name} on {server_name}")
                
            return connect(**connection_config)
        except Error as e:
            if self.debug_mode:
                print(f"Error connecting to {db_name} on {server_name}: {e}")
            return None

    def execute_query(self, db_name, query, params=None):
        """Execute a query on the specified database"""
        conn = self._get_connection(db_name)
        if not conn:
            if self.debug_mode:
                print(f"Failed to get connection for {db_name}. Cannot execute query.")
            return None
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            if self.debug_mode:
                print(f"Executing query on {db_name}: {query[:100]}{'...' if len(query) > 100 else ''}")
                if params:
                    print(f"With parameters: {params}")
            
            if params:
                # Convert 'None' strings to None type for SQL NULL
                processed_params = [None if param == 'None' or param == '' else param for param in params]
                cursor.execute(query, processed_params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
                last_id = cursor.lastrowid
                if self.debug_mode:
                    print(f"Query executed successfully. Last inserted ID: {last_id}")
                return last_id
            else:
                results = cursor.fetchall()
                if self.debug_mode:
                    print(f"Query returned {len(results)} rows")
                    if len(results) == 0:
                        print("WARNING: Query returned no results.")
                return results
        except Error as e:
            if self.debug_mode:
                server_name = self.db_server_map.get(db_name, 'unknown')
                print(f"Error executing query on {db_name} (server: {server_name}): {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


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
            if database:
                connection = connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
            else:
                connection = connect(
                    host=host,
                    user=user,
                    password=password
                )
            if self.debug_mode:
                print(f"Connected to MySQL Server: {host}" + 
                      (f", Database: {database}" if database else ""))
            return connection
        except Error as e:
            if self.debug_mode:
                print(f"Error connecting to MySQL Server: {host}" + 
                      (f", Database: {database}" if database else "") + 
                      f", Error: {e}")
            return None

    def execute_query(self, connection, query, params=None):
        """Execute a query on the MySQL server"""
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            if self.debug_mode:
                print("Query executed successfully")
            return cursor.lastrowid if cursor.lastrowid else True
        except Error as e:
            if self.debug_mode:
                print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()

    def setup_database(self):
        """Set up all databases and tables"""
        # Set up Server 1
        if self.debug_mode:
            print("\n=== Setting up Server 1 ===")
        
        server1_conn = self.create_connection(
            self.servers['server1']['host'], 
            self.servers['server1']['user'], 
            self.servers['server1']['password']
        )
        
        if server1_conn:
            # Create databases on Server 1
            for db in self.servers['server1']['databases']:
                if self.debug_mode:
                    print(f"\nCreating database: {db}")
                
                self.execute_query(server1_conn, f"CREATE DATABASE IF NOT EXISTS {db}")
                
                # Connect to the specific database
                db_conn = self.create_connection(
                    self.servers['server1']['host'],
                    self.servers['server1']['user'],
                    self.servers['server1']['password'],
                    db
                )
                
                if db_conn:
                    # Set up database structure based on database name
                    if self.debug_mode:
                        print(f"Setting up {db} structure")
                    
                    if db == 'patients_db':
                        self.setup_patients_db(db_conn)
                    elif db == 'medical_db':
                        self.setup_medical_db(db_conn)
                    
                    db_conn.close()
            
            server1_conn.close()
        
        # Set up Server 2
        if self.debug_mode:
            print("\n=== Setting up Server 2 ===")
        
        server2_conn = self.create_connection(
            self.servers['server2']['host'], 
            self.servers['server2']['user'], 
            self.servers['server2']['password']
        )
        
        if server2_conn:
            # Create databases on Server 2
            for db in self.servers['server2']['databases']:
                if self.debug_mode:
                    print(f"\nCreating database: {db}")
                
                self.execute_query(server2_conn, f"CREATE DATABASE IF NOT EXISTS {db}")
                
                # Connect to the specific database
                db_conn = self.create_connection(
                    self.servers['server2']['host'],
                    self.servers['server2']['user'],
                    self.servers['server2']['password'],
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
            
            server2_conn.close()
        
        if self.debug_mode:
            print("\n=== Database setup completed ===")

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
                print(f"Added invoice: Patient {invoice[0]}, Amount: ${invoice[2]}, ID: {invoice_id}")

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
