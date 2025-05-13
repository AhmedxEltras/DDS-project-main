#!/bin/bash
# Master script to set up all databases for the Hospital Management System

echo "=== Hospital Management System Database Setup ==="
echo "This script will set up all databases on all three PostgreSQL servers."
echo "Make sure PostgreSQL is running on ports 5433, 5434, and 5435."
echo

# Set PostgreSQL superuser credentials
POSTGRES_USER="postgres"
read -sp "Enter PostgreSQL superuser password: " POSTGRES_PASSWORD
echo

# Server 1 setup (port 5433)
echo
echo "=== Setting up Server 1 (port 5433) ==="
echo "Creating databases on Server 1..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h localhost -p 5433 -U $POSTGRES_USER -f server1/01_create_databases.sql

echo "Creating tables in appointments_db..."
PGPASSWORD=pass1 psql -h localhost -p 5433 -U user1 -d appointments_db -f server1/02_appointments_db_tables.sql

echo "Creating tables in billing_db..."
PGPASSWORD=pass1 psql -h localhost -p 5433 -U user1 -d billing_db -f server1/03_billing_db_tables.sql

# Server 2 setup (port 5434)
echo
echo "=== Setting up Server 2 (port 5434) ==="
echo "Creating databases on Server 2..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h localhost -p 5434 -U $POSTGRES_USER -f server2/01_create_databases.sql

echo "Creating tables in patients_db..."
PGPASSWORD=pass2 psql -h localhost -p 5434 -U user2 -d patients_db -f server2/02_patients_db_tables.sql

echo "Creating tables in medical_db..."
PGPASSWORD=pass2 psql -h localhost -p 5434 -U user2 -d medical_db -f server2/03_medical_db_tables.sql

# Server 3 setup (port 5435)
echo
echo "=== Setting up Server 3 (port 5435) - Backup Server ==="
echo "Creating databases on Server 3..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h localhost -p 5435 -U $POSTGRES_USER -f server3/01_create_databases.sql

echo "Creating tables in backup databases..."
PGPASSWORD=pass3 psql -h localhost -p 5435 -U user3 -d appointments_backup_db -f server3/02_backup_tables.sql
PGPASSWORD=pass3 psql -h localhost -p 5435 -U user3 -d billing_backup_db -f server3/02_backup_tables.sql
PGPASSWORD=pass3 psql -h localhost -p 5435 -U user3 -d medical_backup_db -f server3/02_backup_tables.sql
PGPASSWORD=pass3 psql -h localhost -p 5435 -U user3 -d patients_backup_db -f server3/02_backup_tables.sql

echo
echo "=== Database setup completed ==="
echo "All databases and tables have been created on all three servers."
echo "You can now run the Hospital Management System application."
