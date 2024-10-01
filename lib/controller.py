from playback_advanced import playActions
import time
import tkinter as tk
from tkinter import filedialog, simpledialog
import os 
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.stats import entropy
from key_logger import KeyLogger
from data import (
    load_json,
    filter_clicks, compare_entries, compute_click_time_stats,
    compute_statistics 
)
from data_conversion import json_to_dataframe
from data_loader import merge_json_files
from bot_detection import calculate_shannon_entropy, plot_autocorrelation, count_repeated_sequences, detect_repeated_sequences

def elbow_method(coordinates, max_clusters):
    wcss = []
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, n_init=10, random_state=42)
        kmeans.fit(coordinates)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, max_clusters + 1), wcss, marker="o")
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    # plt.show()

    first_derivative = np.diff(wcss)
    second_derivative = np.diff(first_derivative)
    elbow_point = np.argmax(second_derivative) + 2  # +2 to account for the diff shifting the indices
    return elbow_point

# Silhouette scores to determine the optimal number of clusters
def silhouette_scores(coordinates, max_clusters):
    
    silhouette_scores = []
    for i in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, n_init=10, random_state=42)
        kmeans.fit(coordinates)
        score = silhouette_score(coordinates, kmeans.labels_)
        silhouette_scores.append(score)

    if silhouette_scores:
        plt.plot(range(2, max_clusters + 1), silhouette_scores)
        plt.title('Silhouette Scores')
        plt.xlabel('Number of clusters')
        plt.ylabel('Silhouette Score')
        # plt.show()

        optimal_clusters = np.argmax(silhouette_scores) + 2
        return optimal_clusters
    else:
        return None

def opt_clusters(coordinates):
     # # Calculate the number of unique points in the coordinates
    unique_points = len(np.unique(coordinates, axis=0))
    max_clusters = min(unique_points, 10)
    if unique_points < 2:
        print("Not enough unique points to form silhouette clusters.")
        return None
    # # Determine the optimal number of clusters using elbow method and silhouette scores
    optimal_clusters_elbow = elbow_method(coordinates, max_clusters)
    optimal_clusters_silhouette = silhouette_scores(coordinates, max_clusters)
    final_clusters = max(optimal_clusters_elbow, optimal_clusters_silhouette)
    print(f"Optimal clusters (Elbow Method): {optimal_clusters_elbow}")
    print(f"Optimal clusters (Silhouette Scores): {optimal_clusters_silhouette}")
    print(f"Final clusters is: {final_clusters}")
    return final_clusters

# Apply K-Means Clustering
def cluster(coordinates, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(coordinates)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # Plotting the results
    plt.figure(figsize=(10, 6))  # Create a new figure
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c=labels, cmap='viridis', marker='o')
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red', marker='x')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.title('K-Means Clustering of Coordinates')
    plt.colorbar(label='Cluster Label')
    plt.show()  # Display the plot
    plt.close()  # Close the figure to prevent empty windows
    
    return kmeans


def run_key_logger(output_filename, record_move_actions, min_move_interval):
    # Initialize and start the key logger with additional parameters
    key_logger = KeyLogger(record_move_actions, min_move_interval)
    key_logger.start(output_filename)

def start_key_logger_with_filename(parent):
    output_filename = simpledialog.askstring("Input", "Enter filename for recording:", parent=parent, initialvalue='default_name')
    if output_filename:
        # Prompt user for additional settings
        record_move_actions = simpledialog.askstring("Input", "Record move actions? (yes/no):", parent=parent, initialvalue='yes')
        if record_move_actions.lower() in ['yes', 'y']:
            record_move_actions = True
        else:
            record_move_actions = False

        min_move_interval = simpledialog.askfloat("Input", "Enter minimum time interval between move actions (seconds):", parent=parent, initialvalue=1.0)
        if min_move_interval is None:
            min_move_interval = 1.0

        # Call run_key_logger with the collected parameters
        run_key_logger(output_filename, record_move_actions, min_move_interval)

def select_files():
    recordings_dir = os.path.join(os.path.dirname(__file__), 'recordings')
    filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
    filenames = filedialog.askopenfilenames(title="Select JSON files", initialdir=recordings_dir, filetypes=filetypes)

    # Shorten the file paths to just the file names or relative paths
    short_filenames = [os.path.basename(filepath) for filepath in filenames]
    
    return short_filenames

def remove_items_from_list(items, indices):
    for index in reversed(indices):
        items.pop(index)
    return items

def move_item_up(items, selected_indices):
    for index in selected_indices:
        if index > 0:
            items[index], items[index - 1] = items[index - 1], items[index]
    return items

def move_item_down(items, selected_indices):
    for index in reversed(selected_indices):
        if index < len(items) - 1:
            items[index], items[index + 1] = items[index + 1], items[index]
    return items

def play_files_sequentially(filenames, path_type, vary_coords, variation, delay, loop_reps, ignore_move_actions):
    for _ in range(loop_reps):
        for filename in filenames:
            playActions(filename, path_type=path_type, vary_coords=vary_coords, variation=variation, ignore_move_actions=ignore_move_actions)
            time.sleep(delay)
## new

def get_playback_config_window(parent):
    top = tk.Toplevel(parent)
    top.title("Playback Configuration")
    top.grab_set()  # Make the window modal

    config = {}  # Initialize config here

    # Create input fields and labels
    tk.Label(top, text="Enter path type (none/spline/bezier):").pack()
    path_type_var = tk.StringVar(value='none')
    path_type_entry = tk.Entry(top, textvariable=path_type_var)
    path_type_entry.pack()

    tk.Label(top, text="Vary coordinates? (yes/no):").pack()
    vary_coords_var = tk.StringVar(value='no')
    vary_coords_entry = tk.Entry(top, textvariable=vary_coords_var)
    vary_coords_entry.pack()

    tk.Label(top, text="Ignore move actions? (yes/no):").pack()
    ignore_move_actions_var = tk.StringVar(value='no')
    ignore_move_actions_entry = tk.Entry(top, textvariable=ignore_move_actions_var)
    ignore_move_actions_entry.pack()

    tk.Label(top, text="Enter variation:").pack()
    variation_var = tk.DoubleVar(value=0.01)
    variation_entry = tk.Entry(top, textvariable=variation_var)
    variation_entry.pack()

    tk.Label(top, text="Enter number of times to loop:").pack()
    loop_reps_var = tk.IntVar(value=1)
    loop_reps_entry = tk.Entry(top, textvariable=loop_reps_var)
    loop_reps_entry.pack()

    tk.Label(top, text="Enter delay between actions:").pack()
    delay_var = tk.DoubleVar(value=2)
    delay_entry = tk.Entry(top, textvariable=delay_var)
    delay_entry.pack()

    # Function to close the window and get inputs
    def on_ok():
        config.update({
            'path_type': path_type_var.get(),
            'vary_coords': vary_coords_var.get().lower() in ['yes', 'true', '1'],
            'ignore_move_actions': ignore_move_actions_var.get().lower() in ['yes', 'true', '1'],
            'variation': variation_var.get(),
            'loop_reps': loop_reps_var.get(),
            'delay': delay_var.get()
        })
        top.destroy()  # Close the window after getting input

    tk.Button(top, text="OK", command=on_ok).pack()

    # Wait until the window is destroyed
    top.wait_window()

    return config


def get_repeated_sequences_detailed(file_path, repetitions, min_sequence_length=5):
    data = load_json(file_path)
    coordinates = [event.get('pos') for event in data if event.get('type') == 'mouseDown']
    
    # Duplicate the coordinates for the given number of repetitions
    extended_data = coordinates * repetitions

    # Detect detailed repeated sequences
    repeated_sequences = detect_repeated_sequences(extended_data, min_sequence_length)
    return repeated_sequences

def process_repeated_sequences(file_path, repetitions, min_sequence_length=5):
    data = load_json(file_path)
    coordinates = [event.get('pos') for event in data if event.get('type') == 'mouseDown']
    
    # Duplicate the coordinates for the given number of repetitions
    extended_data = coordinates * repetitions

    # Get the count of repeated sequences with fixed min_sequence_length
    repeated_sequences = detect_repeated_sequences(extended_data, min_sequence_length)
    return len(repeated_sequences)

def process_shannon_entropy(file_path):
    data = load_json(file_path)

    coordinates = [tuple(event.get('pos')) for event in data if event.get('type') == 'mouseDown' and event.get('pos') is not None]

    if not coordinates:
        raise ValueError("No valid click positions found in the file.")
    return calculate_shannon_entropy(coordinates)

def merge_selected_json_files(filenames, output_filename):
    try:
        print("Merging files:", filenames)  # Debug print
        merged_data = []
        last_time = 0

        for filename in filenames:
            if not os.path.isfile(filename):
                raise FileNotFoundError(f"The file {filename} does not exist.")
            
            with open(filename, 'r') as file:
                data = json.load(file)
                
                for entry in data:
                    if 'time' in entry:
                        entry['time'] += last_time
                
                merged_data.extend(data)
                if merged_data:
                    last_time = merged_data[-1].get('time', last_time)

        with open(output_filename, 'w') as outfile:
            json.dump(merged_data, outfile, indent=2)

        return True
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
def plot_autocorrelation_from_file(file_path, repetitions):
    data = load_json(file_path)
    coordinates = [event.get('pos') for event in data if event.get('type') == 'mouseDown']
    autocorrelation_results = plot_autocorrelation(coordinates, repetitions=repetitions)
    return autocorrelation_results

