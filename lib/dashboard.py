import tkinter as tk
from tkinter import filedialog, messagebox
from controller import (
    select_files, remove_items_from_list, move_item_up, move_item_down,
    play_files_sequentially, start_key_logger_with_filename, get_playback_config,
    filter_clicks, compare_json_files, compare_clicks, load_json, get_time_stats
)

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

# New function to play selected actions
def play_selected_actions():
    filenames = file_listbox.get(0, tk.END)
    if not filenames:
        return
    
    config = get_playback_config()
    play_files_sequentially(filenames, **config)
    print("All actions have been played.")

# New function to compare selected JSON files
def compare_selected_json(filtered=True):
    selected_files = file_listbox.curselection()
    if len(selected_files) == 2:
        file1 = file_listbox.get(selected_files[0])
        file2 = file_listbox.get(selected_files[1])

        # Load JSON data from the selected files
        data1 = load_json(file1)
        data2 = load_json(file2)
        
        if filtered:  # If filter is true
            # Filter out only click entries
            data1 = filter_clicks(data1)
            data2 = filter_clicks(data2)

        # Compare the data
        if filtered:
            result = compare_clicks(data1, data2)
        else:
            result = compare_json_files(file1, file2)
        return result
    else:
        print("Please select exactly 2 files to compare.")

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

# Create widgets and layout
def create_widgets(root):
    global stats_text
    stats_text = tk.Text(root, width=50, height=10, state=tk.DISABLED)
    stats_text.pack(pady=10)

# Main application window
root = tk.Tk()
root.title("Dashboard")

file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100, height=15)
file_listbox.pack(pady=10)

add_files_button = tk.Button(root, text="Add JSON Files", command=add_files)
remove_files_button = tk.Button(root, text="Remove Selected", command=remove_selected)
move_up_button = tk.Button(root, text="Move Up", command=move_up)
move_down_button = tk.Button(root, text="Move Down", command=move_down)
play_record_button = tk.Button(root, text="Play Selected Actions", command=play_selected_actions)
start_record_button = tk.Button(root, text="Start Key Logger", command=start_key_logger_with_filename)

compare_json_button = tk.Button(root, text="Compare Selected JSON", command=compare_selected_json)
time_stats_button = tk.Button(root, text="Show Time Statistics", command=display_time_stats)

# Pack the buttons into the window
add_files_button.pack(pady=5)
remove_files_button.pack(pady=5)
move_up_button.pack(pady=5)
move_down_button.pack(pady=5)
play_record_button.pack(pady=20)
start_record_button.pack(pady=20)
compare_json_button.pack(pady=5)
time_stats_button.pack(pady=5)

# Create a permanent stats display frame
create_widgets(root)

root.mainloop()