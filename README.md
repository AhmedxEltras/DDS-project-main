# Hospital Management System

A comprehensive system for managing hospital operations including patients, doctors, appointments, medical records, and billing.

## Overview

The Hospital Management System is a desktop application built with Python and Tkinter that provides a user-friendly interface for hospital staff to manage various aspects of hospital operations. The system uses a distributed database architecture with MySQL to store and manage data across multiple databases.

## Features

- **Patient Management**: Add, update, and delete patient records
- **Doctor Management**: Manage doctor information and specializations
- **Appointment Scheduling**: Schedule and track patient appointments
- **Medical Records**: Maintain patient medical history and treatment records
- **Billing and Invoicing**: Generate and manage patient invoices
- **Auto-Refresh**: Real-time data updates with configurable refresh intervals
- **Cross-Database Queries**: Seamless data retrieval across multiple databases

## System Architecture

The system uses a distributed database architecture with two logical servers:

- **Server 1**:
  - `patients_db`: Stores patient information
  - `medical_db`: Stores medical records

- **Server 2**:
  - `appointments_db`: Stores doctor information and appointments
  - `billing_db`: Stores billing and invoice information

## Technical Stack

- **Programming Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Database**: MySQL
- **Database Connector**: mysql-connector-python

## Project Structure

```
hospital-management-system/
├── setup.py                 # Database setup script
├── requirements.txt         # Project dependencies
├── src/
│   ├── main.py              # Application entry point
│   ├── database_setup.py    # Database initialization module
│   ├── models/
│   │   └── database_utils.py # Database utility functions and classes
│   └── ui/
│       ├── styles.py        # UI styling configurations
│       └── tabs/
│           ├── patients_tab.py    # Patient management UI
│           ├── doctors_tab.py     # Doctor management UI
│           ├── appointments_tab.py # Appointment scheduling UI
│           └── billing_tab.py     # Billing and invoicing UI
└── docs/                    # Documentation files
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hospital-management-system.git
   cd hospital-management-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   python setup.py --debug
   ```

## Usage

1. Start the application:
   ```
   python src/main.py
   ```

2. Navigate through the tabs to manage different aspects of the hospital:
   - **Patients**: Manage patient information
   - **Doctors**: Manage doctor information
   - **Appointments**: Schedule and manage appointments
   - **Billing**: Generate and manage invoices

## Database Setup Options

The `setup.py` script provides several options for database initialization:

- `--no-tables`: Skip creating database tables
- `--no-sample-data`: Skip generating sample data
- `--debug`: Enable debug mode with verbose output

Example:
```
python setup.py --no-sample-data --debug
```

## Auto-Refresh Feature

The application includes an auto-refresh feature that automatically updates the data displayed in the UI at regular intervals. This feature can be enabled or disabled using the toggle button in the application.

## Development

### Adding New Features

1. Create new UI components in the `src/ui/tabs` directory
2. Update the database schema in `src/database_setup.py`
3. Add new functionality to the main application in `src/main.py`

### Database Configuration

Database connection settings can be modified in `src/models/database_utils.py`. The default settings are:

- **Host**: localhost
- **User**: root
- **Password**: root

For production environments, it is recommended to change these settings to more secure values.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Ahmed Eltras

## Acknowledgments

- Thanks to all contributors who have helped improve this system
- Special thanks to the open-source community for providing the tools and libraries used in this project
