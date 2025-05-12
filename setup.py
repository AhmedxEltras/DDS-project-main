#!/usr/bin/env python
"""
Hospital Management System Setup Script
This script initializes the database and generates sample data.
"""

import argparse
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database_setup import initialize_database

def main():
    """Main function to set up the Hospital Management System"""
    parser = argparse.ArgumentParser(description='Hospital Management System Setup')
    
    parser.add_argument('--no-tables', action='store_true',
                        help='Skip creating database tables')
    
    parser.add_argument('--no-sample-data', action='store_true',
                        help='Skip generating sample data')
    
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode with verbose output')
    
    args = parser.parse_args()
    
    # Initialize the database
    initialize_database(
        setup_tables=not args.no_tables,
        add_sample_data=not args.no_sample_data,
        debug_mode=args.debug
    )
    
    print("\nSetup completed successfully!")
    print("\nTo run the application, use the following command:")
    print("python src/main.py")

if __name__ == "__main__":
    main()
