import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
from data import compute_click_time_stats
from controller import (
    load_json, filter_clicks, compare_entries, 
    process_repeated_sequences, process_shannon_entropy,
    get_repeated_sequences_detailed, plot_autocorrelation_from_file, 
    cluster, opt_clusters
)


# Compare two JSON files
def compare_selected_json(file1, file2, time_var, color_var, pos_var, stats_text):
    # Check if both files are selected
    if not file1 or not file2:
        messagebox.showwarning("Selection Error", "Please select two files.")
        return

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
        differences = compare_entries(data1, data2, compare_time=time_var, compare_color=color_var, compare_position=pos_var)
        num_differences = len(differences)
        
        # Adding file names to the output
        result_summary = f"File 1 is {file1}\nFile 2 is {file2}\n\nDifferences found in {num_differences} entries:\n\n"
        result_details = "\n".join(differences) if differences else "No differences found."

        # Update the stats display window
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, "end")
        stats_text.insert("end", result_summary + result_details + "\n")
        stats_text.config(state=tk.DISABLED)
        
    except FileNotFoundError:
        messagebox.showerror("Error", "One or both files not found.")

# Display time statistics
def display_time_stats(file_path, ignore_moves, stats_text):
    try:
        # Directly call compute_click_time_stats
        click_stats, mousedown_stats = compute_click_time_stats(file_path)

        if click_stats is None or mousedown_stats is None:
            messagebox.showerror("Error", "Failed to compute time statistics.")
            return
        
        # Unpack the results
        (min_click, max_click, avg_click, std_click) = click_stats
        (min_mousedown, max_mousedown, avg_mousedown, std_mousedown) = mousedown_stats

        # Update the stats display window
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, "end")

        # Insert the statistics into the text widget
        stats_text.insert("end", "MouseDown to MouseUp Stats:\n")
        stats_text.insert("end", f"Min time: {min_click:.3f} seconds\n")
        stats_text.insert("end", f"Max time: {max_click:.3f} seconds\n")
        stats_text.insert("end", f"Average time: {avg_click:.3f} seconds\n")
        stats_text.insert("end", f"Standard deviation: {std_click:.3f} seconds\n\n")
        
        stats_text.insert("end", "MouseDown to MouseDown Stats (Time between clicks):\n")
        stats_text.insert("end", f"Min time: {min_mousedown:.3f} seconds\n")
        stats_text.insert("end", f"Max time: {max_mousedown:.3f} seconds\n")
        stats_text.insert("end", f"Average time: {avg_mousedown:.3f} seconds\n")
        stats_text.insert("end", f"Standard deviation: {std_mousedown:.3f} seconds\n")

        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Analyze repeated sequences
def analyze_repeated_sequences(file_path, repetitions, stats_text):
    try:
        repeated_sequence_count = process_repeated_sequences(file_path, repetitions)
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, "end")
        stats_text.insert("end", f"Number of repeated sequences across {repetitions} repetitions: {repeated_sequence_count}\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Display detailed repeated sequences
def display_repeated_sequences_detailed(file_path, repetitions, stats_text):
    try:
        repeated_sequences = get_repeated_sequences_detailed(file_path, repetitions)

        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, "end")
        for seq, positions in repeated_sequences.items():
            stats_text.insert("end", f"Sequence: {seq}\nPositions: {positions}\n\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Display Shannon Entropy
def display_shannon_entropy(file_path, stats_text):
    try:
        shannon_entropy_value = process_shannon_entropy(file_path)
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, "end")
        stats_text.insert("end", f"Shannon Entropy of the selected file: {shannon_entropy_value:.3f}\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Plot autocorrelation for the selected file
def plot_autocorrelation_for_selected(file_path, repetitions, stats_text):
    try:
        autocorrelation_metric = plot_autocorrelation_from_file(file_path, repetitions)
        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, "end")
        stats_text.insert("end", f"Autocorrelation Results for {file_path} with {repetitions} repetitions:\n")
        stats_text.insert("end", f"Autocorrelation Metric: {autocorrelation_metric:.2f}\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Perform clustering
def perform_clustering(file_path, n_clusters, stats_text):
    try:
        data = load_json(file_path)
        coordinates = np.array([event.get('pos') for event in data if event.get('type') == 'mouseDown'])

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

        stats_text.config(state=tk.NORMAL)
        stats_text.delete(1.0, "end")
        stats_text.insert("end", f"Cluster centers:\n{kmeans.cluster_centers_}\n")
        stats_text.insert("end", f"Labels:\n{kmeans.labels_}\n")
        stats_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
