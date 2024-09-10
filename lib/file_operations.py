import tkinter as tk
from controller import select_files, remove_items_from_list, move_item_up, move_item_down, merge_selected_json_files
from tkinter import filedialog, messagebox
import os

def add_files(file_listbox):
    """
    Add files to the file_listbox using a file selection dialog.
    """
    filenames = select_files()
    for filename in filenames:
        file_listbox.insert(tk.END, filename)

def remove_selected(file_listbox):
    """
    Remove selected files from the file_listbox.
    """
    items = list(file_listbox.get(0, tk.END))
    selected_indices = file_listbox.curselection()
    new_items = remove_items_from_list(items, selected_indices)
    file_listbox.delete(0, tk.END)
    for item in new_items:
        file_listbox.insert(tk.END, item)

def move_up(file_listbox):
    """
    Move the selected file(s) up in the file_listbox.
    """
    items = list(file_listbox.get(0, tk.END))
    selected_indices = file_listbox.curselection()
    new_items = move_item_up(items, selected_indices)
    file_listbox.delete(0, tk.END)
    for item in new_items:
        file_listbox.insert(tk.END, item)
    for index in selected_indices:
        if index > 0:
            file_listbox.selection_set(index - 1)

def move_down(file_listbox):
    """
    Move the selected file(s) down in the file_listbox.
    """
    items = list(file_listbox.get(0, tk.END))
    selected_indices = file_listbox.curselection()
    new_items = move_item_down(items, selected_indices)
    file_listbox.delete(0, tk.END)
    for item in new_items:
        file_listbox.insert(tk.END, item)
    for index in selected_indices:
        if index < len(new_items) - 1:
            file_listbox.selection_set(index + 1)


def merge_json_files_action(file_listbox):
    # Get selected files from the listbox
    selected_files = file_listbox.curselection()
    if len(selected_files) < 2:  # Ensure at least two files are selected for merging
        messagebox.showerror("Error", "Please select at least two files to merge.")
        return

    # Get the filenames from the selected indices
    filenames = [file_listbox.get(i) for i in selected_files]

    # Define directories
    base_dir = os.path.dirname(__file__)
    recordings_dir = os.path.join(base_dir, 'recordings')
    log_records_dir = os.path.join(base_dir, 'log_records')

    # Update paths to the correct directories
    updated_filenames = []
    for filename in filenames:
        # Check in both directories
        filepath = os.path.join(recordings_dir, filename)
        if not os.path.isfile(filepath):
            filepath = os.path.join(log_records_dir, filename)
        if os.path.isfile(filepath):
            updated_filenames.append(filepath)
        else:
            messagebox.showerror("Error", f"File {filename} not found in both directories.")
            return

    # Ask the user for an output filename
    output_filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if not output_filename:
        return

    # Call the controller function to merge the selected files
    success = merge_selected_json_files(updated_filenames, output_filename)
    
    if success:
        messagebox.showinfo("Success", f"Merged JSON files into {output_filename}")
    else:
        messagebox.showerror("Error", "An error occurred while merging files.")
