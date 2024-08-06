import tkinter as tk
from tkinter import filedialog, simpledialog
from controller import run_key_logger, playActions
from locate import get_starting_position
from controller import (
    select_files, remove_files_from_listbox, move_up_in_listbox, move_down_in_listbox,
    play_files_sequentially, start_key_logger_with_filename
)
from data import filter_clicks, compare_json_files, compare_clicks, load_coordinates, load_json


def add_files():
    filenames = select_files()
    for filename in filenames:
        file_listbox.insert(tk.END, filename)

def remove_selected():
    remove_files_from_listbox(file_listbox)

def move_up():
    move_up_in_listbox(file_listbox)

def move_down():
    move_down_in_listbox(file_listbox)

def play_selected_actions():
    filenames = file_listbox.get(0, tk.END)
    if not filenames:
        return
    
    path_type = simpledialog.askstring("Input", "Enter path type:", initialvalue='spline')
    vary_coords_str = simpledialog.askstring("Input", "Vary coordinates? (yes/no)", initialvalue='yes')
    vary_coords = vary_coords_str.lower() in ['yes', 'true', '1']
    variation = simpledialog.askfloat("Input", "Enter variation:", initialvalue=0.05)
    delay = simpledialog.askfloat("Input", "Enter delay between actions:", initialvalue=2)
    loop_reps = simpledialog.askinteger("Input", "Enter number of times to loop:", initialvalue=1)

    play_files_sequentially(filenames, path_type, vary_coords, variation, delay, loop_reps)
    
    print("All actions have been played.")

# New function to compare selected JSON files
def compare_selected_json(filtered=True):
    selected_files = file_listbox.curselection()
    if len(selected_files) == 2:
        file1 = file_listbox.get(selected_files[0])
        file2 = file_listbox.get(selected_files[1])
        print(file1)
        print(file2)
        # Load JSON data from the selected files
        data1 = load_json(file1)
        data2 = load_json(file2)

        if filtered:
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
# Create the main application window
root = tk.Tk()
root.title("Tkinter with PyAutoGUI")

file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100, height=15)
file_listbox.pack(pady=10)

add_files_button = tk.Button(root, text="Add JSON Files", command=add_files)
remove_files_button = tk.Button(root, text="Remove Selected", command=remove_selected)
move_up_button = tk.Button(root, text="Move Up", command=move_up)
move_down_button = tk.Button(root, text="Move Down", command=move_down)
play_record_button = tk.Button(root, text="Play Selected Actions", command=play_selected_actions)
start_record_button = tk.Button(root, text="Start Key Logger", command=start_key_logger_with_filename)

# Button to compare selected JSON files
compare_json_button = tk.Button(root, text="Compare Selected JSON", command=compare_selected_json)

# Pack the buttons into the window
add_files_button.pack(pady=5)
remove_files_button.pack(pady=5)
move_up_button.pack(pady=5)
move_down_button.pack(pady=5)
play_record_button.pack(pady=20)
start_record_button.pack(pady=20)
compare_json_button.pack(pady=20)  # Add the compare button

root.mainloop()