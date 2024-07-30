import tkinter as tk
from tkinter import filedialog, simpledialog
from controller import run_key_logger, check_and_run_actions
from locate import get_starting_position
import os

def select_files():
    recordings_dir = os.path.join(os.path.dirname(__file__), 'recordings')
    filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
    filenames = filedialog.askopenfilenames(title="Select JSON files", initialdir=recordings_dir, filetypes=filetypes)
    return filenames

def play_selected_actions():
    filenames = select_files()
    if not filenames:
        return
    
    # Get parameters from the user
    path_type = simpledialog.askstring("Input", "Enter path type:", initialvalue='spline')
    vary_coords_str = simpledialog.askstring("Input", "Vary coordinates? (yes/no)", initialvalue='yes')
    vary_coords = vary_coords_str.lower() in ['yes', 'true', '1']
    variation = simpledialog.askfloat("Input", "Enter variation:", initialvalue=0.05)
    delay = simpledialog.askfloat("Input", "Enter delay between actions:", initialvalue=2)
    check_type = simpledialog.askstring("Input", "Enter check type:", initialvalue='subscribe')
    
    # Prepare actions with parameters
    actions_with_params = [(filename, {'path_type': path_type, 'vary_coords': vary_coords, 'variation': variation, 'delay': delay}) for filename in filenames]

    locations = [
    {
        "edit": ["edit.png", "edit.PNG"]
    },
    {
        "subscribe": ["subscribe.PNG", "like.PNG", "icon_yt.PNG"]
    },
    {
        "menu": ["menu_image1.png", "menu_image2.png"]
    }
]
    check_and_run_actions(get_starting_position, locations, actions_with_params, check_type)

def start_key_logger_with_filename():
    output_filename = simpledialog.askstring("Input", "Enter filename for recording:", initialvalue='default_name')
    if output_filename:
        run_key_logger(output_filename)
        
# Create the main application window
root = tk.Tk()
root.title("Tkinter with PyAutoGUI")

# Create buttons for the functions
start_record_button = tk.Button(root, text="Start Key Logger", command=start_key_logger_with_filename)
play_record_button = tk.Button(root, text="Play Selected Actions", command=play_selected_actions)

# Pack the buttons into the window
start_record_button.pack(pady=20)
play_record_button.pack(pady=20)

# Start the main event loop
root.mainloop()