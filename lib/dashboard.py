import tkinter as tk
import pyautogui
import time
# # Create a function to move the mouse when the button is clicked
def move_mouse():
    print("starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
        time.sleep(1)
    print("Go")

    root.after(0, pyautogui.moveTo, 500, 500)  # Move the mouse after a small delay
# # Create the main application window
root = tk.Tk()
root.title("Tkinter with PyAutoGUI")
# # Create a button widget
button = tk.Button(root, text="Move Mouse", command=move_mouse)
button.pack()
# # Start the main event loop
root.mainloop()
