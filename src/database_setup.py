#!/usr/bin/env python
"""
Hospital Management System Database Setup
This module provides functions for setting up and initializing the database.
"""

import argparse
from src.models.database_utils import DatabaseSetup, initialize_database


def main():
    """Main function to set up the Hospital Management System database"""
    parser = argparse.ArgumentParser(description='Hospital Management System Database Setup')
    
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
    
    if args.debug:
        print("\nSetup completed successfully!")
        print("\nTo run the application, use the following command:")
        print("python src/main.py")


if __name__ == "__main__":
    main()
