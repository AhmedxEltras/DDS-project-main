import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AppointmentsTab:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        # Configure grid
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=3)  # Tree gets more space
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create frames
        form_frame = ttk.LabelFrame(self.parent, text="Appointment Information", padding=15)
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        tree_frame = ttk.LabelFrame(self.parent, text="Appointments List", padding=15)
        tree_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        # Configure form frame grid
        form_frame.grid_columnconfigure(1, weight=1)
        for i in range(10):  # Approximate number of rows
            form_frame.grid_rowconfigure(i, weight=1)
            
        # Configure tree frame grid
        tree_frame.grid_rowconfigure(1, weight=1)  # TreeView gets all extra space
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Appointment Information Form
        ttk.Label(form_frame, text="Appointment ID:").grid(row=0, column=0, padx=5, pady=5)
        self.appointment_id = ttk.Entry(form_frame)
        self.appointment_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Patient:").grid(row=1, column=0, padx=5, pady=5)
        self.patient_combo = ttk.Combobox(form_frame)
        self.patient_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Doctor:").grid(row=2, column=0, padx=5, pady=5)
        self.doctor_combo = ttk.Combobox(form_frame)
        self.doctor_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        self.date = ttk.Entry(form_frame)
        self.date.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Time (HH:MM):").grid(row=4, column=0, padx=5, pady=5)
        self.time = ttk.Entry(form_frame)
        self.time.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Status:").grid(row=5, column=0, padx=5, pady=5)
        self.status_combo = ttk.Combobox(form_frame, values=["Scheduled", "Completed", "Cancelled"])
        self.status_combo.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Notes:").grid(row=6, column=0, padx=5, pady=5)
        self.notes = ttk.Entry(form_frame)
        self.notes.grid(row=6, column=1, padx=5, pady=5)

        # Buttons
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        
        # Add buttons
        ttk.Button(buttons_frame, text="Add", command=self.add_appointment).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Update", command=self.update_appointment).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Delete", command=self.delete_appointment).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)
        
        # Create Treeview with scrollbars
        tree_container = ttk.Frame(tree_frame)
        tree_container.grid(row=1, column=0, sticky='nsew')
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_container,
                                columns=('ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status'),
                                show='headings')
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        
        # Grid scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Patient', text='Patient')
        self.tree.heading('Doctor', text='Doctor')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Status', text='Status')
        
        # Set column weights
        total_width = tree_container.winfo_width()
        self.tree.column('ID', width=int(total_width * 0.1), minwidth=50)
        self.tree.column('Patient', width=int(total_width * 0.2), minwidth=100)
        self.tree.column('Doctor', width=int(total_width * 0.2), minwidth=100)
        self.tree.column('Date', width=int(total_width * 0.15), minwidth=80)
        self.tree.column('Time', width=int(total_width * 0.15), minwidth=80)
        self.tree.column('Status', width=int(total_width * 0.2), minwidth=80)
        
        # Bind select event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Bind resize event to adjust column widths
        tree_container.bind('<Configure>', self.on_tree_resize)
        
        # Initial refresh
        self.refresh_lists()
        self.refresh_appointments()

    def refresh_lists(self):
        # Refresh patient list
        query = "SELECT patient_id, first_name, last_name FROM patients"
        results = self.db_manager.execute_query('patients_db', query)
        if results:
            self.patients = {f"{fname} {lname}": pid for pid, fname, lname in results}
            self.patient_combo['values'] = list(self.patients.keys())

        # Refresh doctor list
        query = "SELECT doctor_id, first_name, last_name FROM doctors"
        results = self.db_manager.execute_query('appointments_db', query)
        if results:
            self.doctors = {f"{fname} {lname}": did for did, fname, lname in results}
            self.doctor_combo['values'] = list(self.doctors.keys())

    def clear_form(self):
        self.appointment_id.delete(0, tk.END)
        self.patient_combo.set('')
        self.doctor_combo.set('')
        self.date.delete(0, tk.END)
        self.time.delete(0, tk.END)
        self.status_combo.set('')
        self.notes.delete(0, tk.END)

    def add_appointment(self):
        patient_name = self.patient_combo.get()
        doctor_name = self.doctor_combo.get()
        date = self.date.get()
        time = self.time.get()
        status = self.status_combo.get()
        notes = self.notes.get()
        
        if not all([patient_name, doctor_name, date, time, status]):
            messagebox.showerror("Error", "All fields except notes are required!")
            return
            
        patient_id = self.patients.get(patient_name)
        doctor_id = self.doctors.get(doctor_name)
        
        if not patient_id or not doctor_id:
            messagebox.showerror("Error", "Invalid patient or doctor selection!")
            return
            
        query = """INSERT INTO appointments 
                   (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
                   VALUES (%s, %s, STR_TO_DATE(%s, '%Y-%m-%d'), STR_TO_DATE(%s, '%H:%i'), %s, %s)"""
        params = (patient_id, doctor_id, date, time, status, notes)
        
        result = self.db_manager.execute_query('appointments_db', query, params)
        if result:
            messagebox.showinfo("Success", "Appointment added successfully!")
            self.clear_form()
            self.refresh_appointments()
        else:
            messagebox.showerror("Error", "Failed to add appointment!")

    def update_appointment(self):
        appointment_id = self.appointment_id.get()
        if not appointment_id:
            messagebox.showerror("Error", "Please select an appointment to update!")
            return
            
        patient_name = self.patient_combo.get()
        doctor_name = self.doctor_combo.get()
        date = self.date.get()
        time = self.time.get()
        status = self.status_combo.get()
        notes = self.notes.get()
        
        patient_id = self.patients.get(patient_name)
        doctor_id = self.doctors.get(doctor_name)
        
        query = """UPDATE appointments 
                   SET patient_id = %s, doctor_id = %s, 
                       appointment_date = STR_TO_DATE(%s, '%Y-%m-%d'),
                       appointment_time = STR_TO_DATE(%s, '%H:%i'), 
                       status = %s, notes = %s
                   WHERE appointment_id = %s"""
        params = (patient_id, doctor_id, date, time, status, notes, appointment_id)
        
        result = self.db_manager.execute_query('appointments_db', query, params)
        if result is not None:
            messagebox.showinfo("Success", "Appointment updated successfully!")
            self.clear_form()
            self.refresh_appointments()
        else:
            messagebox.showerror("Error", "Failed to update appointment!")

    def delete_appointment(self):
        appointment_id = self.appointment_id.get()
        if not appointment_id:
            messagebox.showerror("Error", "Please select an appointment to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this appointment?"):
            # First, delete related records in invoices
            delete_invoices = "DELETE FROM billing_db.invoices WHERE appointment_id = %s"
            self.db_manager.execute_query('billing_db', delete_invoices, (appointment_id,))
            
            # Then, delete related records in medical records
            delete_records = "DELETE FROM medical_db.medical_records WHERE appointment_id = %s"
            self.db_manager.execute_query('medical_db', delete_records, (appointment_id,))
            
            # Finally, delete the appointment
            delete_appointment = "DELETE FROM appointments WHERE appointment_id = %s"
            result = self.db_manager.execute_query('appointments_db', delete_appointment, (appointment_id,))
            
            if result is not None:
                messagebox.showinfo("Success", "Appointment deleted successfully!")
                self.clear_form()
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to delete appointment!")

    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)['values']
            if values:
                self.appointment_id.delete(0, tk.END)
                self.appointment_id.insert(0, values[0])
                self.patient_combo.set(values[1])
                self.doctor_combo.set(values[2])
                self.date.delete(0, tk.END)
                self.date.insert(0, values[3])
                self.time.delete(0, tk.END)
                self.time.insert(0, values[4])
                self.status_combo.set(values[5])

    def refresh_appointments(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # First get all appointments
        query_appointments = """
            SELECT a.appointment_id, a.patient_id, a.doctor_id,
                   DATE_FORMAT(a.appointment_date, '%Y-%m-%d') as date,
                   TIME_FORMAT(a.appointment_time, '%H:%i') as time,
                   a.status
            FROM appointments a
            ORDER BY a.appointment_date, a.appointment_time
        """
        appointments = self.db_manager.execute_query('appointments_db', query_appointments)
        
        if not appointments:
            return
            
        # Get all patients
        query_patients = "SELECT patient_id, first_name, last_name FROM patients"
        patients_result = self.db_manager.execute_query('patients_db', query_patients)
        patients = {p[0]: f"{p[1]} {p[2]}" for p in patients_result} if patients_result else {}
        
        # Get all doctors
        query_doctors = "SELECT doctor_id, first_name, last_name FROM doctors"
        doctors_result = self.db_manager.execute_query('appointments_db', query_doctors)
        doctors = {d[0]: f"{d[1]} {d[2]}" for d in doctors_result} if doctors_result else {}
        
        # Combine the data
        for appt in appointments:
            appointment_id = appt[0]
            patient_id = appt[1]
            doctor_id = appt[2]
            date = appt[3]
            time = appt[4]
            status = appt[5]
            
            patient_name = patients.get(patient_id, f"Patient {patient_id}")
            doctor_name = doctors.get(doctor_id, f"Doctor {doctor_id}")
            
            self.tree.insert('', 'end', values=(
                appointment_id,
                patient_name,
                doctor_name,
                date,
                time,
                status
            ))
        


    def on_tree_resize(self, event):
        # Adjust column widths based on container width
        width = event.width
        self.tree.column('ID', width=int(width * 0.1), minwidth=50)
        self.tree.column('Patient', width=int(width * 0.2), minwidth=100)
        self.tree.column('Doctor', width=int(width * 0.2), minwidth=100)
        self.tree.column('Date', width=int(width * 0.15), minwidth=80)
        self.tree.column('Time', width=int(width * 0.15), minwidth=80)
        self.tree.column('Status', width=int(width * 0.2), minwidth=80)
