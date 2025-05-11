import tkinter as tk
from tkinter import ttk
from models.database_manager import DatabaseManager
from ui.styles import configure_styles
from ui.tabs.patients_tab import PatientsTab
from ui.tabs.doctors_tab import DoctorsTab
from ui.tabs.appointments_tab import AppointmentsTab
from ui.tabs.billing_tab import BillingTab

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        
        # Configure window properties
        self.root.minsize(800, 600)
        self.root.configure(bg='#f5f6fa')
        
        # Make the window responsive
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Calculate initial window size (80% of screen)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.grid(row=0, column=0, sticky='nsew')
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Add a title frame
        title_frame = ttk.Frame(self.main_container)
        title_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=(20,0))
        title_frame.grid_columnconfigure(0, weight=1)
        
        # Add title label with responsive font size
        self.title_label = ttk.Label(title_frame, 
                                    text="Hospital Management System",
                                    font=('Segoe UI', 24, 'bold'),
                                    foreground='#2c3e50')
        self.title_label.grid(row=0, column=0, pady=10)
        
        # Add subtitle with responsive font size
        self.subtitle_label = ttk.Label(title_frame,
                                       text="Manage patients, appointments, and billing efficiently",
                                       font=('Segoe UI', 12),
                                       foreground='#7f8c8d')
        self.subtitle_label.grid(row=1, column=0, pady=(0,20))
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Configure modern styles
        configure_styles()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        
        # Create tabs with consistent styling and make them responsive
        self.patients_tab = ttk.Frame(self.notebook)
        self.doctors_tab = ttk.Frame(self.notebook)
        self.appointments_tab = ttk.Frame(self.notebook)
        self.billing_tab = ttk.Frame(self.notebook)
        
        # Configure tab grids
        for tab in [self.patients_tab, self.doctors_tab, self.appointments_tab, self.billing_tab]:
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)
        
        # Add tabs to notebook with descriptive text
        self.notebook.add(self.patients_tab, text="👥 Patients")
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Auto-refresh configuration
        self.refresh_interval = 5000  # 5 seconds
        self.tab_controllers = {}
        self.notebook.add(self.doctors_tab, text="👨‍⚕️ Doctors")
        self.notebook.add(self.appointments_tab, text="📅 Appointments")
        self.notebook.add(self.billing_tab, text="💰 Billing")
        
        # Initialize tab controllers
        self.patients = PatientsTab(self.patients_tab, self.db_manager)
        self.doctors = DoctorsTab(self.doctors_tab, self.db_manager)
        self.appointments = AppointmentsTab(self.appointments_tab, self.db_manager)
        self.billing = BillingTab(self.billing_tab, self.db_manager)
        
        # Store tab controllers for auto-refresh
        self.tab_controllers = {
            self.patients_tab: self.patients,
            self.doctors_tab: self.doctors,
            self.appointments_tab: self.appointments,
            self.billing_tab: self.billing
        }
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Start auto-refresh
        self.current_tab = self.patients_tab
        self.schedule_refresh()
    
    def on_tab_changed(self, event):
        self.current_tab = self.notebook.select()
        self.refresh_current_tab()
    
    def refresh_current_tab(self):
        current_controller = self.tab_controllers.get(self.current_tab)
        if current_controller and hasattr(current_controller, 'refresh_list'):
            current_controller.refresh_list()
        elif current_controller and hasattr(current_controller, 'refresh_appointments'):
            current_controller.refresh_appointments()
    
    def schedule_refresh(self):
        self.refresh_current_tab()
        self.root.after(self.refresh_interval, self.schedule_refresh)
    
    def on_window_resize(self, event):
        # Only handle window resize events, not other configure events
        if event.widget == self.root:
            # Calculate responsive font sizes
            window_width = event.width
            title_size = max(16, min(24, int(window_width / 50)))
            subtitle_size = max(10, min(14, int(window_width / 80)))
            
            # Update font sizes
            self.title_label.configure(font=('Segoe UI', title_size, 'bold'))
            self.subtitle_label.configure(font=('Segoe UI', subtitle_size))
            
            # Update padding based on window size
            base_padding = max(10, min(20, int(window_width / 60)))
            self.notebook.grid(padx=base_padding, pady=base_padding)

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Center the loading window
        width = 400
        height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configure the window
        self.root.configure(bg='#2c3e50')
        
        # Create a frame for content
        self.frame = ttk.Frame(root)
        self.frame.pack(expand=True, fill='both')
        
        # Add hospital icon
        title_label = ttk.Label(self.frame,
                               text="🏥",
                               font=('Segoe UI', 48),
                               foreground='#3498db')
        title_label.pack(pady=(40, 20))
        
        # Add loading text
        self.loading_label = ttk.Label(self.frame,
                                      text="Loading Hospital Management System",
                                      font=('Segoe UI', 14),
                                      foreground='#2c3e50')
        self.loading_label.pack(pady=10)
        
        # Add progress bar
        self.progress = ttk.Progressbar(self.frame, length=300, mode='determinate')
        self.progress.pack(pady=20)
        
        # Start loading animation
        self.progress_value = 0
        self.dots = 0
        self.animate()
    
    def animate(self):
        if self.progress_value < 100:
            self.progress_value += 2
            self.progress['value'] = self.progress_value
            
            # Animate loading dots
            self.dots = (self.dots + 1) % 4
            dots_text = '.' * self.dots
            self.loading_label['text'] = f"Loading Hospital Management System{dots_text}"
            
            self.root.after(50, self.animate)
        else:
            self.root.destroy()

def fade_in_window(window):
    alpha = 0
    window.attributes('-alpha', alpha)
    window.deiconify()
    
    def increase_opacity():
        nonlocal alpha
        if alpha < 1.0:
            alpha += 0.1
            window.attributes('-alpha', alpha)
            window.after(20, increase_opacity)
    
    increase_opacity()

def main():
    # Show loading screen
    loading_root = tk.Tk()
    loading_screen = LoadingScreen(loading_root)
    loading_root.mainloop()
    
    # Create main window
    root = tk.Tk()
    root.withdraw()  # Hide window initially
    
    # Initialize app
    app = HospitalManagementSystem(root)
    
    # Show window with fade effect
    fade_in_window(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
