-- Server 3 Database Creation Script (port 5435) - Backup Server
-- Run as postgres user: psql -h localhost -p 5435 -U postgres -f 01_create_databases.sql

-- Create backup databases
CREATE DATABASE appointments_backup_db
    WITH 
    OWNER = user3
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

CREATE DATABASE billing_backup_db
    WITH 
    OWNER = user3
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

CREATE DATABASE medical_backup_db
    WITH 
    OWNER = user3
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

CREATE DATABASE patients_backup_db
    WITH 
    OWNER = user3
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE appointments_backup_db TO user3;
GRANT ALL PRIVILEGES ON DATABASE billing_backup_db TO user3;
GRANT ALL PRIVILEGES ON DATABASE medical_backup_db TO user3;
GRANT ALL PRIVILEGES ON DATABASE patients_backup_db TO user3;
