import tkinter as tk
from tkinter import ttk, messagebox
from random import choice

class DoctorsTab:
    SPECIALIZATIONS = [
        'Cardiology',
        'Dermatology',
        'Endocrinology',
        'Family Medicine',
        'Gastroenterology',
        'Hematology',
        'Internal Medicine',
        'Neurology',
        'Obstetrics and Gynecology',
        'Oncology',
        'Ophthalmology',
        'Orthopedics',
        'Pediatrics',
        'Psychiatry',
        'Pulmonology',
        'Radiology',
        'Rheumatology',
        'Surgery',
        'Urology'
    ]
    
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
        form_frame = ttk.LabelFrame(self.parent, text="Doctor Information", padding=15)
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        tree_frame = ttk.LabelFrame(self.parent, text="Doctors List", padding=15)
        tree_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        # Configure form frame grid
        form_frame.grid_columnconfigure(1, weight=1)
        for i in range(10):  # Approximate number of rows
            form_frame.grid_rowconfigure(i, weight=1)
            
        # Configure tree frame grid
        tree_frame.grid_rowconfigure(1, weight=1)  # TreeView gets all extra space
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Doctor Information Form
        ttk.Label(form_frame, text="Doctor ID:").grid(row=0, column=0, padx=5, pady=5)
        self.doctor_id = ttk.Entry(form_frame)
        self.doctor_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="First Name:").grid(row=1, column=0, padx=5, pady=5)
        self.first_name = ttk.Entry(form_frame)
        self.first_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=2, column=0, padx=5, pady=5)
        self.last_name = ttk.Entry(form_frame)
        self.last_name.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Specialization:").grid(row=3, column=0, padx=5, pady=5)
        self.specialization = ttk.Combobox(form_frame, width=27, values=self.SPECIALIZATIONS, state='readonly')
        self.specialization.grid(row=3, column=1, padx=5, pady=5)
        self.specialization.set(choice(self.SPECIALIZATIONS))  # Set random initial value

        ttk.Label(form_frame, text="Contact Number:").grid(row=4, column=0, padx=5, pady=5)
        self.contact = ttk.Entry(form_frame)
        self.contact.grid(row=4, column=1, padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Doctor", command=self.add_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Doctor", command=self.update_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Doctor", command=self.delete_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        # Create Treeview with scrollbars
        tree_container = ttk.Frame(tree_frame)
        tree_container.grid(row=1, column=0, sticky='nsew')
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        self.doctor_tree = ttk.Treeview(tree_container,
                                      columns=('ID', 'Name', 'Specialization', 'Contact'),
                                      show='headings')
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.doctor_tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.doctor_tree.xview)
        
        # Grid scrollbars
        self.doctor_tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.doctor_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Configure columns
        self.doctor_tree.heading('ID', text='ID')
        self.doctor_tree.heading('Name', text='Name')
        self.doctor_tree.heading('Specialization', text='Specialization')
        self.doctor_tree.heading('Contact', text='Contact')
        
        # Set column weights
        total_width = tree_container.winfo_width()
        self.doctor_tree.column('ID', width=int(total_width * 0.1), minwidth=50)
        self.doctor_tree.column('Name', width=int(total_width * 0.3), minwidth=100)
        self.doctor_tree.column('Specialization', width=int(total_width * 0.4), minwidth=120)
        self.doctor_tree.column('Contact', width=int(total_width * 0.2), minwidth=80)
        
        # Bind select event
        self.doctor_tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Bind resize event to adjust column widths
        tree_container.bind('<Configure>', self.on_tree_resize)
        
        # Initial refresh
        self.refresh_list()

    def clear_form(self):
        self.doctor_id.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.specialization.set(choice(self.SPECIALIZATIONS))  # Set random specialization
        self.contact.delete(0, tk.END)

    def add_doctor(self):
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        specialization = self.specialization.get()
        contact = self.contact.get()
        
        if not all([first_name, last_name, specialization, contact]):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        query = """INSERT INTO doctors (first_name, last_name, specialization, contact_number)
                   VALUES (%s, %s, %s, %s)"""
        params = (first_name, last_name, specialization, contact)
        
        result = self.db_manager.execute_query('appointments_db', query, params)
        if result:
            messagebox.showinfo("Success", "Doctor added successfully!")
            self.clear_form()
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Failed to add doctor!")

    def update_doctor(self):
        doctor_id = self.doctor_id.get()
        if not doctor_id:
            messagebox.showerror("Error", "Please select a doctor to update!")
            return
            
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        specialization = self.specialization.get()
        contact = self.contact.get()
        
        query = """UPDATE doctors 
                   SET first_name = %s, last_name = %s, specialization = %s, contact_number = %s
                   WHERE doctor_id = %s"""
        params = (first_name, last_name, specialization, contact, doctor_id)
        
        result = self.db_manager.execute_query('appointments_db', query, params)
        if result is not None:
            messagebox.showinfo("Success", "Doctor updated successfully!")
            self.clear_form()
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Failed to update doctor!")

    def delete_doctor(self):
        doctor_id = self.doctor_id.get()
        if not doctor_id:
            messagebox.showerror("Error", "Please select a doctor to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor?"):
            try:
                # Delete related records in medical records
                delete_medical = "DELETE FROM medical_db.medical_records WHERE doctor_id = %s"
                self.db_manager.execute_query('medical_db', delete_medical, (doctor_id,))
                
                # Delete related appointments
                delete_appointments = "DELETE FROM appointments WHERE doctor_id = %s"
                self.db_manager.execute_query('appointments_db', delete_appointments, (doctor_id,))
                
                # Finally delete the doctor
                delete_doctor = "DELETE FROM doctors WHERE doctor_id = %s"
                result = self.db_manager.execute_query('appointments_db', delete_doctor, (doctor_id,))
                
                if result is not None:
                    messagebox.showinfo("Success", "Doctor deleted successfully!")
                    self.clear_form()
                    self.refresh_list()
                else:
                    messagebox.showerror("Error", "Failed to delete doctor!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor: {str(e)}")

    def on_select(self, event):
        selected_items = self.doctor_tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.doctor_tree.item(item)['values']
            if values:
                self.doctor_id.delete(0, tk.END)
                self.doctor_id.insert(0, values[0])
                self.first_name.delete(0, tk.END)
                self.first_name.insert(0, values[1].split()[0])
                self.last_name.delete(0, tk.END)
                self.last_name.insert(0, values[1].split()[1])
                self.specialization.set(values[2])
                self.contact.delete(0, tk.END)
                self.contact.insert(0, values[3])

    def refresh_list(self):
        # Clear tree
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
        
        # Get doctors from database
        query = "SELECT * FROM doctors"
        result = self.db_manager.execute_query('appointments_db', query)
        
        if result:
            for row in result:
                self.doctor_tree.insert('', 'end', values=row)
    
    def on_tree_resize(self, event):
        # Adjust column widths based on container width
        width = event.width
        self.doctor_tree.column('ID', width=int(width * 0.1), minwidth=50)
        self.doctor_tree.column('Name', width=int(width * 0.3), minwidth=100)
        self.doctor_tree.column('Specialization', width=int(width * 0.4), minwidth=120)
        self.doctor_tree.column('Contact', width=int(width * 0.2), minwidth=80)
