import tkinter as tk
from tkinter import ttk, messagebox

class PatientsTab:
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
        form_frame = ttk.LabelFrame(self.parent, text="Patient Information", padding=15)
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        tree_frame = ttk.LabelFrame(self.parent, text="Patients List", padding=15)
        tree_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        # Configure form frame grid
        form_frame.grid_columnconfigure(1, weight=1)
        for i in range(10):  # Approximate number of rows
            form_frame.grid_rowconfigure(i, weight=1)
            
        # Configure tree frame grid
        tree_frame.grid_rowconfigure(1, weight=1)  # TreeView gets all extra space
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Patient Information Form
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
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        # Add buttons
        ttk.Button(buttons_frame, text="Add", command=self.add_patient).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Update", command=self.update_patient).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Delete", command=self.delete_patient).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)
        
        # Create Treeview with scrollbars
        tree_container = ttk.Frame(tree_frame)
        tree_container.grid(row=1, column=0, sticky='nsew')
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_container,
                                columns=('ID', 'Name', 'DOB'),
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
        self.tree.heading('Name', text='Name')
        self.tree.heading('DOB', text='Date of Birth')
        
        # Set column weights
        total_width = tree_container.winfo_width()
        self.tree.column('ID', width=int(total_width * 0.1), minwidth=50)
        self.tree.column('Name', width=int(total_width * 0.2), minwidth=100)
        self.tree.column('DOB', width=int(total_width * 0.15), minwidth=80)
        
        # Bind select event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Bind resize event to adjust column widths
        tree_container.bind('<Configure>', self.on_tree_resize)
        
        # Initial refresh
        self.refresh_list()

    def clear_form(self):
        self.patient_id.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.dob.delete(0, tk.END)

    def add_patient(self):
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        dob = self.dob.get()
        
        if not all([first_name, last_name, dob]):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        query = """INSERT INTO patients (first_name, last_name, date_of_birth)
                   VALUES (%s, %s, %s)"""
        params = (first_name, last_name, dob)
        
        result = self.db_manager.execute_query('patients_db', query, params)
        if result:
            messagebox.showinfo("Success", "Patient added successfully!")
            self.clear_form()
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Failed to add patient!")

    def update_patient(self):
        patient_id = self.patient_id.get()
        if not patient_id:
            messagebox.showerror("Error", "Please select a patient to update!")
            return
            
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        dob = self.dob.get()
        
        query = """UPDATE patients 
                   SET first_name = %s, last_name = %s, date_of_birth = %s
                   WHERE patient_id = %s"""
        params = (first_name, last_name, dob, patient_id)
        
        result = self.db_manager.execute_query('patients_db', query, params)
        if result is not None:
            messagebox.showinfo("Success", "Patient updated successfully!")
            self.clear_form()
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Failed to update patient!")

    def delete_patient(self):
        patient_id = self.patient_id.get()
        if not patient_id:
            messagebox.showerror("Error", "Please select a patient to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
            query = "DELETE FROM patients WHERE patient_id = %s"
            result = self.db_manager.execute_query('patients_db', query, (patient_id,))
            
            if result is not None:
                messagebox.showinfo("Success", "Patient deleted successfully!")
                self.clear_form()
                self.refresh_list()
            else:
                messagebox.showerror("Error", "Failed to delete patient!")

    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)['values']
            if values:
                self.patient_id.delete(0, tk.END)
                self.patient_id.insert(0, values[0])
                self.first_name.delete(0, tk.END)
                self.first_name.insert(0, values[1].split()[0])
                self.last_name.delete(0, tk.END)
                self.last_name.insert(0, values[1].split()[1])
                self.dob.delete(0, tk.END)
                self.dob.insert(0, values[2])

    def refresh_list(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get patients from database
        query = "SELECT patient_id, first_name, last_name, date_of_birth FROM patients"
        result = self.db_manager.execute_query('patients_db', query)
        
        if result:
            for patient in result:
                self.tree.insert('', 'end', values=(
                    patient[0],
                    f"{patient[1]} {patient[2]}",
                    patient[3]
                ))

    def on_tree_resize(self, event):
        # Adjust column widths based on container width
        width = event.width
        self.tree.column('ID', width=int(width * 0.1), minwidth=50)
        self.tree.column('Name', width=int(width * 0.2), minwidth=100)
        self.tree.column('DOB', width=int(width * 0.15), minwidth=80)
