import tkinter as tk
import time
import pyautogui
from main import fl_furnace

def move_mouse():
    print("Starting move_mouse", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
        time.sleep(1)
    print("Go")

    root.after(0, pyautogui.moveTo, 500, 500)

def furnace_button_click():
    print("Furnace button clicked")
    fl_furnace("silver ore")  # Replace "some_item" with the appropriate item

# Create the main application window
root = tk.Tk()
root.title("Tkinter with PyAutoGUI")

# Create buttons for move_mouse and fl_furnace functions
move_mouse_button = tk.Button(root, text="Move Mouse", command=move_mouse)
furnace_button = tk.Button(root, text="Furnace", command=furnace_button_click)

# Pack the buttons into the window
move_mouse_button.pack()
furnace_button.pack()

# Start the main event loop
root.mainloop()
