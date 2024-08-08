from playback_advanced import playActions
import time
import os 
from key_logger import main as start_key_logger
from tkinter import filedialog, simpledialog
from data import (
    load_json, load_coordinates, load_coordinates_from_dicts, combine_json, merge_json_files, 
    filter_clicks, compare_clicks, compare_json_files, calculate_time_differences, 
    compute_statistics, calculate_shannon_entropy, elbow_method, silhouette_scores, 
    cluster, detect_repetition, detect_repeated_sequences, compute_time_stats, 
    divide_coordinates, opt_clusters, plot_autocorrelation, flatten_json, unflatten_json, 
    json_to_csv, compute_time_stats
)


def run_key_logger(output_filename):
    start_key_logger(output_filename)

def start_key_logger_with_filename():
    output_filename = simpledialog.askstring("Input", "Enter filename for recording:", initialvalue='default_name')
    if output_filename:
        run_key_logger(output_filename)

def select_files():
    recordings_dir = os.path.join(os.path.dirname(__file__), 'recordings')
    filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
    return filedialog.askopenfilenames(title="Select JSON files", initialdir=recordings_dir, filetypes=filetypes)

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

def play_files_sequentially(filenames, path_type, vary_coords, variation, delay, loop_reps):
    for _ in range(loop_reps):
        for filename in filenames:
            playActions(filename, path_type=path_type, vary_coords=vary_coords, variation=variation)
            time.sleep(delay)
## new
def get_playback_config():
    config = {
        'path_type': simpledialog.askstring("Input", "Enter path type:", initialvalue='spline'),
        'vary_coords': simpledialog.askstring("Input", "Vary coordinates? (yes/no)", initialvalue='yes').lower() in ['yes', 'true', '1'],
        'variation': simpledialog.askfloat("Input", "Enter variation:", initialvalue=0.05),
        'delay': simpledialog.askfloat("Input", "Enter delay between actions:", initialvalue=2),
        'loop_reps': simpledialog.askinteger("Input", "Enter number of times to loop:", initialvalue=1)
    }
    return config
##
def get_time_stats(file_path, ignore_moves=True):
    try:
        return compute_time_stats(file_path, ignore_moves)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None

def get_repeated_sequences(file_path, min_sequence_length=3, min_repetitions=2):
    data = load_json(file_path)
    coordinates = []

    for event in data:
        if event.get('type') == 'click':  # Only process 'click' events
            pos = event.get('pos')
            if pos and len(pos) == 2:  # Ensure pos has both x and y
                coordinates.append(tuple(pos))  # Convert list to tuple for hashing

    if not coordinates:
        raise ValueError("No valid coordinates found in the selected file.")

    repeated_sequences = detect_repeated_sequences(coordinates, min_sequence_length, min_repetitions)
    return repeated_sequences


def process_repeated_sequences(file_path, repetitions):
    data = load_json(file_path)
    coordinates = [event['pos'] for event in data if event['type'] == 'click']
    extended_data = coordinates * repetitions

    # Get the count of repeated sequences
    return detect_repeated_sequences(extended_data)