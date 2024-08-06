import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json
import os
from scipy.stats import entropy
from collections import Counter
import pandas as pd#
from itertools import islice


# Load JSON data from a file
def load_json(filename):
    script_dir = os.path.dirname(__file__)
    
    # Check in 'recordings' directory
    recordings_path = os.path.join(script_dir, 'recordings', filename)
    if os.path.exists(recordings_path):
        with open(recordings_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    # Check in 'log_records' directory
    log_records_path = os.path.join(script_dir, 'log_records', filename)
    if os.path.exists(log_records_path):
        with open(log_records_path, 'r', encoding='utf-8') as file:
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

def load_coordinates_from_dicts(coordinates_list):
    coordinates = [[coord['x'], coord['y']] for coord in coordinates_list]
    return np.array(coordinates)

## requires retesting to see if the sequence will play after timeline has been distrupted.
def combine_json(file1_name, file2_name, output_file_name='combined_file.json'):
    script_dir = os.path.dirname(__file__)
    rec_dir = os.path.join(script_dir, 'recordings')

    file1 = os.path.join(rec_dir, file1_name)
    file2 = os.path.join(rec_dir, file2_name)
    output_file = os.path.join(rec_dir, output_file_name)

    if not os.path.exists(file1):
        print(f"Error: {file1} not found.")
        return
    if not os.path.exists(file2):
        print(f"Error: {file2} not found.")
        return

    with open(file1, 'r') as f1:
        data1 = json.load(f1)
    with open(file2, 'r') as f2:
        data2 = json.load(f2)

    combined_data = data1 + data2
    with open(output_file, 'w') as f_out:
        json.dump(combined_data, f_out, indent=2)
    print(f'file1 has {len(data1)} entries, file2 has {len(data2)} entries, combined has {len(combined_data)} entries')
    print(f"Combined data written to {output_file} successfully!")

## untested
def merge_json_files(filenames):
    merged_actions = []
    for filename in filenames:
        with open(filename, 'r') as file:
            actions = json.load(file)
            
            if merged_actions:
                # Update the time of actions in the current file
                last_time_in_previous_file = merged_actions[-1]['time']
                for action in actions:
                    action['time'] += last_time_in_previous_file
            
            merged_actions.extend(actions)
            
    return merged_actions

def filter_clicks(events):
    clicks = [event for event in events if event.get('type') == 'click']
    return clicks

def compare_clicks(file1, file2):
    if len(file1) != len(file2):
        print(f"Files have different number of click entries: {len(file1)} vs {len(file2)}")
        return

    differences = []
    for i, (entry1, entry2) in enumerate(zip(file1, file2)):
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
    return kmeans

def detect_repetition(coordinates, threshold):
    coordinate_tuples = tuple(map(tuple, coordinates))
    coordinate_counts = Counter(coordinate_tuples)
    total_coordinates = len(coordinates)
    # Calculate frequency of each event
    frequencies = {coord: count / total_coordinates for coord, count in coordinate_counts.items()}
    # Check if any event frequency exceeds the threshold
    repeated_coordinates = [coord for coord, freq in frequencies.items() if freq > threshold]
    
    return repeated_coordinates

def detect_repeated_sequences(coordinates, min_sequence_length=3, min_repetitions=2):
    def window(seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    # Convert numpy arrays to tuples for hashing
    coordinates = [tuple(coord) for coord in coordinates]

    sequences = {}
    for i in range(len(coordinates) - min_sequence_length + 1):
        sequence = tuple(coordinates[i:i + min_sequence_length])
        if sequence in sequences:
            sequences[sequence].append(i)
        else:
            sequences[sequence] = [i]

    repeated_sequences = {seq: indices for seq, indices in sequences.items() if len(indices) >= min_repetitions}
    return repeated_sequences

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

def divide_coordinates(coords, num_groups, output_file_name):
    script_dir = os.path.dirname(__file__)
    log_dir = os.path.join(script_dir, 'data_points')
    output_file = os.path.join(log_dir, output_file_name)
    os.makedirs(log_dir, exist_ok=True)

    structured_coords = {}
    coords_per_group = len(coords) // num_groups
    remainder = len(coords) % num_groups

    start = 0
    for i in range(num_groups):
        end = start + coords_per_group + (1 if i < remainder else 0)
        group_name = f'rock{i+1}'
        structured_coords[group_name] = [{'x': int(coord[0]), 'y': int(coord[1])} for coord in coords[start:end]]
        start = end
    
    with open(output_file, 'w') as f_out:
        json.dump(structured_coords, f_out, indent=2)
    print(f"Divided coordinates saved to {output_file}")

    return structured_coords
 
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
    # plt.show()
    
    print(f"Autocorrelation metric for {repetitions} repetitions: {autocorr_metric}")

    return autocorr_metric

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            out[name[:-1]] = json.dumps(x)  # Store list as JSON string
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def unflatten_json(flat):
    out = {}
    for k, v in flat.items():
        keys = k.split('_')
        d = out
        for key in keys[:-1]:
            if key.isdigit():
                key = int(key)
            if key not in d:
                d[key] = {}
            d = d[key]
        try:
            v = json.loads(v)  # Convert JSON string back to list
        except (ValueError, TypeError):
            pass
        d[keys[-1]] = v
    return out

def json_to_csv(json_filename, csv_filename):
    try:
        data = load_json(json_filename)
        flattened_data = [flatten_json(item) for item in data]

        df = pd.DataFrame(flattened_data)
        
        csv_dir = os.path.dirname(csv_filename)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        df.to_csv(csv_filename, encoding='utf-8', index=False)
        
        print(f"Successfully converted '{json_filename}' to '{csv_filename}'.")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

# CSV to JSON Function
def csv_to_json(csv_filename, json_filename):
    try:
        df = pd.read_csv(csv_filename, encoding='utf-8')
        data = df.to_dict(orient='records')
        unflattened_data = [unflatten_json(item) for item in data]

        json_dir = os.path.dirname(json_filename)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(unflattened_data, json_file, indent=4)
        
        print(f"Successfully converted '{csv_filename}' to '{json_filename}'.")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
       
# Example usage
   
#     filename = 'combined_file.json'
#     ignore_moves = 'yes'
# # #     filename = input("Enter file name: ")
# # #     ignore_moves = input("Ignore move actions? (yes/no): ").strip().lower() == 'yes'
#     print("from json") 
# #     compute_time_stats(filename)
#     events = load_json(filename)
#     coordinates = load_coordinates(events, ignore_moves)
#     print(coordinates)
#     repeated_sequences = detect_repeated_sequences(coordinates)
#     print("Repeated Sequences:", repeated_sequences)
    
#     rock_coords = divide_coordinates(coordinates, 5, '')

    
# #     print("from dictionary")
# #     coordinates_list = [
# #     {'x': 1435, 'y': 758},
# #     {'x': 1376, 'y': 696},
# #     {'x': 1475, 'y': 302},
# #     {'x': 1435, 'y': 758},  # Repeated coordinate
# #     {'x': 1376, 'y': 696},  # Repeated coordinate
# #     {'x': 1435, 'y': 758},  # Repeated coordinate
# # ]
# #     coordinates = load_coordinates_from_dicts(coordinates_list)
   
#     # Perform clustering with the optimal number of clusters
#     final_clusters = opt_clusters(coordinates)
#     cluster(coordinates, n_clusters=final_clusters)
    
#     num_repeats  = 10
#     threshold = 0.3
#     repeated_sequences = [np.tile(coordinates, (i, 1)) for i in range(1, num_repeats + 1)]
#     # print(repeated_sequences)

#     for i in range(1, num_repeats + 1):
#         repeated_sequence = np.tile(coordinates, (i, 1))


#     # #     #  # # Perform clustering with the optimal number of clusters
#     final_clusters = opt_clusters(repeated_sequence)
#     cluster(repeated_sequence, n_clusters=final_clusters)
#     shannon_entropy = calculate_shannon_entropy(repeated_sequence)
#     repeated_coords = detect_repetition(repeated_sequence, threshold)
   
#     print(f"Sequence repeated {i} times - Shannon Entropy: {shannon_entropy:.3f}")
#     print(f"Repeated Coordinates:{repeated_coords}")
#     print(f"there are {len(coordinates)} coordinates")
#     # Call the method with the sequence repeated 100 times
#     # autocorr_metric = plot_autocorrelation(coordinates, num_repeats)

#     for num_repeats in [1, num_repeats, 100]:
#         autocorr_metric = plot_autocorrelation(coordinates, num_repeats)

# json_to_csv('color_coord_test_01_log_1.json', 'csv_data/output.csv')
# csv_to_json('csv_data/output.csv', 'log_records/output.json')

# # compare json files
# # file_in = input("enter second file to compare: ")
    file1 = 'lum_mine_copper_01.json'
    file2 = 'lum_mine_copper_01_log.json'
    try:
        compare_json_files(file1, file2)
    except FileNotFoundError as e:
        print(e)

#     file_1 = ''
#     file_2 = ''
# # Combine the JSON files
#     combine_json(file_1, file_2)

if __name__ == "__main__":
    main()