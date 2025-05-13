#!/usr/bin/env python
"""
Hospital Management System Setup Script
This script sets up the PostgreSQL databases using SQL scripts.
"""

import argparse
import os
import subprocess
import sys
import getpass

def run_sql_script(host, port, user, password, database, script_path):
    """Run a SQL script on a PostgreSQL database"""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    cmd = [
        'psql',
        '-h', host,
        '-p', str(port),
        '-U', user
    ]
    
    if database:
        cmd.extend(['-d', database])
    
    cmd.extend(['-f', script_path])
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error executing SQL script: {e.stderr}"

def setup_server(server_num, host, port, postgres_user, postgres_password, db_user, db_password, debug=False):
    """Set up databases and tables for a specific server"""
    sql_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql')
    server_dir = os.path.join(sql_dir, f'server{server_num}')
    
    if debug:
        print(f"\n=== Setting up Server {server_num} (port {port}) ===")
    
    # Create databases first
    script_path = os.path.join(server_dir, '01_create_databases.sql')
    success, output = run_sql_script(host, port, postgres_user, postgres_password, None, script_path)
    
    if debug:
        print(f"Creating databases on Server {server_num}...")
        if success:
            print("Databases created successfully.")
        else:
            print(output)
    
    # Get list of SQL files for table creation
    table_scripts = [f for f in os.listdir(server_dir) if f.startswith('0') and f != '01_create_databases.sql']
    table_scripts.sort()
    
    # For each database, run the appropriate table creation script
    for script in table_scripts:
        script_path = os.path.join(server_dir, script)
        
        # Extract database name from script name
        if server_num == 1:
            if 'appointments' in script:
                db_name = 'appointments_db'
            elif 'billing' in script:
                db_name = 'billing_db'
        elif server_num == 2:
            if 'patients' in script:
                db_name = 'patients_db'
            elif 'medical' in script:
                db_name = 'medical_db'
        elif server_num == 3:
            # For server 3, we need to run the backup script for each database
            backup_dbs = [
                'appointments_backup_db',
                'billing_backup_db',
                'medical_backup_db',
                'patients_backup_db'
            ]
            
            for db_name in backup_dbs:
                if debug:
                    print(f"Creating tables in {db_name}...")
                
                success, output = run_sql_script(host, port, db_user, db_password, db_name, script_path)
                
                if debug:
                    if success:
                        print(f"Tables in {db_name} created successfully.")
                    else:
                        print(output)
            
            # Skip the rest of the loop for server 3 as we've handled all databases
            continue
        
        if debug:
            print(f"Creating tables in {db_name}...")
        
        success, output = run_sql_script(host, port, db_user, db_password, db_name, script_path)
        
        if debug:
            if success:
                print(f"Tables in {db_name} created successfully.")
            else:
                print(output)

def main():
    """Main function to set up the Hospital Management System"""
    parser = argparse.ArgumentParser(description='Hospital Management System Setup')
    
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode with verbose output')
    
    args = parser.parse_args()
    
    # Configuration for the three PostgreSQL servers
    servers = [
        {
            'num': 1,
            'host': 'localhost',
            'port': 5433,
            'db_user': 'user1',
            'db_password': 'pass1'
        },
        {
            'num': 2,
            'host': 'localhost',
            'port': 5434,
            'db_user': 'user2',
            'db_password': 'pass2'
        },
        {
            'num': 3,
            'host': 'localhost',
            'port': 5435,
            'db_user': 'user3',
            'db_password': 'pass3'
        }
    ]
    
    print("=== Hospital Management System Database Setup ===")
    print("This script will set up all databases on all three PostgreSQL servers.")
    print("Make sure PostgreSQL is running on ports 5433, 5434, and 5435.")
    print()
    
    # Get PostgreSQL superuser credentials
    postgres_user = input("Enter PostgreSQL superuser username [postgres]: ") or "postgres"
    postgres_password = getpass.getpass("Enter PostgreSQL superuser password: ")
    
    # Set up each server
    for server in servers:
        setup_server(
            server['num'],
            server['host'],
            server['port'],
            postgres_user,
            postgres_password,
            server['db_user'],
            server['db_password'],
            args.debug
        )
    
    print("\n=== Database setup completed ===")
    print("All databases and tables have been created on all three servers.")
    print("\nTo run the application, use the following command:")
    print("python src/main.py")

if __name__ == "__main__":
    main()
