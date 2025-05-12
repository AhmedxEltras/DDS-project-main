<div align="center">

# 🏥 Hospital Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/)

A modern, distributed healthcare management solution built with Python

[Key Features](#key-features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Video Tutorials](#video-tutorials)

<img src="docs/images/dashboard.png" alt="Dashboard" width="600"/>

</div>

## ✨ Key Features

🎨 **Modern UI**
- Professional theme with clean aesthetics
- Responsive design for all screen sizes
- Smooth animations and transitions
- Intuitive navigation system

🗄️ **Distributed Database**
- Four specialized databases distributed across two servers
- Server-based load balancing for improved performance
- Real-time synchronization across modules
- Automatic backup and recovery
- Data integrity validation

👥 **Patient Management**
- Comprehensive patient profiles
- Medical history tracking
- Document management
- Search and filter capabilities

👨‍⚕️ **Doctor Management**
- Staff scheduling and rotation
- Specialization tracking
- Performance analytics
- Availability management

📅 **Appointment System**
- Smart scheduling algorithm
- Automated reminders
- Conflict detection
- Calendar integration

💰 **Billing System**
- Automated invoice generation
- Multiple payment methods
- Insurance processing
- Financial reporting

### Core Modules

1. **Patient Management**
   - Patient registration and profile management
   - Medical history tracking
   - Contact information management
   - Search and filter capabilities

2. **Doctor Management**
   - Doctor profiles and specializations
   - Schedule management
   - Contact information
   - Qualification tracking

3. **Appointment System**
   - Schedule appointments
   - Status tracking (Scheduled/Completed/Cancelled)
   - Date and time management
   - Notes and special instructions

4. **Billing System**
   - Invoice generation
   - Payment tracking
   - Status monitoring (Paid/Pending/Overdue)
   - Financial reporting

## Technical Architecture

### Database Structure

The system uses a distributed database architecture with four specialized databases spread across two servers:

**Server 1:**

1. **patients_db**
   - Patient personal information
   - Medical history
   - Contact details

2. **medical_db**
   - Medical records
   - Diagnoses
   - Treatment plans

**Server 2:**

3. **appointments_db**
   - Doctor schedules
   - Appointment bookings
   - Status tracking

4. **billing_db**
   - Invoices
   - Payment records
   - Financial transactions

### Technology Stack

- **Frontend**: Python Tkinter with ttk widgets
- **Backend**: Python with MySQL
- **Database**: Distributed MySQL databases across two servers
- **UI Framework**: Custom responsive grid system

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- MySQL Server (two instances on separate servers)
- Git (optional)

### Installation

1️⃣ **Get the Code**
```bash
# Clone the repository
git clone https://github.com/yourusername/hospital-management-system.git

# Or download and extract the ZIP file
# https://github.com/yourusername/hospital-management-system/archive/main.zip

# Navigate to project directory
cd hospital-management-system
```

2️⃣ **Set Up Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Initialize System**
```bash
# Set up databases (make sure to configure server hostnames in database_setup.py)
python database_setup.py

# Start the application
python src/main.py
```

## Usage Guide

### Patient Registration

1. Navigate to the Patients tab
2. Click "Add" to create a new patient
3. Fill in required information:
   - Patient ID (auto-generated)
   - First Name
   - Last Name
   - Date of Birth
   - Gender
   - Contact Number
   - Address
4. Click "Save" to store the patient record

### Doctor Management

1. Access the Doctors tab
2. Click "Add" for new doctor entry
3. Provide required details:
   - Doctor ID (auto-generated)
   - First Name
   - Last Name
   - Specialization
   - Contact Number
4. Click "Save" to add the doctor

### Appointment Booking

1. Open the Appointments tab
2. Click "Add" for new appointment
3. Enter appointment details:
   - Patient ID
   - Doctor ID
   - Date
   - Time
   - Status
   - Notes (optional)
4. Click "Save" to schedule

### Billing Management

1. Select the Billing tab
2. Click "Add" for new invoice
3. Input billing information:
   - Invoice ID (auto-generated)
   - Patient ID
   - Amount
   - Date
   - Status
   - Description
4. Click "Save" to create invoice

## Development

## 📁 Project Structure

```
📦 hospital-management-system
┣ 📂 src                      # Source code
┃ ┣ 📂 models                 # Data models and business logic
┃ ┃ ┣ 📜 patient.py           # Patient management
┃ ┃ ┣ 📜 doctor.py            # Doctor management
┃ ┃ ┣ 📜 appointment.py       # Appointment handling
┃ ┃ ┗ 📜 billing.py           # Billing operations
┃ ┣ 📂 ui                     # User interface components
┃ ┃ ┣ 📂 tabs                 # Tab-specific UI modules
┃ ┃ ┣ 📜 styles.py            # UI styling and themes
┃ ┃ ┗ 📜 widgets.py           # Custom widgets
┃ ┣ 📂 utils                  # Utility functions
┃ ┃ ┣ 📜 validators.py        # Input validation
┃ ┃ ┗ 📜 helpers.py           # Helper functions
┃ ┗ 📜 main.py               # Application entry point
┣ 📂 database                 # Database files
┃ ┣ 📜 patients.db            # Patient records
┃ ┣ 📜 appointments.db        # Appointment data
┃ ┣ 📜 billing.db             # Financial records
┃ ┗ 📜 medical.db             # Medical history
┣ 📂 docs                     # Documentation
┃ ┣ 📂 images                 # Screenshots and images
┃ ┣ 📂 videos                 # Video tutorials
┃ ┗ 📜 API.md                 # API documentation
┣ 📂 tests                    # Test suite
┃ ┣ 📜 test_models.py         # Model tests
┃ ┗ 📜 test_utils.py          # Utility tests
┣ 📜 requirements.txt         # Dependencies
┣ 📜 database_setup.sql       # Database schema
┗ 📜 README.md               # Project documentation
```

## 💻 Development

### Code Style Guidelines

```python
# ✅ Good Example
def calculate_patient_age(birth_date: datetime) -> int:
    """Calculate patient's age from birth date.
    
    Args:
        birth_date: Patient's date of birth
        
    Returns:
        int: Patient's current age in years
    """
    today = datetime.now()
    age = today.year - birth_date.year
    return age - ((today.month, today.day) < (birth_date.month, birth_date.day))

# ❌ Bad Example
def calc_age(bd):
    # No type hints, poor naming, no docstring
    t = datetime.now()
    return t.year - bd.year - ((t.month, t.day) < (bd.month, bd.day))
```

### Best Practices

📝 **Documentation**
- Comprehensive docstrings for all functions and classes
- Clear inline comments for complex logic
- Up-to-date API documentation
- Detailed commit messages

🔍 **Code Quality**
- Type hints for better code clarity
- Unit tests for all components
- Regular code reviews
- Consistent code formatting

🛠️ **Tools**
- Black for code formatting
- Flake8 for linting
- PyTest for testing
- MyPy for type checking

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Requirements

- Python 3.8+
- SQLite 3
- Tkinter (usually comes with Python)
- Additional requirements in `requirements.txt`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue if needed

## Authors

- [Your Name]
- [Contributors]

## Acknowledgments

- Thanks to all contributors
- Inspired by modern healthcare systems
- Built with best practices in mind

## 🤝 Contributing

### Getting Started

1️⃣ **Fork the Repository**
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hospital-management-system.git

# Add upstream remote
git remote add upstream https://github.com/original/hospital-management-system.git
```

2️⃣ **Create a Branch**
```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

3️⃣ **Make Changes**
- Follow code style guidelines
- Add unit tests for new features
- Update documentation as needed

4️⃣ **Submit Changes**
```bash
# Stage changes
git add .

# Commit with meaningful message
git commit -m "feat: add new feature"

# Push to your fork
git push origin feature/your-feature-name
```

5️⃣ **Create Pull Request**
- Use the PR template
- Add detailed description
- Link related issues

## 🎥 Video Tutorials

Step-by-step video guides are available in [docs/videos](docs/videos):

### 1. System Setup (5:00)

🎬 **Installation Guide**
- System requirements
- Dependencies setup
- Database initialization
- First-time configuration

### 2. Patient Module (7:30)

🎬 **Patient Management**
- Registration workflow
- Profile management
- Medical history
- Search techniques

### 3. Doctor Module (6:45)

🎬 **Staff Management**
- Doctor onboarding
- Schedule configuration
- Patient assignment
- Performance tracking

### 4. Appointments (8:15)

🎬 **Scheduling System**
- Booking workflow
- Calendar management
- Notification system
- Conflict resolution

### 5. Billing (7:00)

🎬 **Financial Management**
- Invoice workflow
- Payment processing
- Insurance handling
- Report generation

## 📘 Documentation

📄 **User Guide**
- [Getting Started](docs/getting-started.md)
- [User Manual](docs/user-manual.md)
- [FAQ](docs/faq.md)

📄 **Developer Guide**
- [API Reference](docs/api.md)
- [Database Schema](docs/schema.md)
- [Contributing Guide](docs/contributing.md)

📄 **Additional Resources**
- [Architecture Overview](docs/architecture.md)
- [Security Guidelines](docs/security.md)
- [Deployment Guide](docs/deployment.md)

## 👨‍💻 Support

### Community
- [Discord Server](https://discord.gg/your-server)
- [Stack Overflow Tag](https://stackoverflow.com/questions/tagged/hms)
- [GitHub Discussions](https://github.com/your-repo/discussions)

### Help
1. 📖 Read the [documentation](docs/)
2. 🎥 Watch [video tutorials](docs/videos/)
3. 🔍 Search [existing issues](https://github.com/your-repo/issues)
4. 💬 Ask in [community forums](https://github.com/your-repo/discussions)

## 👨‍💻 Authors

**Lead Developer**
- 👨‍💻 [Your Name](https://github.com/yourusername)

**Core Team**
- 👩‍💻 [Team Member 1](https://github.com/team1)
- 👨‍💻 [Team Member 2](https://github.com/team2)

## 🌟 Acknowledgments

👏 **Special Thanks**
- All our amazing contributors
- The open-source community
- Healthcare professionals for feedback

📚 **Inspiration**
- Modern healthcare systems
- Open-source projects
- Industry best practices

## 📃 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by the Hospital Management System Team
</div>
