-- Server 1 Database Creation Script (port 5433)
-- Run as postgres user: psql -h localhost -p 5433 -U postgres -f 01_create_databases.sql

-- Create appointments database
CREATE DATABASE appointments_db
    WITH 
    OWNER = user1
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Create billing database
CREATE DATABASE billing_db
    WITH 
    OWNER = user1
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE appointments_db TO user1;
GRANT ALL PRIVILEGES ON DATABASE billing_db TO user1;
