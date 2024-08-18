import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from controller import (
    select_files, remove_items_from_list, move_item_up, move_item_down,
    play_files_sequentially, start_key_logger_with_filename, get_playback_config,
    filter_clicks, load_json, get_time_stats, 
    process_repeated_sequences, process_shannon_entropy,
    get_repeated_sequences_detailed, merge_selected_json_files, plot_autocorrelation_from_file,
    cluster, opt_clusters, compare_entries
)
import numpy as np

def add_files():
    filenames = select_files()
    for filename in filenames:
        file_listbox.insert(tk.END, filename)

def remove_selected():
    items = list(file_listbox.get(0, tk.END))
    selected_indices = file_listbox.curselection()
    new_items = remove_items_from_list(items, selected_indices)
    file_listbox.delete(0, tk.END)
    for item in new_items:
        file_listbox.insert(tk.END, item)

def move_up():
    items = list(file_listbox.get(0, tk.END))
    selected_indices = file_listbox.curselection()
    new_items = move_item_up(items, selected_indices)
    file_listbox.delete(0, tk.END)
    for item in new_items:
        file_listbox.insert(tk.END, item)
    for index in selected_indices:
        if index > 0:
            file_listbox.selection_set(index - 1)

def move_down():
    items = list(file_listbox.get(0, tk.END))
    selected_indices = file_listbox.curselection()
    new_items = move_item_down(items, selected_indices)
    file_listbox.delete(0, tk.END)
    for item in new_items:
        file_listbox.insert(tk.END, item)
    for index in selected_indices:
        if index < len(new_items) - 1:
            file_listbox.selection_set(index + 1)

def play_selected_actions():
    filenames = file_listbox.get(0, tk.END)
    if not filenames:
        return
    
    config = get_playback_config()
    play_files_sequentially(filenames, **config)
    print("All actions have been played.")

def compare_selected_json():
    selected_files = file_listbox.curselection()
    if len(selected_files) == 2:
        file1 = file_listbox.get(selected_files[0])
        file2 = file_listbox.get(selected_files[1])

        try:
            # Load JSON data from the selected files
            data1 = load_json(file1)
            data2 = load_json(file2)
            
            # Apply filtering by default
            data1 = filter_clicks(data1)
            data2 = filter_clicks(data2)

            # Check for discrepancies in number of entries
            if len(data1) != len(data2):
                messagebox.showinfo("Warning", f"Files have different number of entries: {len(data1)} vs {len(data2)}")

            # Compare the entries
            differences = compare_entries(data1, data2, compare_time=time_var.get(), compare_color=color_var.get(), compare_position=pos_var.get())
            
            num_differences = len(differences)
            result_summary = f"Differences found in {num_differences} entries:\n\n"
            result_details = "\n".join(differences) if differences else "No differences found."

            # Update the stats display window
            stats_text.config(state=tk.NORMAL)
            stats_text.delete(1.0, tk.END)
            stats_text.insert(tk.END, result_summary + result_details + "\n")
            stats_text.config(state=tk.DISABLED)
            
        except FileNotFoundError:
            messagebox.showerror("Error", "One or both files not found.")
    else:
        messagebox.showerror("Error", "Please select exactly 2 files to compare.")

def display_time_stats():
    selected_files = file_listbox.curselection()
    if len(selected_files) != 1:
        messagebox.showerror("Error", "Please select exactly one file to analyze.")
        return

    file_path = file_listbox.get(selected_files[0])
    ignore_moves = messagebox.askyesno("Ignore Moves", "Ignore move actions?")

    try:
        result = get_time_stats(file_path, ignore_moves)
        if result is None:
            messagebox.showerror("Error", "Failed to compute time statistics.")
            return

        min_time, max_time, avg_time, std_time = result

        # Update the stats display window
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, tk.END)
        stats_text.insert(tk.END, f"Min time between actions: {min_time:.3f} seconds\n")
        stats_text.insert(tk.END, f"Max time between actions: {max_time:.3f} seconds\n")
        stats_text.insert(tk.END, f"Average time between actions: {avg_time:.3f} seconds\n")
        stats_text.insert(tk.END, f"Standard deviation: {std_time:.3f} seconds\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def analyze_repeated_sequences():
    selected_files = file_listbox.curselection()
    if len(selected_files) != 1:
        messagebox.showerror("Error", "Please select exactly one file to analyze.")
        return

    file_path = file_listbox.get(selected_files[0])
    repetitions = simpledialog.askinteger("Repetitions", "Enter number of repetitions:", minvalue=1, maxvalue=100)
    if repetitions is None:
        return

    try:
        # Count the number of repeated sequences
        repeated_sequence_count = process_repeated_sequences(file_path, repetitions)

        # Update the stats display window
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, tk.END)
        stats_text.insert(tk.END, f"Number of repeated sequences across {repetitions} repetitions: {repeated_sequence_count}\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_repeated_sequences_detailed():
    selected_files = file_listbox.curselection()
    if len(selected_files) != 1:
        messagebox.showerror("Error", "Please select exactly one file to analyze.")
        return

    file_path = file_listbox.get(selected_files[0])
    repetitions = simpledialog.askinteger("Repetitions", "Enter number of repetitions:", minvalue=1, maxvalue=100)
    if repetitions is None:
        return

    try:
        # Get the detailed repeated sequences
        repeated_sequences = get_repeated_sequences_detailed(file_path, repetitions)

        # Update the stats display window
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, tk.END)
        for seq, positions in repeated_sequences.items():
            stats_text.insert(tk.END, f"Sequence: {seq}\nPositions: {positions}\n\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_shannon_entropy():
    selected_files = file_listbox.curselection()
    if len(selected_files) != 1:
        messagebox.showerror("Error", "Please select exactly one file to analyze.")
        return

    file_path = file_listbox.get(selected_files[0])

    try:
        shannon_entropy_value = process_shannon_entropy(file_path)

        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, tk.END)
        stats_text.insert(tk.END, f"Shannon Entropy of the selected file: {shannon_entropy_value:.3f}\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def merge_json_files_action():
    # Get selected files from the listbox
    selected_files = file_listbox.curselection()
    if len(selected_files) < 2:  # Ensure at least two files are selected for merging
        messagebox.showerror("Error", "Please select at least two files to merge.")
        return

    # Get the filenames from the selected indices
    filenames = [file_listbox.get(i) for i in selected_files]

    # Ask the user for an output filename
    output_filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if not output_filename:
        return

    # Call the controller function to merge the selected files
    success = merge_selected_json_files(filenames, output_filename)
    
    if success:
        messagebox.showinfo("Success", f"Merged JSON files into {output_filename}")
    else:
        messagebox.showerror("Error", "An error occurred while merging files.")

def plot_autocorrelation_for_selected():
    selected_files = file_listbox.curselection()
    if len(selected_files) != 1:
        messagebox.showerror("Error", "Please select exactly one file to plot autocorrelation.")
        return

    file_path = file_listbox.get(selected_files[0])
    repetitions = simpledialog.askinteger("Repetitions", "Enter number of repetitions:", minvalue=1, maxvalue=100)
    if repetitions is None:
        return

    try:
        autocorrelation_metric = plot_autocorrelation_from_file(file_path, repetitions)
        
        # Display the results in the stats text box
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, tk.END)
        stats_text.insert(tk.END, f"Autocorrelation Results for {file_path} with {repetitions} repetitions:\n")
        stats_text.insert(tk.END, f"Autocorrelation Metric: {autocorrelation_metric:.2f}\n")
        stats_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def perform_clustering():
    selected_files = file_listbox.curselection()
    if len(selected_files) != 1:
        messagebox.showerror("Error", "Please select exactly one file to analyze.")
        return

    file_path = file_listbox.get(selected_files[0])
    
    # Ask user for number of clusters
    n_clusters = simpledialog.askinteger("Number of Clusters", "Enter number of clusters (leave blank for auto):", minvalue=1, maxvalue=10, initialvalue=None)

    try:
        data = load_json(file_path)
        coordinates = np.array([event.get('pos') for event in data if event.get('type') == 'click'])

        if n_clusters is None:
            n_clusters = opt_clusters(coordinates)
            if n_clusters is None:
                messagebox.showerror("Error", "Could not determine optimal number of clusters.")
                return
        elif n_clusters < 1:
            messagebox.showerror("Error", "Number of clusters must be at least 1.")
            return

        # Perform clustering
        kmeans = cluster(coordinates, n_clusters)

        # Update the stats display window
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, tk.END)
        stats_text.insert(tk.END, f"Cluster centers:\n{kmeans.cluster_centers_}\n")
        stats_text.insert(tk.END, f"Labels:\n{kmeans.labels_}\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_mouse_wheel(event):
    # Scroll up or down depending on the mouse wheel movement
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Main application window
root = tk.Tk()
root.title("Dashboard")

# Create a frame for the left side (file list and buttons)
left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="both", expand=True)

canvas = tk.Canvas(left_frame)
scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)

# Add scrollable frame to canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

root.bind_all("<MouseWheel>", on_mouse_wheel)

# File Listbox
file_listbox = tk.Listbox(scrollable_frame, selectmode=tk.MULTIPLE, width=100, height=15)
file_listbox.pack(pady=10)

# Buttons
add_files_button = tk.Button(scrollable_frame, text="Add JSON Files", command=add_files)
remove_files_button = tk.Button(scrollable_frame, text="Remove Selected", command=remove_selected)
move_up_button = tk.Button(scrollable_frame, text="Move Up", command=move_up)
move_down_button = tk.Button(scrollable_frame, text="Move Down", command=move_down)
merge_json_button = tk.Button(scrollable_frame, text="Merge JSON Files", command=merge_json_files_action)
play_record_button = tk.Button(scrollable_frame, text="Play Selected Actions", command=play_selected_actions)
start_record_button = tk.Button(scrollable_frame, text="Start Key Logger", command=start_key_logger_with_filename)
repeated_sequences_button = tk.Button(scrollable_frame, text="Analyze Repeated Sequences", command=analyze_repeated_sequences)
compare_json_button = tk.Button(scrollable_frame, text="Compare Selected JSON", command=compare_selected_json)
time_stats_button = tk.Button(scrollable_frame, text="Show Time Statistics", command=display_time_stats)
shannon_entropy_button = tk.Button(scrollable_frame, text="Calculate Shannon Entropy", command=display_shannon_entropy)
detailed_sequences_button = tk.Button(scrollable_frame, text="View Repeated Sequences", command=display_repeated_sequences_detailed)
autocorrelation_button = tk.Button(scrollable_frame, text="Plot Autocorrelation", command=plot_autocorrelation_for_selected)
clustering_button = tk.Button(scrollable_frame, text="Cluster Coordinates", command=perform_clustering)

# Pack buttons into scrollable frame
add_files_button.pack(pady=5)
remove_files_button.pack(pady=5)
move_up_button.pack(pady=5)
move_down_button.pack(pady=5)
merge_json_button.pack(pady=5)
play_record_button.pack(pady=20)
start_record_button.pack(pady=20)
compare_json_button.pack(pady=20)
time_stats_button.pack(pady=20)
repeated_sequences_button.pack(pady=5)
detailed_sequences_button.pack(pady=5)
shannon_entropy_button.pack(pady=20)
autocorrelation_button.pack(pady=20)
clustering_button.pack(pady=20)

# Create a frame for the display area (right side)
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True)

# Create a Text widget for displaying stats (read-only mode)
stats_text = tk.Text(right_frame, wrap=tk.WORD, state=tk.DISABLED)
stats_text.pack(side="left", fill="both", expand=True)

# Create a scrollbar for the Text widget
text_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=stats_text.yview)
text_scrollbar.pack(side="right", fill="y")

# Configure the Text widget to use the scrollbar
stats_text.configure(yscrollcommand=text_scrollbar.set)

# Create checkboxes for comparison options
comparison_frame = tk.LabelFrame(left_frame, text="Comparison Options", padx=10, pady=10)
comparison_frame.pack(pady=10)

time_var = tk.BooleanVar(value=False)
color_var = tk.BooleanVar(value=False)
pos_var = tk.BooleanVar(value=False)

tk.Checkbutton(comparison_frame, text="Compare Time", variable=time_var).pack(anchor="w")
tk.Checkbutton(comparison_frame, text="Compare Color", variable=color_var).pack(anchor="w")
tk.Checkbutton(comparison_frame, text="Compare Position", variable=pos_var).pack(anchor="w")

# Running the main application loop
root.mainloop()