from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Color scheme
    colors = {
        'primary': '#1a365d',    # Deep Navy Blue
        'secondary': '#718096',  # Professional Gray
        'background': '#f7fafc',  # Light Cool Gray
        'text': '#2d3748',       # Dark Gray Blue
        'accent': '#4a5568',     # Medium Gray Blue
        'border': '#e2e8f0',     # Light Gray Blue
        'hover': '#2c5282',      # Lighter Navy Blue
        'selected': '#2a4365',   # Darker Navy Blue
        'error': '#e74c3c',      # Red
        'white': '#ffffff',
        'light_gray': '#f8f9fa'
    }
    
    # Configure notebook (tabs)
    style.configure('TNotebook', background=colors['background'])
    style.configure('TNotebook.Tab',
                    padding=[15, 8],
                    font=('Arial', 10),
                    background=colors['primary'],
                    foreground=colors['white'])
    style.map('TNotebook.Tab',
              background=[('selected', colors['selected'])],
              foreground=[('selected', colors['white'])])
    
    # Configure frames
    style.configure('TFrame', background=colors['background'])
    style.configure('TLabelframe',
                    background=colors['white'],
                    padding=20)
    style.configure('TLabelframe.Label',
                    background=colors['white'],
                    foreground=colors['text'],
                    font=('Arial', 11, 'bold'))
    
    # Configure labels
    style.configure('TLabel',
                    background=colors['background'],
                    foreground=colors['text'],
                    font=('Arial', 10))
    
    # Configure entries and inputs
    style.configure('TEntry',
                    padding=8,
                    font=('Arial', 10),
                    background='white',
                    foreground=colors['text'],
                    insertbackground=colors['text'],
                    relief='solid',
                    borderwidth=1)
    style.map('TEntry',
              fieldbackground=[('focus', colors['white']),
                              ('!focus', colors['light_gray'])])
    
    # Configure buttons
    style.configure('TButton',
                    padding=[15, 8],
                    font=('Arial', 10, 'bold'),
                    background=colors['primary'],
                    foreground=colors['white'])
    style.map('TButton',
              background=[('active', colors['hover'])],
              foreground=[('active', colors['white'])])
    
    # Configure comboboxes
    style.configure('TCombobox',
                    padding=8,
                    font=('Arial', 10))
    
    # Configure treeview
    style.configure('Treeview',
                    font=('Arial', 10),
                    rowheight=28,
                    background='white',
                    fieldbackground='white',
                    foreground=colors['text'])
    style.configure('Treeview.Heading',
                    font=('Arial', 10, 'bold'),
                    background=colors['primary'],
                    foreground=colors['white'])
    style.map("Treeview",
              background=[("selected", colors['selected'])],
              foreground=[("selected", colors['white'])])
    
    # Configure scrollbars
    style.configure('Vertical.TScrollbar',
                    background=colors['background'],
                    troughcolor=colors['light_gray'],
                    width=16)
    style.configure('Horizontal.TScrollbar',
                    background=colors['background'],
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
                    background=colors['background'],
                    font=('Arial', 14),
                    foreground=colors['text'])
