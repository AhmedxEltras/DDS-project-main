-- Server 1 - Appointments Database Tables (port 5433)
-- Run as user1: psql -h localhost -p 5433 -U user1 -d appointments_db -f 02_appointments_db_tables.sql

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create appointments table
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
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_doctors_name ON doctors(last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors(specialization);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);

-- Sample data insertion for doctors
INSERT INTO doctors (first_name, last_name, specialization, phone, email)
VALUES
    ('Robert', 'Miller', 'Cardiology', '555-2468', 'robert.m@hospital.com'),
    ('Sarah', 'Taylor', 'Neurology', '555-1357', 'sarah.t@hospital.com'),
    ('James', 'Anderson', 'Orthopedics', '555-3690', 'james.a@hospital.com'),
    ('Jennifer', 'Thomas', 'Pediatrics', '555-8024', 'jennifer.t@hospital.com'),
    ('William', 'Jackson', 'Dermatology', '555-7913', 'william.j@hospital.com');

-- Sample data insertion for appointments (commented out because it depends on patient_ids)
/*
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
VALUES
    (1, 1, '2023-06-15', '09:00:00', 'Scheduled', 'Annual checkup'),
    (2, 2, '2023-06-16', '10:30:00', 'Scheduled', 'Follow-up appointment'),
    (3, 3, '2023-06-17', '14:00:00', 'Scheduled', 'Initial consultation'),
    (4, 4, '2023-06-18', '11:15:00', 'Scheduled', 'Vaccination'),
    (5, 5, '2023-06-19', '15:45:00', 'Scheduled', 'Skin examination');
*/
