import tkinter as tk
from tkinter import filedialog, simpledialog
from controller import run_key_logger, playActions
from locate import get_starting_position
import os
import time

def select_files():
    recordings_dir = os.path.join(os.path.dirname(__file__), 'recordings')
    filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
    filenames = filedialog.askopenfilenames(title="Select JSON files", initialdir=recordings_dir, filetypes=filetypes)
    for filename in filenames:
        file_listbox.insert(tk.END, filename)

def remove_selected():
    selected_indices = file_listbox.curselection()
    for index in reversed(selected_indices):
        file_listbox.delete(index)

def move_up():
    selected_indices = file_listbox.curselection()
    for index in selected_indices:
        if index == 0:
            continue
        filename = file_listbox.get(index)
        file_listbox.delete(index)
        file_listbox.insert(index-1, filename)
        file_listbox.selection_set(index-1)

def move_down():
    selected_indices = file_listbox.curselection()
    for index in reversed(selected_indices):
        if index == file_listbox.size()-1:
            continue
        filename = file_listbox.get(index)
        file_listbox.delete(index)
        file_listbox.insert(index+1, filename)
        file_listbox.selection_set(index+1)

def play_files_sequentially(filenames, path_type, vary_coords, variation, delay, loop_reps):
    for _ in range(loop_reps):
        for filename in filenames:
            playActions(filename, path_type=path_type, vary_coords=vary_coords, variation=variation)
            time.sleep(delay)  # Wait for the specified delay before playing the next file

def play_selected_actions():
    filenames = file_listbox.get(0, tk.END)
    if not filenames:
        return
    
    # Get parameters from the user
    path_type = simpledialog.askstring("Input", "Enter path type:", initialvalue='spline')
    vary_coords_str = simpledialog.askstring("Input", "Vary coordinates? (yes/no)", initialvalue='yes')
    vary_coords = vary_coords_str.lower() in ['yes', 'true', '1']
    variation = simpledialog.askfloat("Input", "Enter variation:", initialvalue=0.05)
    delay = simpledialog.askfloat("Input", "Enter delay between actions:", initialvalue=2)
    loop_reps = simpledialog.askinteger("Input", "Enter number of times to loop:", initialvalue=1)  # Default to 1 loop

    play_files_sequentially(filenames, path_type, vary_coords, variation, delay, loop_reps)
    
    print("All actions have been played.")

    # # Play each file in the order selected by the user
    # for filename in filenames:
    #     playActions(filename, path_type=path_type, vary_coords=vary_coords, variation=variation)
    #     time.sleep(delay)  # Delay between playing each file

def start_key_logger_with_filename():
    output_filename = simpledialog.askstring("Input", "Enter filename for recording:", initialvalue='default_name')
    if output_filename:
        run_key_logger(output_filename)

# Create the main application window
root = tk.Tk()
root.title("Tkinter with PyAutoGUI")

# Create listbox to show selected files
file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100, height=15)
file_listbox.pack(pady=10)

# Create buttons for the functions
add_files_button = tk.Button(root, text="Add JSON Files", command=select_files)
remove_files_button = tk.Button(root, text="Remove Selected", command=remove_selected)
move_up_button = tk.Button(root, text="Move Up", command=move_up)
move_down_button = tk.Button(root, text="Move Down", command=move_down)
play_record_button = tk.Button(root, text="Play Selected Actions", command=play_selected_actions)
start_record_button = tk.Button(root, text="Start Key Logger", command=start_key_logger_with_filename)

# Pack the buttons into the window
add_files_button.pack(pady=5)
remove_files_button.pack(pady=5)
move_up_button.pack(pady=5)
move_down_button.pack(pady=5)
play_record_button.pack(pady=20)
start_record_button.pack(pady=20)

# Start the main event loop
root.mainloop()