-- Server 2 - Medical Database Tables (port 5434)
-- Run as user2: psql -h localhost -p 5434 -U user2 -d medical_db -f 03_medical_db_tables.sql

-- Create medical_records table
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
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_medical_records_patient ON medical_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_medical_records_doctor ON medical_records(doctor_id);
CREATE INDEX IF NOT EXISTS idx_medical_records_date ON medical_records(record_date);

-- Sample data insertion (to be run after patients and doctors are created)
-- This is commented out because it depends on patient_ids and doctor_ids
/*
INSERT INTO medical_records (patient_id, diagnosis, treatment, notes, record_date, doctor_id)
VALUES
    (1, 'Hypertension', 'Prescribed Lisinopril 10mg', 'Blood pressure 140/90', '2023-01-15', 1),
    (2, 'Migraine', 'Prescribed Sumatriptan', 'Recurring headaches with aura', '2023-02-10', 2),
    (3, 'Sprained ankle', 'RICE protocol, ankle brace', 'Grade 2 sprain, follow-up in 2 weeks', '2023-03-05', 3),
    (4, 'Allergic rhinitis', 'Prescribed Cetirizine', 'Seasonal allergies, worse in spring', '2023-04-20', 4),
    (5, 'Eczema', 'Topical corticosteroid cream', 'Flare-up on arms and neck', '2023-05-12', 5);
*/
