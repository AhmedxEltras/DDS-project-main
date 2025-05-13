-- Server 2 - Patients Database Tables (port 5434)
-- Run as user2: psql -h localhost -p 5434 -U user2 -d patients_db -f 02_patients_db_tables.sql

-- Create patients table
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
);

-- Sample data insertion
INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone, email)
VALUES 
    ('John', 'Doe', '1980-05-15', 'Male', '123 Main St', '555-1234', 'john.doe@email.com'),
    ('Jane', 'Smith', '1975-08-22', 'Female', '456 Oak Ave', '555-5678', 'jane.smith@email.com'),
    ('Michael', 'Johnson', '1990-03-10', 'Male', '789 Pine Rd', '555-9012', 'michael.j@email.com'),
    ('Emily', 'Williams', '1985-11-30', 'Female', '321 Cedar Ln', '555-3456', 'emily.w@email.com'),
    ('David', 'Brown', '1972-07-18', 'Male', '654 Birch Blvd', '555-7890', 'david.b@email.com');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_patients_dob ON patients(date_of_birth);
