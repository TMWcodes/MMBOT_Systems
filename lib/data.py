import numpy as np
import matplotlib.pyplot as plt
import json
import os
from scipy.stats import entropy
from collections import Counter
import pandas as pd
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

#  transforms lists of coordinate dictionaries into NumPy arrays
def load_coordinates_from_dicts(coordinates_list):
    coordinates = [[coord['x'], coord['y']] for coord in coordinates_list]
    return np.array(coordinates)

## requires retesting to see if the sequence will play after timeline has been distrupted.
def merge_json_files(filenames, output_file_name='merged_file.json'):
    merged_actions = []
    total_entries = 0

    for i, filename in enumerate(filenames):
        if not os.path.exists(filename):
            print(f"Error: {filename} not found.")
            return

        with open(filename, 'r') as file:
            actions = json.load(file)

            if i > 0:
                # Update the time of actions in the current file
                last_time_in_previous_file = merged_actions[-1]['time']
                for action in actions:
                    action['time'] += last_time_in_previous_file
            
            merged_actions.extend(actions)
            total_entries += len(actions)
            print(f'File {filename} has {len(actions)} entries.')

    print(f'Combined total entries: {total_entries}')

    script_dir = os.path.dirname(__file__)
    rec_dir = os.path.join(script_dir, 'recordings')
    output_file = os.path.join(rec_dir, output_file_name)

    with open(output_file, 'w') as f_out:
        json.dump(merged_actions, f_out, indent=2)
    
    print(f"Combined data written to {output_file} successfully!")
    return merged_actions

def filter_clicks(events):
    return [event for event in events if event.get('type') == 'click']

def compare_entries(data1, data2, compare_time=False, compare_color=True, compare_position=True):
    differences = []
    
    for i, (entry1, entry2) in enumerate(zip(data1, data2)):
        pos1, color1, time1 = entry1.get('pos'), entry1.get('color'), entry1.get('time')
        pos2, color2, time2 = entry2.get('pos'), entry2.get('color'), entry2.get('time')

        pos_diff = pos1 != pos2 if compare_position else False
        color_diff = color1 != color2 if compare_color else False
        time_diff = time1 != time2 if compare_time else False

        if pos_diff or color_diff or time_diff:
            diffs_file1 = []
            diffs_file2 = []

            if compare_time and time_diff:
                diffs_file1.append(f"Time: {time1}")
                diffs_file2.append(f"Time: {time2}")
            if compare_position and pos_diff:
                diffs_file1.append(f"Pos: {pos1}")
                diffs_file2.append(f"Pos: {pos2}")
            if compare_color and color_diff:
                diffs_file1.append(f"Color: {color1}")
                diffs_file2.append(f"Color: {color2}")

            differences.append(f"Index {i}:\n  File 1 - {', '.join(diffs_file1)}\n  File 2 - {', '.join(diffs_file2)}")

    return differences
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

def compute_time_stats(filename, ignore_moves="yes"):
    events = load_json(filename)
    time_diffs = calculate_time_differences(events, ignore_moves)
    # Compute and print time statistics
    min_time, max_time, avg_time, std_time = compute_statistics(time_diffs)
    print(f"Min time between actions: {min_time:.3f} seconds")
    print(f"Max time between actions: {max_time:.3f} seconds")
    print(f"Average time between actions: {avg_time:.3f} seconds")
    print(f"Standard deviation of time differences: {std_time} seconds")
    if min_time is None:
        min_time, max_time, avg_time, std_time = 0, 0, 0, 0
    
    return min_time, max_time, avg_time, std_time
    # if avg_time < 0.2 and std_time < 0.1:  # Example thresholds
    #     print("Suspicious bot-like behavior detected!")
    # else:
    #     print("Likely human behavior.")
    

def calculate_shannon_entropy(sequence):
    unique, counts = np.unique(sequence, axis=0, return_counts=True)
    probs = counts / len(sequence)
    shannon_entropy = entropy(probs)
    return shannon_entropy

def count_repeated_sequences(coordinates, min_sequence_length=5, min_repetitions=2):
    sequences = {}
    for i in range(len(coordinates) - min_sequence_length + 1):
        sequence = tuple(tuple(coord) for coord in coordinates[i:i + min_sequence_length])
        if sequence in sequences:
            sequences[sequence].append(i)
        else:
            sequences[sequence] = [i]

    repeated_sequence_count = sum(1 for indices in sequences.values() if len(indices) >= min_repetitions)
    return repeated_sequence_count

def detect_repeated_sequences(coordinates, min_sequence_length=5, min_repetitions=2):
    sequences = {}
    for i in range(len(coordinates) - min_sequence_length + 1):
        sequence = tuple(tuple(coord) for coord in coordinates[i:i + min_sequence_length])
        if sequence in sequences:
            sequences[sequence].append(i)
        else:
            sequences[sequence] = [i]

    repeated_sequences = {seq: indices for seq, indices in sequences.items() if len(indices) >= min_repetitions}
    return repeated_sequences

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
    
    # Compute multidimensional autocorrelation
    acf = multidimensional_autocorrelation(sequence_repeated)
    
    # Calculate a simple metric, such as the mean of the first few lags
    autocorr_metric = np.mean(acf[:len(sequence)]) * 1000
    
    # Plot the autocorrelation with custom figure size
    # plt.figure(figsize=figsize)  # Create a new figure
    # lags = range(min(len(acf), max_lag))
    # plt.stem(lags, acf[:max_lag], linefmt='-', markerfmt='o', basefmt=' ')
    # plt.xlabel('Lag')
    # plt.ylabel('Autocorrelation')
    # plt.title(f'Multidimensional Autocorrelation of Coordinate Pairs (Repeated {repetitions} times)')
    # plt.show()  # Display the plot
    # plt.close()  # Close the figure to prevent empty windows
    
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


def json_to_dataframe(json_file):
    data = load_json(json_file)
    df = pd.DataFrame(data)

    # Convert 'pos' and 'color' lists to strings for display
    df['pos'] = df['pos'].apply(lambda x: ', '.join(map(str, x)) if x else 'None')
    df['color'] = df['color'].apply(lambda x: ', '.join(map(str, x)) if x else 'None')

    # Round the 'time' column to 4 decimal places
    df['time'] = df['time'].round(4)

    # Initialize a list to hold the filtered rows
    filtered_data = []
    held_keys = {}  # Track keys that are held down

    i = 0
    while i < len(df):
        current_row = df.iloc[i].copy()  # Make a copy to avoid SettingWithCopyWarning

        if current_row['type'] == 'keyDown':
            key = current_row['button']

            # Check if the key is held down and suppress duplicate keyDown events
            if key not in held_keys:
                held_keys[key] = True  # Mark the key as held down
                
                # Check if the next event is a 'keyUp' for the same key within 0.2 seconds
                if i + 1 < len(df):
                    next_row = df.iloc[i + 1]
                    if (
                        next_row['type'] == 'keyUp' 
                        and next_row['button'] == key 
                        and next_row['time'] - current_row['time'] <= 0.2
                    ):
                        # Combine 'keyDown' and 'keyUp' into a single 'keyPress' event
                        current_row['type'] = 'keyPress'
                        filtered_data.append(current_row)
                        i += 1  # Skip the next row (keyUp) since it's combined
                    else:
                        # No immediate keyUp, so just add the keyDown event
                        filtered_data.append(current_row)
                else:
                    filtered_data.append(current_row)

        elif current_row['type'] == 'keyUp':
            key = current_row['button']

            # Remove the key from held keys and add keyUp event to the display
            held_keys.pop(key, None)
            filtered_data.append(current_row)

        else:
            # For non-key events, just add them
            filtered_data.append(current_row)

        i += 1

    # Convert the filtered data back to a DataFrame
    df_filtered = pd.DataFrame(filtered_data)
    return df_filtered

# def main():
 
    
# if __name__ == "__main__":
#     main()