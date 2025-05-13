-- Server 2 Database Creation Script (port 5434)
-- Run as postgres user: psql -h localhost -p 5434 -U postgres -f 01_create_databases.sql

-- Create medical database
CREATE DATABASE medical_db
    WITH 
    OWNER = user2
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Create patients database
CREATE DATABASE patients_db
    WITH 
    OWNER = user2
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE medical_db TO user2;
GRANT ALL PRIVILEGES ON DATABASE patients_db TO user2;
