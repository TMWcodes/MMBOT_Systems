import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json
import os
from scipy.stats import entropy
from collections import Counter


# Load JSON data from a file
def load_json(filename):
    script_dir = os.path.dirname(__file__)
    
    # Check in 'recordings' directory
    recordings_path = os.path.join(script_dir, 'recordings', filename)
    # print(f"Checking for file in: {recordings_path}")  # Debug print
    if os.path.exists(recordings_path):
        with open(recordings_path, 'r') as file:
            return json.load(file)
    
    # Check in 'log_records' directory
    log_records_path = os.path.join(script_dir, 'log_records', filename)
    # print(f"Checking for file in: {log_records_path}")  # Debug print
    if os.path.exists(log_records_path):
        with open(log_records_path, 'r') as file:
            return json.load(file)
    
    # If file is not found in both directories
    raise FileNotFoundError(f"File '{filename}' not found in 'recordings' or 'log_records' directories.")
# Load coordinates from JSON data with an option to ignore move actions
def load_coordinates(events, ignore_moves=False):
    coordinates = []
    for event in events:
        if ignore_moves and event.get('type') == 'move':
            continue
        pos = event.get('pos')
        if pos and isinstance(pos, list) and len(pos) == 2:
            coordinates.append(pos)
    return np.array(coordinates)

# Calculate time differences between consecutive events with an option to ignore move actions
def calculate_time_differences(events, ignore_moves=False):
    time_diffs = []
    filtered_events = [event for event in events if not (ignore_moves and event.get('type') == 'move')]
    
    for i in range(1, len(filtered_events)):
        time_diff = filtered_events[i]['time'] - filtered_events[i-1]['time']
        time_diffs.append(time_diff)
    return time_diffs

# Compute min, max, and average time differences
def compute_statistics(time_diffs):
    if not time_diffs:
        return None, None, None
    
    min_time = min(time_diffs)
    max_time = max(time_diffs)
    avg_time = sum(time_diffs) / len(time_diffs)
    std_time = np.std(time_diffs)
    
    return min_time, max_time, avg_time, std_time
   

# Apply K-Means Clustering
def cluster(coordinates, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(coordinates)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # Plotting the results
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c=labels, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.title('K-Means Clustering of Coordinates')
    # plt.show()

def calculate_shannon_entropy(sequence):
    unique, counts = np.unique(sequence, axis=0, return_counts=True)
    probs = counts / len(sequence)
    shannon_entropy = entropy(probs)
    return shannon_entropy

# Elbow method to determine the optimal number of clusters
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

def detect_repetition(coordinates, threshold):
    coordinate_tuples = tuple(map(tuple, coordinates))
    coordinate_counts = Counter(coordinate_tuples)
    total_coordinates = len(coordinates)
    # Calculate frequency of each event
    frequencies = {coord: count / total_coordinates for coord, count in coordinate_counts.items()}
    # Check if any event frequency exceeds the threshold
    repeated_coordinates = [coord for coord, freq in frequencies.items() if freq > threshold]
    
    return repeated_coordinates

def compute_time_stats(filename, ignore_moves="yes"):
    events = load_json(filename)
    time_diffs = calculate_time_differences(events, ignore_moves)
    # Compute and print time statistics
    min_time, max_time, avg_time, std_time = compute_statistics(time_diffs)
    print(f"Min time between actions: {min_time:.3f} seconds")
    print(f"Max time between actions: {max_time:.3f} seconds")
    print(f"Average time between actions: {avg_time:.3f} seconds")
    print(f"Standard deviation of time differences: {std_time} seconds")
    # if avg_time < 0.2 and std_time < 0.1:  # Example thresholds
    #     print("Suspicious bot-like behavior detected!")
    # else:
    #     print("Likely human behavior.")
# Convert coordinates list to NumPy array
def load_coordinates_from_dicts(coordinates_list):
    coordinates = [[coord['x'], coord['y']] for coord in coordinates_list]
    return np.array(coordinates)


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

def plot_autocorrelation(sequence, repetitions, figsize=(12, 6), max_lag=50):
    """
    Plot the multidimensional autocorrelation of a sequence of coordinate pairs.
    
    Parameters:
    - sequence: numpy array of shape (n, 2) where n is the number of coordinate pairs.
    - repetitions: int, the number of times the sequence is repeated.
    - figsize: tuple, the size of the figure (width, height) in inches.
    - max_lag: int, maximum number of lags to display in the plot.
    
    """
    
    def multidimensional_autocorrelation(sequence):
        # Flatten the 2D sequence into a 1D array
        flat_sequence = sequence.flatten()
        
        n = len(flat_sequence)
        variance = np.var(flat_sequence)
        flat_sequence = flat_sequence - np.mean(flat_sequence)
        
        # Compute the autocorrelation
        r = np.correlate(flat_sequence, flat_sequence, mode='full')[-n:]
        result = r / (variance * (np.arange(n, 0, -1)))
        
        return result
    
    # Repeat the sequence to simulate multiple repetitions
    sequence_repeated = np.tile(sequence, (repetitions, 1))
    # print("Repeated Sequence:\n", sequence_repeated) # debug
    
    # Compute multidimensional autocorrelation
    acf = multidimensional_autocorrelation(sequence_repeated)
    
    # Calculate a simple metric, such as the mean of the first few lags
    autocorr_metric = np.mean(acf[:len(sequence)])
    autocorr_metric = autocorr_metric * 1000
    
    # Plotting the autocorrelation with custom figure size
    plt.figure(figsize=figsize)  # Set figure size
    lags = range(min(len(acf), max_lag))
    plt.stem(lags, acf[:max_lag], linefmt='-', markerfmt='o', basefmt=' ')
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title(f'Multidimensional Autocorrelation of Coordinate Pairs (Repeated {repetitions} times)')
    plt.show()
    
    print(f"Autocorrelation metric for {repetitions} repetitions: {autocorr_metric}")

    return autocorr_metric

def compare_json_files(file1, file2):
    data1 = load_json(file1)
    data2 = load_json(file2)
    
    if len(data1) != len(data2):
        print(f"Files have different number of entries: {len(data1)} vs {len(data2)}")
        return

    differences = []
    for i, (entry1, entry2) in enumerate(zip(data1, data2)):
        pos1, color1 = entry1['pos'], entry1['color']
        pos2, color2 = entry2['pos'], entry2['color']
        
        if pos1 != pos2 or color1 != color2:
            differences.append({
                'index': i,
                'file1': {'pos': pos1, 'color': color1},
                'file2': {'pos': pos2, 'color': color2}
            })

    if differences:
        print(f"Differences found in {len(differences)} entries:")
        for diff in differences:
            print(f"Index {diff['index']}:")
            print(f"  File 1 - Pos: {diff['file1']['pos']}, Color: {diff['file1']['color']}")
            print(f"  File 2 - Pos: {diff['file2']['pos']}, Color: {diff['file2']['color']}")
    else:
        print("No differences found")

# Replace with the actual file paths


def main():
    filename = input("Enter filename: ")
    ignore_moves = input("Ignore move actions? (yes/no): ").strip().lower() == 'yes'
    print("from json") 
    compute_time_stats(filename)
    events = load_json(filename)
    
    coordinates = load_coordinates(events, ignore_moves)
    


#     print("from dict")
#     coordinates_list = [
#     {'x': 1435, 'y': 758},
#     {'x': 1376, 'y': 696},
#     {'x': 1475, 'y': 302},
#     {'x': 1435, 'y': 758},  # Repeated coordinate
#     {'x': 1376, 'y': 696},  # Repeated coordinate
#     {'x': 1435, 'y': 758},  # Repeated coordinate
# ]
#     coordinates = load_coordinates_from_dicts(coordinates_list)
   
    # # # Perform clustering with the optimal number of clusters
    final_clusters = opt_clusters(coordinates)
    cluster(coordinates, n_clusters=final_clusters)
    
    num_repeats = 10
    threshold = 0.3
    # repeated_sequences = [np.tile(coordinates, (i, 1)) for i in range(1, num_repeats + 1)]
    # print(repeated_sequences)

    for i in range(1, num_repeats + 1):
        repeated_sequence = np.tile(coordinates, (i, 1))

    # # print(repeated_sequence)
    # # #     #  # # Perform clustering with the optimal number of clusters
    # final_clusters = opt_clusters(repeated_sequence)
    # cluster(repeated_sequence, n_clusters=final_clusters)
    shannon_entropy = calculate_shannon_entropy(repeated_sequence)
    repeated_coords = detect_repetition(repeated_sequence, threshold)
   
    print(f"Sequence repeated {i} times - Shannon Entropy: {shannon_entropy:.3f}")
    print(f"Repeated Coordinates:{repeated_coords}")
    print(f"there are {len(coordinates)} coordinates")
    # Call the method with the sequence repeated 100 times
    # autocorr_metric = plot_autocorrelation(coordinates, num_repeats)

    for num_repeats in [1, num_repeats, 100]:
        autocorr_metric = plot_autocorrelation(coordinates, num_repeats)

file_in = input()
file1 = r'C:\Users\Tyrone\Documents\Programming\coding\MMBOT_systems\lib\log_records\color_coord_test_01_log.json'
file2 = r'C:\Users\Tyrone\Documents\Programming\coding\MMBOT_systems\lib\log_records\file_in'

compare_json_files(file1, file2)
if __name__ == "__main__":
    main()