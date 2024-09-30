import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from controller import (
    play_files_sequentially, start_key_logger_with_filename, get_playback_config_window,
    json_to_dataframe
)
import numpy as np
import os
from file_operations import add_files, remove_selected, move_down, move_up, merge_json_files_action
from ui import setup_ui
from data_processing import (
    compare_selected_json, display_time_stats, analyze_repeated_sequences,
    display_repeated_sequences_detailed, display_shannon_entropy, 
    plot_autocorrelation_for_selected, perform_clustering
)

def play_selected_actions(root):
    filenames = file_listbox.get(0, tk.END)
    if not filenames:
        return

    config = get_playback_config_window(root)
    
    # Assume the files could be from either recordings or log_records
    # Append directory paths based on file naming conventions or user selection
    base_dirs = ['recordings', 'log_records']
    full_paths = []

    for filename in filenames:
        for base_dir in base_dirs:
            # Check if the file exists in one of the directories
            potential_path = f"{base_dir}/{filename}"
            if os.path.exists(potential_path):  # Use a quick check here; you may need to adjust this
                full_paths.append(potential_path)
                break
        else:
            # If file is not found in the base directories, show an error
            messagebox.showerror("Error", f"File not found in any of the expected directories: {filename}")
            return

    play_files_sequentially(full_paths, **config)
    print("All actions have been played.")


def on_mouse_wheel(event):
    # Scroll up or down depending on the mouse wheel movement
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def display_dataframe_in_treeview(df, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(parent_frame)
    tree.pack(expand=True, fill='both')

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Function to load and display JSON data
def load_and_display_json(table_tree):
    selected_files = file_listbox.curselection()
    
    if not selected_files:
        messagebox.showwarning("No selection", "Please select a file from the list.")
        return
    
    for item in table_tree.get_children():
        table_tree.delete(item)
    
    for index in selected_files:
        json_file = file_listbox.get(index)
        
        try:
            df = json_to_dataframe(json_file)
            display_dataframe_in_treeview(df, table_tree)
        
        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
###


def main():
    global file_listbox, stats_text, time_var, color_var, pos_var, table_tree

    root = tk.Tk()

    # Define handlers to pass to the UI setup
    handlers = {
        'add_files': lambda: add_files(file_listbox),
        'remove_selected': lambda: remove_selected(file_listbox),
        'move_up': lambda: move_up(file_listbox),
        'move_down': lambda: move_down(file_listbox),
        'load_and_display_json': lambda: load_and_display_json(table_tree),

        'merge_json_files_action': lambda: merge_json_files_action(file_listbox),
        'start_key_logger_with_filename': lambda: start_key_logger_with_filename(root),
        'play_selected_actions': lambda: play_selected_actions(root),
        'compare_selected_json': lambda: compare_selected_json(
            file_listbox.get(file_listbox.curselection()[0]), 
            file_listbox.get(file_listbox.curselection()[1]), 
            time_var.get(), 
            color_var.get(), 
            pos_var.get(), 
            stats_text
        ),
         'display_time_stats': lambda: display_time_stats(
            file_listbox.get(file_listbox.curselection()[0]), 
            messagebox.askyesno("Ignore Moves", "Ignore move actions?"), 
            stats_text  # This will be the Text widget where stats will be displayed
        ),
        'display_shannon_entropy': lambda: display_shannon_entropy(file_listbox.get(file_listbox.curselection()[0]), 
                                                                   stats_text),
        'analyze_repeated_sequences': lambda: analyze_repeated_sequences(file_listbox.get(file_listbox.curselection()[0]), 
                                                                           simpledialog.askinteger("Repetitions", "Enter number of repetitions:", minvalue=1, maxvalue=100),
                                                                           stats_text),
        'display_repeated_sequences_detailed': lambda: display_repeated_sequences_detailed(file_listbox.get(file_listbox.curselection()[0]), 
                                                                                          simpledialog.askinteger("Repetitions", "Enter number of repetitions:", minvalue=1, maxvalue=100),
                                                                                          stats_text),
        
        
        'plot_autocorrelation_for_selected': lambda: plot_autocorrelation_for_selected(file_listbox.get(file_listbox.curselection()[0]), 
                                                                                       simpledialog.askinteger("Repetitions", "Enter number of repetitions:", minvalue=1, maxvalue=100),
                                                                                       stats_text),
        'perform_clustering': lambda: perform_clustering(file_listbox.get(file_listbox.curselection()[0]), 
                                                         simpledialog.askinteger("Number of Clusters", "Enter number of clusters (leave blank for auto):", minvalue=1, maxvalue=10, initialvalue=None),
                                                         stats_text)
    }

    file_listbox, table_tree, stats_text, time_var, color_var, pos_var = setup_ui(root, handlers)

    root.mainloop()
if __name__ == "__main__":
    main()

