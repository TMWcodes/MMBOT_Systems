import json
import os
import numpy as np

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