-- Server 1 - Billing Database Tables (port 5433)
-- Run as user1: psql -h localhost -p 5433 -U user1 -d billing_db -f 03_billing_db_tables.sql

-- Create invoices table
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
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_invoices_patient ON invoices(patient_id);
CREATE INDEX IF NOT EXISTS idx_invoices_appointment ON invoices(appointment_id);
CREATE INDEX IF NOT EXISTS idx_invoices_payment_status ON invoices(payment_status);
CREATE INDEX IF NOT EXISTS idx_invoices_due_date ON invoices(due_date);

-- Sample data insertion (commented out because it depends on patient_ids and appointment_ids)
/*
INSERT INTO invoices (patient_id, appointment_id, amount, payment_status, issue_date, due_date, payment_date)
VALUES
    (1, 1, 150.00, 'Paid', '2023-06-15', '2023-07-15', '2023-06-20'),
    (2, 2, 200.00, 'Pending', '2023-06-16', '2023-07-16', NULL),
    (3, 3, 175.00, 'Paid', '2023-06-17', '2023-07-17', '2023-06-18'),
    (4, 4, 100.00, 'Pending', '2023-06-18', '2023-07-18', NULL),
    (5, 5, 225.00, 'Paid', '2023-06-19', '2023-07-19', '2023-06-25');
*/
