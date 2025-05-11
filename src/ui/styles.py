from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Color scheme
    colors = {
        'primary': '#2980b9',    # Blue
        'secondary': '#f5f6fa',  # Light gray
        'accent': '#27ae60',     # Green
        'text': '#2c3e50',       # Dark gray
        'error': '#e74c3c',      # Red
        'white': '#ffffff',
        'light_gray': '#f8f9fa'
    }
    
    # Configure notebook (tabs)
    style.configure('TNotebook', background=colors['secondary'])
    style.configure('TNotebook.Tab',
                    padding=[15, 8],
                    font=('Segoe UI', 10),
                    background=colors['primary'],
                    foreground=colors['white'])
    style.map('TNotebook.Tab',
              background=[('selected', colors['accent'])],
              foreground=[('selected', colors['white'])])
    
    # Configure frames
    style.configure('TFrame', background=colors['secondary'])
    style.configure('TLabelframe',
                    background=colors['white'],
                    padding=20)
    style.configure('TLabelframe.Label',
                    background=colors['white'],
                    foreground=colors['text'],
                    font=('Segoe UI', 11, 'bold'))
    
    # Configure labels
    style.configure('TLabel',
                    background=colors['secondary'],
                    foreground=colors['text'],
                    font=('Segoe UI', 10))
    
    # Configure entries and inputs
    style.configure('TEntry',
                    padding=8,
                    font=('Segoe UI', 10))
    style.map('TEntry',
              fieldbackground=[('focus', colors['white']),
                              ('!focus', colors['light_gray'])])
    
    # Configure buttons
    style.configure('TButton',
                    padding=[15, 8],
                    font=('Segoe UI', 10, 'bold'),
                    background=colors['primary'],
                    foreground=colors['white'])
    style.map('TButton',
              background=[('active', colors['accent'])],
              foreground=[('active', colors['white'])])
    
    # Configure comboboxes
    style.configure('TCombobox',
                    padding=8,
                    font=('Segoe UI', 10))
    
    # Configure treeview
    style.configure('Treeview',
                    font=('Segoe UI', 10),
                    rowheight=30,
                    background=colors['white'],
                    fieldbackground=colors['white'],
                    foreground=colors['text'])
    style.configure('Treeview.Heading',
                    font=('Segoe UI', 10, 'bold'),
                    background=colors['primary'],
                    foreground=colors['white'])
    style.map("Treeview",
              background=[("selected", colors['accent'])],
              foreground=[("selected", colors['white'])])
    
    # Configure scrollbars
    style.configure('Vertical.TScrollbar',
                    background=colors['secondary'],
                    troughcolor=colors['light_gray'],
                    width=16)
    style.configure('Horizontal.TScrollbar',
                    background=colors['secondary'],
                    troughcolor=colors['light_gray'],
                    width=16)
    
    # Configure progress bar for loading screen
    style.configure('TProgressbar',
                    thickness=10,
                    background=colors['accent'],
                    troughcolor=colors['light_gray'])
    
    # Configure loading screen frame
    style.configure('Loading.TFrame',
                    background=colors['white'],
                    relief='raised',
                    borderwidth=2)
    
    # Configure loading screen labels
    style.configure('Loading.TLabel',
                    background=colors['white'],
                    font=('Segoe UI', 14),
                    foreground=colors['text'])

