import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager
from datetime import datetime

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.db_manager = DatabaseManager()
        
        # Configure window properties
        self.root.minsize(1200, 800)
        self.root.configure(bg='#f5f6fa')
        
        # Set modern theme and styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern colors and styles
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       rowheight=30,
                       fieldbackground="#ffffff",
                       font=('Segoe UI', 10))
        
        style.configure("Treeview.Heading",
                       background="#3498db",
                       foreground="white",
                       relief="flat",
                       font=('Segoe UI', 10, 'bold'))
        
        style.map("Treeview.Heading",
                  background=[('active', '#2980b9')])
        
        # Configure modern button style
        style.configure("TButton",
                       padding=10,
                       relief="flat",
                       background="#3498db",
                       foreground="white",
                       font=('Segoe UI', 10))
        
        style.map("TButton",
                  background=[('active', '#2980b9')],
                  foreground=[('active', 'white')])
        
        # Configure modern entry and combobox style
        style.configure("TEntry",
                       padding=8,
                       relief="flat",
                       font=('Segoe UI', 10))
        
        style.configure("TCombobox",
                       padding=8,
                       relief="flat",
                       font=('Segoe UI', 10))
        
        # Configure modern label frame style
        style.configure("TLabelframe",
                       background="#ffffff",
                       padding=20)
        
        style.configure("TLabelframe.Label",
                       background="#ffffff",
                       foreground="#2c3e50",
                       font=('Segoe UI', 11, 'bold'))
        
        # Configure modern label style
        style.configure("TLabel",
                       background="#ffffff",
                       foreground="#2c3e50",
                       font=('Segoe UI', 10))
        
        # Configure notebook style
        style.configure("TNotebook",
                       background="#f5f6fa",
                       padding=15)
        
        style.configure("TNotebook.Tab",
                       background="#ffffff",
                       padding=[20, 10],
                       font=('Segoe UI', 10))
        
        style.map("TNotebook.Tab",
                  background=[("selected", "#3498db")],
                  foreground=[("selected", "#ffffff")])
        
        # Configure frame style
        style.configure("TFrame",
                       background="#ffffff")
        
        # Add alternating row colors for treeviews
        style.map("Treeview",
                  background=[("selected", "#3498db")],
                  foreground=[("selected", "#ffffff")])
        
        # Create and configure notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=20, padx=20, expand=True, fill='both')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        # Create tabs
        self.patients_tab = ttk.Frame(self.notebook)
        self.appointments_tab = ttk.Frame(self.notebook)
        self.billing_tab = ttk.Frame(self.notebook)
        self.doctors_tab = ttk.Frame(self.notebook)  # New doctors tab
        
        self.notebook.add(self.patients_tab, text="Patients")
        self.notebook.add(self.doctors_tab, text="Doctors")  # Add doctors tab
        self.notebook.add(self.appointments_tab, text="Appointments")
        self.notebook.add(self.billing_tab, text="Billing")
        
        self.setup_patients_tab()
        self.setup_doctors_tab()  # Setup doctors tab
        self.setup_appointments_tab()
        self.setup_billing_tab()
    
        # Add initial refresh and auto-refresh setup
        self.refresh_patient_combobox()
        self.refresh_doctor_combobox()
        self.refresh_billing_patient_combobox()
        self.refresh_patient_list()
        self.setup_patient_auto_refresh()

    def setup_patients_tab(self):
        # Patient Information Form
        form_frame = ttk.LabelFrame(self.patients_tab, text="Patient Information", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Add patient ID field for updates
        ttk.Label(form_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_id = ttk.Entry(form_frame)
        self.patient_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="First Name:").grid(row=1, column=0, padx=5, pady=5)
        self.first_name = ttk.Entry(form_frame)
        self.first_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=2, column=0, padx=5, pady=5)
        self.last_name = ttk.Entry(form_frame)
        self.last_name.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Date of Birth:").grid(row=3, column=0, padx=5, pady=5)
        self.dob = ttk.Entry(form_frame)
        self.dob.grid(row=3, column=1, padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Patient", command=self.add_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Patient", command=self.update_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Patient", command=self.delete_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_patient_form).pack(side=tk.LEFT, padx=5)

        # Patient List with scrollbar
        list_frame = ttk.LabelFrame(self.patients_tab, text="Patient List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.patient_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "DOB"), show="headings", 
                                       yscrollcommand=scrollbar.set)
        self.patient_tree.heading("ID", text="ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("DOB", text="Date of Birth")
        
        # Set column widths
        self.patient_tree.column("ID", width=50)
        self.patient_tree.column("Name", width=200)
        self.patient_tree.column("DOB", width=100)
        self.patient_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar command - only need this once
        scrollbar.config(command=self.patient_tree.yview)

        # Bind treeview selection event
        self.patient_tree.bind('<<TreeviewSelect>>', self.on_patient_select)

    def clear_patient_form(self):
        self.patient_id.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.dob.delete(0, tk.END)

    def on_patient_select(self, event):
        selected_items = self.patient_tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.patient_tree.item(item)['values']
            if values:
                self.patient_id.delete(0, tk.END)
                self.patient_id.insert(0, values[0])
                
                # Split the name into first and last name
                full_name = values[1].split()
                self.first_name.delete(0, tk.END)
                self.last_name.delete(0, tk.END)
                if len(full_name) > 0:
                    self.first_name.insert(0, full_name[0])
                if len(full_name) > 1:
                    self.last_name.insert(0, ' '.join(full_name[1:]))
                
                self.dob.delete(0, tk.END)
                self.dob.insert(0, values[2])

    def update_patient(self):
        if not self.patient_id.get():
            messagebox.showerror("Error", "Please select a patient to update")
            return

        query = """UPDATE patients 
                  SET first_name = %s, last_name = %s, date_of_birth = %s 
                  WHERE patient_id = %s"""
        params = (self.first_name.get(), self.last_name.get(), 
                 self.dob.get(), self.patient_id.get())
        
        if self.db_manager.execute_query('patients_db', query, params):
            messagebox.showinfo("Success", "Patient updated successfully!")
            self.refresh_patient_list()
            self.clear_patient_form()

    def delete_patient(self):
        if not self.patient_id.get():
            messagebox.showerror("Error", "Please select a patient to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient?"):
            patient_id = self.patient_id.get()
            
            # First delete related records from other tables
            delete_appointments = "DELETE FROM appointments_db.appointments WHERE patient_id = %s"
            delete_invoices = "DELETE FROM billing_db.invoices WHERE patient_id = %s"
            delete_medical_records = "DELETE FROM medical_db.medical_records WHERE patient_id = %s"
            
            # Delete related records first
            self.db_manager.execute_query('appointments_db', delete_appointments, (patient_id,))
            self.db_manager.execute_query('billing_db', delete_invoices, (patient_id,))
            self.db_manager.execute_query('medical_db', delete_medical_records, (patient_id,))
            
            # Then delete the patient
            delete_patient = "DELETE FROM patients WHERE patient_id = %s"
            if self.db_manager.execute_query('patients_db', delete_patient, (patient_id,)):
                messagebox.showinfo("Success", "Patient deleted successfully!")
                self.refresh_patient_list()
                self.clear_patient_form()
            else:
                messagebox.showerror("Error", "Failed to delete patient")

    def setup_appointments_tab(self):
        # Appointment Form
        form_frame = ttk.LabelFrame(self.appointments_tab, text="New Appointment", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(form_frame, text="Patient:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_combobox = ttk.Combobox(form_frame, state="readonly")
        self.patient_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.refresh_patient_combobox()

        ttk.Label(form_frame, text="Doctor:").grid(row=1, column=0, padx=5, pady=5)
        self.doctor_combobox = ttk.Combobox(form_frame, state="readonly")
        self.doctor_combobox.grid(row=1, column=1, padx=5, pady=5)
        # Initialize auto-refresh for doctor combobox
        self.setup_doctor_auto_refresh()

        ttk.Label(form_frame, text="Date:").grid(row=2, column=0, padx=5, pady=5)
        self.appointment_date = ttk.Entry(form_frame)
        self.appointment_date.grid(row=2, column=1, padx=5, pady=5)

        # Add the appointment button and refresh button
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        add_appointment_btn = ttk.Button(button_frame, text="Add Appointment", command=self.add_appointment)
        add_appointment_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.refresh_appointment_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Appointments List with scrollbar
        list_frame = ttk.LabelFrame(self.appointments_tab, text="Appointments List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.appointment_tree = ttk.Treeview(list_frame,
                                           columns=("ID", "Patient", "Doctor", "Date", "Status"),
                                           show="headings",
                                           yscrollcommand=scrollbar.set)
        self.appointment_tree.heading("ID", text="ID")
        self.appointment_tree.heading("Patient", text="Patient")
        self.appointment_tree.heading("Doctor", text="Doctor")
        self.appointment_tree.heading("Date", text="Date")
        self.appointment_tree.heading("Status", text="Status")
        
        # Set column widths
        self.appointment_tree.column("ID", width=50)
        self.appointment_tree.column("Patient", width=150)
        self.appointment_tree.column("Doctor", width=150)
        self.appointment_tree.column("Date", width=120)
        self.appointment_tree.column("Status", width=80)
        
        self.appointment_tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.appointment_tree.yview)
        
        # Initial load of appointments
        self.refresh_appointment_list()

    def add_appointment(self):
        selected_patient = self.patient_combobox.get()
        selected_doctor = self.doctor_combobox.get()
        appointment_date = self.appointment_date.get()
        
        if not selected_patient or not selected_doctor or not appointment_date:
            messagebox.showerror("Error", "Please fill in all fields")
            return
                
        patient_id = self.patient_dict[selected_patient]
        doctor_id = self.doctor_dict[selected_doctor]
        
        query = """INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) 
                  VALUES (%s, %s, %s, 'Scheduled')"""
        params = (patient_id, doctor_id, appointment_date)
        
        if self.db_manager.execute_query('appointments_db', query, params):
            messagebox.showinfo("Success", "Appointment scheduled successfully!")
            self.refresh_appointment_list()
            # Clear form
            self.patient_combobox.set('')
            self.doctor_combobox.set('')
            self.appointment_date.delete(0, tk.END)

        # Appointments List with scrollbar
        list_frame = ttk.LabelFrame(self.appointments_tab, text="Appointments List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.appointment_tree = ttk.Treeview(list_frame,
                                           columns=("ID", "Patient", "Doctor", "Date", "Status"),
                                           show="headings",
                                           yscrollcommand=scrollbar.set)
        self.appointment_tree.heading("ID", text="ID")
        self.appointment_tree.heading("Patient", text="Patient")
        self.appointment_tree.heading("Doctor", text="Doctor")
        self.appointment_tree.heading("Date", text="Date")
        self.appointment_tree.heading("Status", text="Status")
        self.appointment_tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.appointment_tree.yview)
        
        # Initial load of appointments
        self.refresh_appointment_list()

    def refresh_patient_combobox(self):
        query = "SELECT patient_id, CONCAT(first_name, ' ', last_name) FROM patients"
        results = self.db_manager.execute_query('patients_db', query)
        
        if results:
            self.patient_dict = {f"{name} (ID: {id})": id for id, name in results}
            self.patient_combobox['values'] = list(self.patient_dict.keys())

    def refresh_doctor_combobox(self):
        query = "SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors"
        results = self.db_manager.execute_query('appointments_db', query)
        
        if results:
            self.doctor_dict = {f"{name} (ID: {id})": id for id, name in results}
            current_selection = self.doctor_combobox.get()  # Store current selection
            self.doctor_combobox['values'] = list(self.doctor_dict.keys())
            if current_selection in self.doctor_dict:  # Restore selection if still valid
                self.doctor_combobox.set(current_selection)

    def refresh_billing_patient_combobox(self):
        query = "SELECT patient_id, CONCAT(first_name, ' ', last_name) FROM patients"
        results = self.db_manager.execute_query('patients_db', query)
        
        if results:
            self.billing_patient_dict = {f"{name} (ID: {id})": id for id, name in results}
            self.billing_patient_combobox['values'] = list(self.billing_patient_dict.keys())

    def create_invoice(self):
        selected_patient = self.billing_patient_combobox.get()
        
        if not selected_patient or not self.invoice_amount.get():
            messagebox.showerror("Error", "Please select a patient and enter amount")
            return
        
        try:
            # Fix: Get patient ID from the selected string
            patient_id = self.billing_patient_dict[selected_patient]
            
            # Fix: Query the patients table directly
            verify_query = "SELECT patient_id FROM patients WHERE patient_id = %s"
            patient_exists = self.db_manager.execute_query('patients_db', verify_query, (patient_id,))
            
            if not patient_exists:
                messagebox.showerror("Error", "Selected patient no longer exists in the database")
                return
                
            # Create invoice if patient exists
            query = """INSERT INTO invoices (patient_id, amount, payment_status) 
                      VALUES (%s, %s, 'Pending')"""
            params = (patient_id, self.invoice_amount.get())
            
            if self.db_manager.execute_query('billing_db', query, params):
                messagebox.showinfo("Success", "Invoice created successfully!")
                self.billing_patient_combobox.set('')
                self.invoice_amount.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create invoice: {str(e)}")


    def refresh_patient_list(self):
        query = "SELECT patient_id, CONCAT(first_name, ' ', last_name), date_of_birth FROM patients"
        results = self.db_manager.execute_query('patients_db', query)
        
        # Clear existing items
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
            
        # Only try to insert results if we got valid data back
        if results:
            for result in results:
                self.patient_tree.insert('', 'end', values=result)
        else:
            print("No patient data retrieved from database")

    def setup_doctors_tab(self):
        # Doctor Information Form
        form_frame = ttk.LabelFrame(self.doctors_tab, text="Doctor Information", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Add doctor ID field for updates
        ttk.Label(form_frame, text="Doctor ID:").grid(row=0, column=0, padx=5, pady=5)
        self.doctor_id = ttk.Entry(form_frame)
        self.doctor_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="First Name:").grid(row=1, column=0, padx=5, pady=5)
        self.doctor_first_name = ttk.Entry(form_frame)
        self.doctor_first_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=2, column=0, padx=5, pady=5)
        self.doctor_last_name = ttk.Entry(form_frame)
        self.doctor_last_name.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Specialization:").grid(row=3, column=0, padx=5, pady=5)
        self.doctor_specialization = ttk.Combobox(form_frame, state="readonly")
        self.doctor_specialization['values'] = [
            'General Internal Medicine',
            'Cardiology'
        ]
        self.doctor_specialization.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Number:").grid(row=4, column=0, padx=5, pady=5)
        self.doctor_contact = ttk.Entry(form_frame)
        self.doctor_contact.grid(row=4, column=1, padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Doctor", command=self.add_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Doctor", command=self.update_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Doctor", command=self.delete_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_doctor_form).pack(side=tk.LEFT, padx=5)

        # Doctor List with scrollbar
        list_frame = ttk.LabelFrame(self.doctors_tab, text="Doctor List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.doctor_tree = ttk.Treeview(list_frame, 
                                      columns=("ID", "Name", "Specialization", "Contact"), 
                                      show="headings",
                                      yscrollcommand=scrollbar.set)
        self.doctor_tree.heading("ID", text="ID")
        self.doctor_tree.heading("Name", text="Name")
        self.doctor_tree.heading("Specialization", text="Specialization")
        self.doctor_tree.heading("Contact", text="Contact")
        
        # Set column widths
        self.doctor_tree.column("ID", width=50)
        self.doctor_tree.column("Name", width=200)
        self.doctor_tree.column("Specialization", width=150)
        self.doctor_tree.column("Contact", width=120)
        self.doctor_tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.doctor_tree.yview)

        # Bind treeview selection event
        self.doctor_tree.bind('<<TreeviewSelect>>', self.on_doctor_select)
        
        # Initial load of doctor list
        self.refresh_doctor_list()

    def clear_doctor_form(self):
        self.doctor_id.delete(0, tk.END)
        self.doctor_first_name.delete(0, tk.END)
        self.doctor_last_name.delete(0, tk.END)
        self.doctor_specialization.delete(0, tk.END)
        self.doctor_contact.delete(0, tk.END)

    def on_doctor_select(self, event):
        selected_items = self.doctor_tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.doctor_tree.item(item)['values']
            if values:
                self.doctor_id.delete(0, tk.END)
                self.doctor_id.insert(0, values[0])
                
                # Split the name into first and last name
                full_name = values[1].split()
                self.doctor_first_name.delete(0, tk.END)
                self.doctor_last_name.delete(0, tk.END)
                if len(full_name) > 0:
                    self.doctor_first_name.insert(0, full_name[0])
                if len(full_name) > 1:
                    self.doctor_last_name.insert(0, ' '.join(full_name[1:]))
                
                self.doctor_specialization.set(values[2])
                
                self.doctor_contact.delete(0, tk.END)
                self.doctor_contact.insert(0, values[3])

    def add_doctor(self):
        query = """INSERT INTO doctors (first_name, last_name, specialization, contact_number) 
                  VALUES (%s, %s, %s, %s)"""
        params = (self.doctor_first_name.get(), self.doctor_last_name.get(),
                 self.doctor_specialization.get(), self.doctor_contact.get())
        if self.db_manager.execute_query('appointments_db', query, params):
            messagebox.showinfo("Success", "Doctor added successfully!")
            self.refresh_doctor_list()
            self.clear_doctor_form()

    def update_doctor(self):
        if not self.doctor_id.get():
            messagebox.showerror("Error", "Please select a doctor to update")
            return

        query = """UPDATE doctors 
                  SET first_name = %s, last_name = %s, specialization = %s, contact_number = %s 
                  WHERE doctor_id = %s"""
        params = (self.doctor_first_name.get(), self.doctor_last_name.get(),
                 self.doctor_specialization.get(), self.doctor_contact.get(),
                 self.doctor_id.get())
        
        if self.db_manager.execute_query('appointments_db', query, params):
            messagebox.showinfo("Success", "Doctor updated successfully!")
            self.refresh_doctor_list()
            self.clear_doctor_form()

    def delete_doctor(self):
        if not self.doctor_id.get():
            messagebox.showerror("Error", "Please select a doctor to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?"):
            query = "DELETE FROM doctors WHERE doctor_id = %s"
            params = (self.doctor_id.get(),)
            
            if self.db_manager.execute_query('appointments_db', query, params):
                messagebox.showinfo("Success", "Doctor deleted successfully!")
                self.refresh_doctor_list()
                self.clear_doctor_form()

    def refresh_doctor_list(self):
        query = """SELECT doctor_id, CONCAT(first_name, ' ', last_name), 
                  specialization, contact_number FROM doctors"""
        results = self.db_manager.execute_query('appointments_db', query)
        
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
            
        for result in results:
            self.doctor_tree.insert('', 'end', values=result)

    def refresh_appointment_list(self):
        query = """
            SELECT a.appointment_id,
                   CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                   CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
                   a.appointment_date,
                   a.status
            FROM appointments a
            JOIN patients_db.patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
        """
        results = self.db_manager.execute_query('appointments_db', query)
        
        # Clear existing items
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        
        # Only try to insert results if we got valid data back
        if results:
            for result in results:
                self.appointment_tree.insert('', 'end', values=result)

    def add_patient(self):
        if not self.first_name.get() or not self.last_name.get() or not self.dob.get():
            messagebox.showerror("Error", "Please fill in all fields")
            return
    
        query = """INSERT INTO patients (first_name, last_name, date_of_birth) 
                  VALUES (%s, %s, %s)"""
        params = (self.first_name.get(), self.last_name.get(), self.dob.get())
        
        if self.db_manager.execute_query('patients_db', query, params):
            messagebox.showinfo("Success", "Patient added successfully!")
            self.refresh_patient_list()
            self.clear_patient_form()

    def setup_billing_tab(self):
        # Billing Form
        form_frame = ttk.LabelFrame(self.billing_tab, text="New Invoice", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(form_frame, text="Patient:").grid(row=0, column=0, padx=5, pady=5)
        self.billing_patient_combobox = ttk.Combobox(form_frame, state="readonly")
        self.billing_patient_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.refresh_billing_patient_combobox()

        ttk.Label(form_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.invoice_amount = ttk.Entry(form_frame)
        self.invoice_amount.grid(row=1, column=1, padx=5, pady=5)

        # Fix the button command binding
        create_invoice_btn = ttk.Button(form_frame, text="Create Invoice", command=self.create_invoice)
        create_invoice_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Invoice List with scrollbar
        list_frame = ttk.LabelFrame(self.billing_tab, text="Invoice List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.invoice_tree = ttk.Treeview(list_frame,
                                       columns=("ID", "Patient", "Amount", "Status"),
                                       show="headings",
                                       yscrollcommand=scrollbar.set)
        self.invoice_tree.heading("ID", text="ID")
        self.invoice_tree.heading("Patient", text="Patient")
        self.invoice_tree.heading("Amount", text="Amount")
        self.invoice_tree.heading("Status", text="Status")
        self.invoice_tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.invoice_tree.yview)
        
        # Initial load of invoices
        self.refresh_invoice_list()

    def refresh_invoice_list(self):
        query = """
            SELECT i.invoice_id,
                   (SELECT CONCAT(p.first_name, ' ', p.last_name) 
                    FROM patients_db.patients p 
                    WHERE p.patient_id = i.patient_id) as patient_name,
                   i.amount,
                   i.payment_status
            FROM invoices i
        """
        results = self.db_manager.execute_query('billing_db', query)
        
        # Clear existing items
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        # Only try to insert results if we got valid data back
        if results:
            for result in results:
                self.invoice_tree.insert('', 'end', values=result)

    def setup_auto_refresh(self):
        """Set up auto-refresh for appointments list"""
        self.refresh_appointment_list()
        # Schedule the next refresh in 30 seconds
        self.root.after(30000, self.setup_auto_refresh)

    def setup_auto_refresh(self):
        """Set up auto-refresh for appointments list"""
        self.refresh_appointment_list()
        # Schedule the next refresh in 30 seconds
        self.root.after(30000, self.setup_auto_refresh)

    def setup_doctor_auto_refresh(self):
        """Set up auto-refresh for doctor combobox"""
        self.refresh_doctor_combobox()
        # Schedule the next refresh in 30 seconds
        self.root.after(30000, self.setup_doctor_auto_refresh)

    def refresh_doctor_combobox(self):
        query = "SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors"
        results = self.db_manager.execute_query('appointments_db', query)
        
        if results:
            self.doctor_dict = {f"{name} (ID: {id})": id for id, name in results}
            current_selection = self.doctor_combobox.get()  # Store current selection
            self.doctor_combobox['values'] = list(self.doctor_dict.keys())
            if current_selection in self.doctor_dict:  # Restore selection if still valid
                self.doctor_combobox.set(current_selection)

    def setup_patient_auto_refresh(self):
        """Set up auto-refresh for patient list"""
        self.refresh_patient_list()
        # Schedule the next refresh in 30 seconds
        self.root.after(30000, self.setup_patient_auto_refresh)

    def refresh_patient_list(self):
        query = "SELECT patient_id, CONCAT(first_name, ' ', last_name), date_of_birth FROM patients"
        results = self.db_manager.execute_query('patients_db', query)
        
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
            
        for result in results:
            self.patient_tree.insert('', 'end', values=result)

    def setup_doctors_tab(self):
        # Doctor Information Form
        form_frame = ttk.LabelFrame(self.doctors_tab, text="Doctor Information", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Add doctor ID field for updates
        ttk.Label(form_frame, text="Doctor ID:").grid(row=0, column=0, padx=5, pady=5)
        self.doctor_id = ttk.Entry(form_frame)
        self.doctor_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="First Name:").grid(row=1, column=0, padx=5, pady=5)
        self.doctor_first_name = ttk.Entry(form_frame)
        self.doctor_first_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=2, column=0, padx=5, pady=5)
        self.doctor_last_name = ttk.Entry(form_frame)
        self.doctor_last_name.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Specialization:").grid(row=3, column=0, padx=5, pady=5)
        self.doctor_specialization = ttk.Combobox(form_frame, state="readonly")
        self.doctor_specialization['values'] = [
            'General Internal Medicine',
            'Cardiology'
        ]
        self.doctor_specialization.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Number:").grid(row=4, column=0, padx=5, pady=5)
        self.doctor_contact = ttk.Entry(form_frame)
        self.doctor_contact.grid(row=4, column=1, padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Doctor", command=self.add_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Doctor", command=self.update_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Doctor", command=self.delete_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_doctor_form).pack(side=tk.LEFT, padx=5)

        # Doctor List with scrollbar
        list_frame = ttk.LabelFrame(self.doctors_tab, text="Doctor List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.doctor_tree = ttk.Treeview(list_frame, 
                                      columns=("ID", "Name", "Specialization", "Contact"), 
                                      show="headings",
                                      yscrollcommand=scrollbar.set)
        self.doctor_tree.heading("ID", text="ID")
        self.doctor_tree.heading("Name", text="Name")
        self.doctor_tree.heading("Specialization", text="Specialization")
        self.doctor_tree.heading("Contact", text="Contact")
        
        # Set column widths
        self.doctor_tree.column("ID", width=50)
        self.doctor_tree.column("Name", width=200)
        self.doctor_tree.column("Specialization", width=150)
        self.doctor_tree.column("Contact", width=120)
        self.doctor_tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.doctor_tree.yview)

        # Bind treeview selection event
        self.doctor_tree.bind('<<TreeviewSelect>>', self.on_doctor_select)
        
        # Initial load of doctor list
        self.refresh_doctor_list()

    def clear_doctor_form(self):
        self.doctor_id.delete(0, tk.END)
        self.doctor_first_name.delete(0, tk.END)
        self.doctor_last_name.delete(0, tk.END)
        self.doctor_specialization.delete(0, tk.END)
        self.doctor_contact.delete(0, tk.END)

    def on_doctor_select(self, event):
        selected_items = self.doctor_tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.doctor_tree.item(item)['values']
            if values:
                self.doctor_id.delete(0, tk.END)
                self.doctor_id.insert(0, values[0])
                
                # Split the name into first and last name
                full_name = values[1].split()
                self.doctor_first_name.delete(0, tk.END)
                self.doctor_last_name.delete(0, tk.END)
                if len(full_name) > 0:
                    self.doctor_first_name.insert(0, full_name[0])
                if len(full_name) > 1:
                    self.doctor_last_name.insert(0, ' '.join(full_name[1:]))
                
                self.doctor_specialization.set(values[2])
                
                self.doctor_contact.delete(0, tk.END)
                self.doctor_contact.insert(0, values[3])

    def add_doctor(self):
        query = """INSERT INTO doctors (first_name, last_name, specialization, contact_number) 
                  VALUES (%s, %s, %s, %s)"""
        params = (self.doctor_first_name.get(), self.doctor_last_name.get(),
                 self.doctor_specialization.get(), self.doctor_contact.get())
        if self.db_manager.execute_query('appointments_db', query, params):
            messagebox.showinfo("Success", "Doctor added successfully!")
            self.refresh_doctor_list()
            self.clear_doctor_form()

    def update_doctor(self):
        if not self.doctor_id.get():
            messagebox.showerror("Error", "Please select a doctor to update")
            return

        query = """UPDATE doctors 
                  SET first_name = %s, last_name = %s, specialization = %s, contact_number = %s 
                  WHERE doctor_id = %s"""
        params = (self.doctor_first_name.get(), self.doctor_last_name.get(),
                 self.doctor_specialization.get(), self.doctor_contact.get(),
                 self.doctor_id.get())
        
        if self.db_manager.execute_query('appointments_db', query, params):
            messagebox.showinfo("Success", "Doctor updated successfully!")
            self.refresh_doctor_list()
            self.clear_doctor_form()

    def delete_doctor(self):
        if not self.doctor_id.get():
            messagebox.showerror("Error", "Please select a doctor to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?"):
            query = "DELETE FROM doctors WHERE doctor_id = %s"
            params = (self.doctor_id.get(),)
            
            if self.db_manager.execute_query('appointments_db', query, params):
                messagebox.showinfo("Success", "Doctor deleted successfully!")
                self.refresh_doctor_list()
                self.clear_doctor_form()

    def refresh_doctor_list(self):
        query = """SELECT doctor_id, CONCAT(first_name, ' ', last_name), 
                  specialization, contact_number FROM doctors"""
        results = self.db_manager.execute_query('appointments_db', query)
        
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
            
        for result in results:
            self.doctor_tree.insert('', 'end', values=result)

    def refresh_appointment_list(self):
        query = """
            SELECT a.appointment_id,
                   CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                   CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
                   a.appointment_date,
                   a.status
            FROM appointments a
            JOIN patients_db.patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
        """
        results = self.db_manager.execute_query('appointments_db', query)
        
        # Clear existing items
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        
        # Only try to insert results if we got valid data back
        if results:
            for result in results:
                self.appointment_tree.insert('', 'end', values=result)

    def add_patient(self):
        if not self.first_name.get() or not self.last_name.get() or not self.dob.get():
            messagebox.showerror("Error", "Please fill in all fields")
            return
    
        query = """INSERT INTO patients (first_name, last_name, date_of_birth) 
                  VALUES (%s, %s, %s)"""
        params = (self.first_name.get(), self.last_name.get(), self.dob.get())
        
        if self.db_manager.execute_query('patients_db', query, params):
            messagebox.showinfo("Success", "Patient added successfully!")
            self.refresh_patient_list()
            self.clear_patient_form()

    def setup_billing_tab(self):
        # Billing Form
        form_frame = ttk.LabelFrame(self.billing_tab, text="New Invoice", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(form_frame, text="Patient:").grid(row=0, column=0, padx=5, pady=5)
        self.billing_patient_combobox = ttk.Combobox(form_frame, state="readonly")
        self.billing_patient_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.refresh_billing_patient_combobox()

        ttk.Label(form_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.invoice_amount = ttk.Entry(form_frame)
        self.invoice_amount.grid(row=1, column=1, padx=5, pady=5)

        # Fix the button command binding
        create_invoice_btn = ttk.Button(form_frame, text="Create Invoice", command=self.create_invoice)
        create_invoice_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Invoice List with scrollbar
        list_frame = ttk.LabelFrame(self.billing_tab, text="Invoice List", padding=15)
        list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.invoice_tree = ttk.Treeview(list_frame,
                                       columns=("ID", "Patient", "Amount", "Status"),
                                       show="headings",
                                       yscrollcommand=scrollbar.set)
        self.invoice_tree.heading("ID", text="ID")
        self.invoice_tree.heading("Patient", text="Patient")
        self.invoice_tree.heading("Amount", text="Amount")
        self.invoice_tree.heading("Status", text="Status")
        self.invoice_tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.invoice_tree.yview)
        
        # Initial load of invoices
        self.refresh_invoice_list()

    def refresh_invoice_list(self):
        query = """
            SELECT i.invoice_id,
                   (SELECT CONCAT(p.first_name, ' ', p.last_name) 
                    FROM patients_db.patients p 
                    WHERE p.patient_id = i.patient_id) as patient_name,
                   i.amount,
                   i.payment_status
            FROM invoices i
        """
        results = self.db_manager.execute_query('billing_db', query)
        
        # Clear existing items
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        # Only try to insert results if we got valid data back
        if results:
            for result in results:
                self.invoice_tree.insert('', 'end', values=result)

    def setup_auto_refresh(self):
        """Set up auto-refresh for appointments list"""
        self.refresh_appointment_list()
        # Schedule the next refresh in 30 seconds
        self.root.after(30000, self.setup_auto_refresh)

    def setup_auto_refresh(self):
        """Set up auto-refresh for appointments list"""
        self.refresh_appointment_list()
        # Schedule the next refresh in 30 seconds
        self.root.after(30000, self.setup_auto_refresh)

    def setup_doctor_auto_refresh(self):
        """Set up auto-refresh for doctor combobox"""
        self.refresh_doctor_combobox()
        # Schedule the next refresh in 30 seconds
        self.root.after(30000, self.setup_doctor_auto_refresh)

    def refresh_doctor_combobox(self):
        query = "SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors"
        results = self.db_manager.execute_query('appointments_db', query)
        
        if results:
            self.doctor_dict = {f"{name} (ID: {id})": id for id, name in results}
            current_selection = self.doctor_combobox.get()  # Store current selection
            self.doctor_combobox['values'] = list(self.doctor_dict.keys())
            if current_selection in self.doctor_dict:  # Restore selection if still valid
                self.doctor_combobox.set(current_selection)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.geometry("800x600")
    root.mainloop()