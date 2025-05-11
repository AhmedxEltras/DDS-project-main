-- Create Patients Database
CREATE DATABASE IF NOT EXISTS patients_db;
USE patients_db;

-- Drop tables if they exist
DROP TABLE IF EXISTS patients;

CREATE TABLE IF NOT EXISTS patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('M', 'F', 'Other'),
    contact_number VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Appointments Database
CREATE DATABASE IF NOT EXISTS appointments_db;
USE appointments_db;

-- Drop tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS doctors;

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100),
    contact_number VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients_db.patients(patient_id) ON DELETE CASCADE
);

-- Create Billing Database
CREATE DATABASE IF NOT EXISTS billing_db;
USE billing_db;

-- Drop tables if they exist
DROP TABLE IF EXISTS invoices;

CREATE TABLE IF NOT EXISTS invoices (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    appointment_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('Pending', 'Paid', 'Cancelled') DEFAULT 'Pending',
    payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients_db.patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments_db.appointments(appointment_id) ON DELETE CASCADE
);

-- Create Medical Database
CREATE DATABASE IF NOT EXISTS medical_db;
USE medical_db;

-- Drop tables if they exist
DROP TABLE IF EXISTS medical_records;

CREATE TABLE IF NOT EXISTS medical_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    diagnosis TEXT,
    prescription TEXT,
    notes TEXT,
    visit_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients_db.patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- Add some sample data for testing
USE patients_db;
INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_number, email)
VALUES 
('John', 'Doe', '1990-01-15', 'M', '123-456-7890', 'john.doe@email.com'),
('Jane', 'Smith', '1985-03-20', 'F', '234-567-8901', 'jane.smith@email.com');

USE appointments_db;
INSERT INTO doctors (first_name, last_name, specialization, contact_number)
VALUES 
('David', 'Wilson', 'Cardiology', '345-678-9012'),
('Sarah', 'Johnson', 'Pediatrics', '456-789-0123');

INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status)
VALUES 
(1, 1, CURDATE(), '10:00:00', 'Scheduled'),
(2, 2, CURDATE(), '14:30:00', 'Scheduled');

USE billing_db;
INSERT INTO invoices (patient_id, appointment_id, amount, payment_status, payment_date)
VALUES 
(1, 1, 150.00, 'Pending', NULL),
(2, 2, 200.00, 'Pending', NULL);

USE medical_db;
INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription, visit_date)
VALUES 
(1, 1, 'Regular checkup', 'Vitamins', CURDATE()),
(2, 2, 'Fever', 'Paracetamol', CURDATE());

USE billing_db;