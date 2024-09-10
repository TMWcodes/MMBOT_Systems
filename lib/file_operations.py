import tkinter as tk
from controller import select_files, remove_items_from_list, move_item_up, move_item_down

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
