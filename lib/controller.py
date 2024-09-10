from playback_advanced import playActions
import time
import os 
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.stats import entropy
from key_logger import KeyLogger
from tkinter import filedialog, simpledialog
from data import (
    load_json, merge_json_files, 
    filter_clicks, compare_entries, calculate_time_differences, 
    compute_statistics, calculate_shannon_entropy, detect_repeated_sequences, compute_time_stats,
    plot_autocorrelation,compute_time_stats, count_repeated_sequences, merge_json_files, json_to_dataframe
    
)

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

def start_key_logger_with_filename():
    output_filename = simpledialog.askstring("Input", "Enter filename for recording:", initialvalue='default_name')
    if output_filename:
        # Prompt user for additional settings
        record_move_actions = simpledialog.askstring("Input", "Record move actions? (yes/no):", initialvalue='yes')
        if record_move_actions.lower() in ['yes', 'y']:
            record_move_actions = True
        else:
            record_move_actions = False

        min_move_interval = simpledialog.askfloat("Input", "Enter minimum time interval between move actions (seconds):", initialvalue=1.0)
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
def get_playback_config():
    # Prompt for path type with the 'none' option added
    path_type = simpledialog.askstring("Input", "Enter path type (none/spline/bezier):", initialvalue='none')
    while path_type not in ['none', 'spline', 'bezier']:
        path_type = simpledialog.askstring("Input", "Invalid input. Enter path type (none/spline/bezier):", initialvalue='none')
    
    config = {
        'path_type': path_type,
        'vary_coords': simpledialog.askstring("Input", "Vary coordinates? (yes/no)", initialvalue='no').lower() in ['yes', 'true', '1'],
        'ignore_move_actions': simpledialog.askstring("Input", "Ignore move actions? (yes/no)", initialvalue='yes').lower() in ['yes', 'true', '1']
    }
    
    # Only prompt for variation if vary_coords is True
    if config['vary_coords']:
        config['variation'] = simpledialog.askfloat("Input", "Enter variation:", initialvalue=0.01)
    else:
        config['variation'] = 0.0

    # Ask for loop repetitions
    config['loop_reps'] = simpledialog.askinteger("Input", "Enter number of times to loop:", initialvalue=1)

    # Only prompt for delay if loop_reps is greater than 1
    if config['loop_reps'] > 1:
        config['delay'] = simpledialog.askfloat("Input", "Enter delay between actions:", initialvalue=2)
    else:
        config['delay'] = 0.0  # Set delay to 0.0 if not looping
    
    return config
##
def get_time_stats(file_path, ignore_moves=True):
    try:
        return compute_time_stats(file_path, ignore_moves)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None

def get_repeated_sequences_detailed(file_path, repetitions, min_sequence_length=5):
    data = load_json(file_path)
    coordinates = [event.get('pos') for event in data if event.get('type') == 'click']
    
    # Duplicate the coordinates for the given number of repetitions
    extended_data = coordinates * repetitions

    # Detect detailed repeated sequences
    repeated_sequences = detect_repeated_sequences(extended_data, min_sequence_length)
    return repeated_sequences

def process_repeated_sequences(file_path, repetitions, min_sequence_length=5):
    data = load_json(file_path)
    coordinates = [event.get('pos') for event in data if event.get('type') == 'click']
    
    # Duplicate the coordinates for the given number of repetitions
    extended_data = coordinates * repetitions

    # Get the count of repeated sequences with fixed min_sequence_length
    repeated_sequences = detect_repeated_sequences(extended_data, min_sequence_length)
    return len(repeated_sequences)

def process_shannon_entropy(file_path):
    data = load_json(file_path)
    coordinates = [event.get('pos') for event in data if event.get('type') == 'click']
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
    coordinates = [event.get('pos') for event in data if event.get('type') == 'click']
    autocorrelation_results = plot_autocorrelation(coordinates, repetitions=repetitions)
    return autocorrelation_results

