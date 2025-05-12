import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class BillingTab:
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
        form_frame = ttk.LabelFrame(self.parent, text="Billing Information", padding=15)
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        tree_frame = ttk.LabelFrame(self.parent, text="Billing List", padding=15)
        tree_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        # Configure form frame grid
        form_frame.grid_columnconfigure(1, weight=1)
        for i in range(10):  # Approximate number of rows
            form_frame.grid_rowconfigure(i, weight=1)
            
        # Configure tree frame grid
        tree_frame.grid_rowconfigure(1, weight=1)  # TreeView gets all extra space
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Billing Information Form
        ttk.Label(form_frame, text="Invoice ID:").grid(row=0, column=0, padx=5, pady=5)
        self.invoice_id = ttk.Entry(form_frame)
        self.invoice_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Patient:").grid(row=1, column=0, padx=5, pady=5)
        self.patient_combo = ttk.Combobox(form_frame)
        self.patient_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Appointment:").grid(row=2, column=0, padx=5, pady=5)
        self.appointment_combo = ttk.Combobox(form_frame)
        self.appointment_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Amount:").grid(row=3, column=0, padx=5, pady=5)
        self.amount = ttk.Entry(form_frame)
        self.amount.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5)
        self.status_combo = ttk.Combobox(form_frame, values=["Pending", "Paid", "Cancelled"])
        self.status_combo.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Payment Date:").grid(row=5, column=0, padx=5, pady=5)
        self.payment_date = ttk.Entry(form_frame)
        self.payment_date.grid(row=5, column=1, padx=5, pady=5)

        # Buttons
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(buttons_frame, text="Add", command=self.add_invoice).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Update", command=self.update_invoice).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Delete", command=self.delete_invoice).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)
        
        # Create Treeview with scrollbars
        tree_container = ttk.Frame(tree_frame)
        tree_container.grid(row=1, column=0, sticky='nsew')
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_container,
                                columns=('ID', 'Patient', 'Amount', 'Status', 'IssueDate', 'DueDate', 'PaymentDate'),
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
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Status', text='Status')
        self.tree.heading('IssueDate', text='Issue Date')
        self.tree.heading('DueDate', text='Due Date')
        self.tree.heading('PaymentDate', text='Payment Date')
        
        # Set column weights
        total_width = tree_container.winfo_width()
        self.tree.column('ID', width=int(total_width * 0.1), minwidth=50)
        self.tree.column('Patient', width=int(total_width * 0.2), minwidth=100)
        self.tree.column('Amount', width=int(total_width * 0.1), minwidth=80)
        self.tree.column('Status', width=int(total_width * 0.1), minwidth=80)
        self.tree.column('IssueDate', width=int(total_width * 0.15), minwidth=80)
        self.tree.column('DueDate', width=int(total_width * 0.15), minwidth=80)
        self.tree.column('PaymentDate', width=int(total_width * 0.15), minwidth=80)
        
        # Bind select event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Bind resize event to adjust column widths
        tree_container.bind('<Configure>', self.on_tree_resize)
        
        # Initial refresh
        self.refresh_lists()
        self.refresh_invoices()

    def refresh_lists(self):
        # Refresh patient list
        query = "SELECT patient_id, first_name, last_name FROM patients"
        results = self.db_manager.execute_query('patients_db', query)
        if results:
            self.patients = {f"{fname} {lname}": pid for pid, fname, lname in results}
            self.patient_combo['values'] = list(self.patients.keys())

        # Refresh appointment list based on selected patient
        self.refresh_appointments()

    def refresh_appointments(self, patient_id=None):
        # Get appointments
        if patient_id:
            query = """
                SELECT a.appointment_id, a.appointment_date, a.appointment_time, a.doctor_id
                FROM appointments a
                WHERE a.patient_id = %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """
            results = self.db_manager.execute_query('appointments_db', query, (patient_id,))
        else:
            query = """
                SELECT a.appointment_id, a.appointment_date, a.appointment_time, a.doctor_id
                FROM appointments a
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """
            results = self.db_manager.execute_query('appointments_db', query)
        
        if not results:
            self.appointment_combo['values'] = []
            self.appointments = {}
            return
            
        # Get doctor information
        doctor_ids = [result[3] for result in results]
        if doctor_ids:
            placeholders = ', '.join(['%s'] * len(doctor_ids))
            query_doctors = f"SELECT doctor_id, first_name, last_name FROM doctors WHERE doctor_id IN ({placeholders})"
            doctors_result = self.db_manager.execute_query('appointments_db', query_doctors, doctor_ids)
            doctors = {d[0]: f"{d[1]} {d[2]}" for d in doctors_result} if doctors_result else {}
        else:
            doctors = {}
            
        # Format appointments with doctor names
        self.appointments = {}
        appointment_values = []
        
        for aid, date, time, doctor_id in results:
            doctor_name = doctors.get(doctor_id, "Unknown Doctor")
            formatted_date = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else date
            formatted_time = time.strftime('%H:%M') if hasattr(time, 'strftime') else time
            appointment_display = f"{formatted_date} {formatted_time} - {doctor_name}"
            self.appointments[appointment_display] = aid
            appointment_values.append(appointment_display)
            
        self.appointment_combo['values'] = appointment_values

    def clear_form(self):
        self.invoice_id.delete(0, tk.END)
        self.patient_combo.set('')
        self.appointment_combo.set('')
        self.amount.delete(0, tk.END)
        self.status_combo.set('')
        self.payment_date.delete(0, tk.END)

    def add_invoice(self):
        patient_name = self.patient_combo.get()
        appointment_time = self.appointment_combo.get()
        amount = self.amount.get()
        status = self.status_combo.get()
        payment_date = self.payment_date.get() if self.payment_date.get() else None
        # Convert empty string to None for SQL NULL
        if payment_date == '':
            payment_date = None
        
        if not all([patient_name, amount, status]):
            messagebox.showerror("Error", "Patient, amount and status are required!")
            return
            
        patient_id = self.patients.get(patient_name)
        appointment_id = self.appointments.get(appointment_time) if appointment_time else None
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
            return
        
        # Set issue_date to today and due_date to 30 days from today
        today = datetime.now().date()
        issue_date = today.strftime('%Y-%m-%d')
        due_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')
            
        query = """INSERT INTO invoices 
                   (patient_id, appointment_id, amount, payment_status, issue_date, due_date, payment_date)
                   VALUES (%s, %s, %s, %s, %s, %s, NULLIF(%s, ''))"""
        params = (patient_id, appointment_id, amount, status, issue_date, due_date, payment_date if payment_date else '')
        
        result = self.db_manager.execute_query('billing_db', query, params)
        if result:
            messagebox.showinfo("Success", "Invoice added successfully!")
            self.clear_form()
            self.refresh_invoices()
        else:
            messagebox.showerror("Error", "Failed to add invoice!")

    def update_invoice(self):
        invoice_id = self.invoice_id.get()
        if not invoice_id:
            messagebox.showerror("Error", "Please select an invoice to update!")
            return
            
        patient_name = self.patient_combo.get()
        appointment_time = self.appointment_combo.get()
        amount = self.amount.get()
        status = self.status_combo.get()
        payment_date = self.payment_date.get() if self.payment_date.get() else None
        # Convert empty string to None for SQL NULL
        if payment_date == '':
            payment_date = None
        
        patient_id = self.patients.get(patient_name)
        appointment_id = self.appointments.get(appointment_time) if appointment_time else None
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
            return
            
        # Get the current invoice data to preserve issue_date and due_date
        get_invoice_query = "SELECT issue_date, due_date FROM invoices WHERE invoice_id = %s"
        invoice_data = self.db_manager.execute_query('billing_db', get_invoice_query, (invoice_id,))
        
        if not invoice_data:
            messagebox.showerror("Error", "Could not retrieve invoice data!")
            return
            
        issue_date, due_date = invoice_data[0]
        
        query = """UPDATE invoices 
                   SET patient_id = %s, appointment_id = %s, amount = %s,
                       payment_status = %s, issue_date = %s, due_date = %s, payment_date = NULLIF(%s, '')
                   WHERE invoice_id = %s"""
        params = (patient_id, appointment_id, amount, status, issue_date, due_date, payment_date if payment_date else '', invoice_id)
        
        result = self.db_manager.execute_query('billing_db', query, params)
        if result is not None:
            messagebox.showinfo("Success", "Invoice updated successfully!")
            self.clear_form()
            self.refresh_invoices()
        else:
            messagebox.showerror("Error", "Failed to update invoice!")

    def delete_invoice(self):
        invoice_id = self.invoice_id.get()
        if not invoice_id:
            messagebox.showerror("Error", "Please select an invoice to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this invoice?"):
            query = "DELETE FROM invoices WHERE invoice_id = %s"
            result = self.db_manager.execute_query('billing_db', query, (invoice_id,))
            
            if result is not None:
                messagebox.showinfo("Success", "Invoice deleted successfully!")
                self.clear_form()
                self.refresh_invoices()
            else:
                messagebox.showerror("Error", "Failed to delete invoice!")

    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)['values']
            if values:
                self.invoice_id.delete(0, tk.END)
                self.invoice_id.insert(0, values[0])
                self.patient_combo.set(values[1])
                self.amount.delete(0, tk.END)
                self.amount.insert(0, values[2])
                self.status_combo.set(values[3])
                if values[4]:
                    self.payment_date.delete(0, tk.END)
                    self.payment_date.insert(0, values[4])

    def refresh_invoices(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch and display invoices
        query = """
            SELECT i.invoice_id, 
                   CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                   i.amount, i.payment_status, 
                   DATE_FORMAT(i.issue_date, '%Y-%m-%d') as issue_date,
                   DATE_FORMAT(i.due_date, '%Y-%m-%d') as due_date,
                   DATE_FORMAT(i.payment_date, '%Y-%m-%d') as payment_date
            FROM invoices i
            JOIN patients_db.patients p ON i.patient_id = p.patient_id
            ORDER BY i.created_at DESC
        """
        results = self.db_manager.execute_query('billing_db', query)
        
        if results:
            for invoice in results:
                self.tree.insert('', 'end', values=invoice)

    def on_tree_resize(self, event):
        # Adjust column widths based on container width
        width = event.width
        self.tree.column('ID', width=int(width * 0.1), minwidth=50)
        self.tree.column('Patient', width=int(width * 0.2), minwidth=100)
        self.tree.column('Amount', width=int(width * 0.1), minwidth=80)
        self.tree.column('Status', width=int(width * 0.1), minwidth=80)
        self.tree.column('IssueDate', width=int(width * 0.15), minwidth=80)
        self.tree.column('DueDate', width=int(width * 0.15), minwidth=80)
        self.tree.column('PaymentDate', width=int(width * 0.15), minwidth=80)
