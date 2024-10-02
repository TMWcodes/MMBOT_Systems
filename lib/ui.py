import tkinter as tk
from tkinter import ttk

def setup_ui(root, handlers):
    root.title("Dashboard")

    # Create a frame for the left side (file list and buttons)
    left_frame = tk.Frame(root)
    left_frame.pack(side="left", fill="both", expand=True)

    # Canvas for scrollable area
    canvas = tk.Canvas(left_frame)
    scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Configure canvas to update scroll region
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Add scrollable frame to canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Enable scrolling with the mouse wheel on Windows
    def _on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    # Bind mouse wheel event to canvas
    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    # File Listbox
    file_listbox = tk.Listbox(scrollable_frame, selectmode=tk.MULTIPLE, width=100, height=15)
    file_listbox.pack(pady=10)

    # File Operation Buttons
    tk.Button(scrollable_frame, text="Add JSON Files", command=handlers['add_files']).pack(pady=5)
    tk.Button(scrollable_frame, text="Remove Selected", command=handlers['remove_selected']).pack(pady=5)
    tk.Button(scrollable_frame, text="Move Up", command=handlers['move_up']).pack(pady=5)
    tk.Button(scrollable_frame, text="Move Down", command=handlers['move_down']).pack(pady=5)
    tk.Button(scrollable_frame, text="Merge Files", command=handlers['merge_json_files_action']).pack(pady=5)
    # Add the new button for displaying JSON data
    tk.Button(scrollable_frame, text="Display JSON", command=handlers['load_and_display_json']).pack(pady=5)
    tk.Button(scrollable_frame, text="Compare Selected JSON", command=handlers['compare_selected_json']).pack(pady=5)

    # Play/Record buttons
    tk.Button(scrollable_frame, text="Start Key Logger", command=handlers['start_key_logger_with_filename']).pack(pady=5)
    tk.Button(scrollable_frame, text="Play Selected Actions", command=handlers['play_selected_actions']).pack(pady=5)

    # Comparison Options
    comparison_frame = tk.LabelFrame(left_frame, text="Comparison Options", padx=10, pady=10)
    comparison_frame.pack(pady=10)

    time_var = tk.BooleanVar(value=False)
    color_var = tk.BooleanVar(value=False)
    pos_var = tk.BooleanVar(value=False)

    tk.Checkbutton(comparison_frame, text="Compare Time", variable=time_var).pack(anchor="w")
    tk.Checkbutton(comparison_frame, text="Compare Color", variable=color_var).pack(anchor="w")
    tk.Checkbutton(comparison_frame, text="Compare Position", variable=pos_var).pack(anchor="w")

    # Analysis Buttons
    tk.Button(scrollable_frame, text="Show Time Statistics", command=handlers['display_time_stats']).pack(pady=5)
    tk.Button(scrollable_frame, text="Calculate Shannon Entropy", command=handlers['display_shannon_entropy']).pack(pady=5)
    tk.Button(scrollable_frame, text="Analyze and View Repeated Sequences", command=handlers['analyze_and_display_repeated_sequences']).pack(pady=5)
   
    tk.Button(scrollable_frame, text="Plot Autocorrelation", command=handlers['plot_autocorrelation_for_selected']).pack(pady=5)
    tk.Button(scrollable_frame, text="Cluster Coordinates", command=handlers['perform_clustering']).pack(pady=5)

    

    # Create a frame for the display area (right side) and Notebook (Tabbed Interface)
    right_frame = tk.Frame(root)
    right_frame.pack(side="right", fill="both", expand=True)

    notebook = ttk.Notebook(right_frame)
    notebook.pack(expand=True, fill="both")

    # Create Frames for each tab
    table_tab = ttk.Frame(notebook)
    stats_tab = ttk.Frame(notebook)

    notebook.add(table_tab, text="Table View")
    notebook.add(stats_tab, text="Statistics")

    table_tree = ttk.Treeview(table_tab)

    # Define the columns
    table_tree['columns'] = ('time', 'type', 'button', 'pos', 'color')

    # Format the columns
    table_tree.column("#0", width=0, stretch=tk.NO)  # Hidden index column
    table_tree.column("time", anchor=tk.W, width=100)
    table_tree.column("type", anchor=tk.W, width=100)
    table_tree.column("button", anchor=tk.W, width=100)
    table_tree.column("pos", anchor=tk.W, width=150)
    table_tree.column("color", anchor=tk.W, width=150)

    # Define headings
    table_tree.heading("#0", text="", anchor=tk.W)  # Hidden index column
    table_tree.heading("time", text="Time", anchor=tk.W)
    table_tree.heading("type", text="Type", anchor=tk.W)
    table_tree.heading("button", text="Button", anchor=tk.W)
    table_tree.heading("pos", text="Position", anchor=tk.W)
    table_tree.heading("color", text="Color", anchor=tk.W)

    # Add the Treeview to the table_tab with a scrollbar
    table_tree.pack(fill="both", expand=True)

    # Add stats_text to stats_tab
    stats_text = tk.Text(stats_tab, wrap=tk.WORD, state=tk.DISABLED)
    stats_text.pack(side="left", fill="both", expand=True)

    text_scrollbar = ttk.Scrollbar(stats_tab, orient="vertical", command=stats_text.yview)
    text_scrollbar.pack(side="right", fill="y")
    stats_text.configure(yscrollcommand=text_scrollbar.set)

    return file_listbox, table_tree, stats_text, time_var, color_var, pos_var
