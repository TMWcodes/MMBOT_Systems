import pyautogui
from time import time, sleep
import random
from my_utils import holdKey,initialize_pyautogui, count_down_timer, compare_colors, check_color, vary_coordinates
from data import load_json, filter_clicks
import json
import numpy as np
import os

log_data=[]
# color = check_color()
start_time = time() 


def log_action(log_data, coordinates, color, elapsed_time):
    log_data.append({
        'time': elapsed_time,
        'type': 'click',
        'button': 'Button.left' if pyautogui.position() == coordinates else 'Button.right',
        'pos': coordinates,
        'color': color
    })

def setup_logging(filename):
    # Directory of the current script
    script_dir = os.path.dirname(__file__)
    
    # Path to the log directory within the script directory
    log_dir = os.path.join(script_dir, 'log_records')
    os.makedirs(log_dir, exist_ok=True)  # Create the log_records directory if it doesn't exist
    
    # Base filename for the log file
    base_filename = os.path.splitext(filename)[0]
    log_record_path = os.path.join(log_dir, f'{base_filename}_log.json')
    
    # Ensure the log file name is unique
    if os.path.exists(log_record_path):
        i = 1
        new_log_record_path = log_record_path
        while os.path.exists(new_log_record_path):
            new_log_record_path = os.path.join(log_dir, f'{base_filename}_log_{i}.json')
            i += 1
        log_record_path = new_log_record_path
    
    return log_record_path

def save_log_data(log_data, log_record_path):
    # Save the log data to the specified JSON file
    with open(log_record_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)
    print(f"Log data saved to: {log_record_path}")

def load_coordinates(events, ignore_moves=False):
    coordinates = []
    for event in events:
        if ignore_moves and event.get('type') == 'move':
            continue
        pos = event.get('pos')
        if pos and isinstance(pos, list) and len(pos) == 2:
            coordinates.append(pos)
    return np.array(coordinates)

def extract_colors_from_clicks(click_events):
    colors = []
    for event in click_events:
        if event.get('color'):
            colors.append(tuple(event['color']))  # Convert list to tuple
    return colors

def filter_duplicate_colors(colors):
    # Convert list to a set to remove duplicates, then back to a list
    unique_colors = list(set(colors))
    return unique_colors


def check_and_click_if_color_matches(coordinate, expected_colors, idx, click_delay=0.1):
    """
    Checks the color at a given coordinate and clicks if it matches the expected color.
    
    Parameters:
    - coordinate: A tuple (x, y) representing the screen coordinates.
    - expected_colors: A list of tuples (R, G, B) representing expected colors.
    - idx: The index of the current coordinate in the loop.
    - click_delay: Delay in seconds to wait before clicking.
    """
    if idx < len(expected_colors):
        expected_color = expected_colors[idx]
        
        # Move to the coordinate and check the color
        pyautogui.moveTo(coordinate[0], coordinate[1])
        if compare_colors(coordinate, expected_color):
            print(f'Color at {coordinate} matches the expected color {expected_color}.')
            pyautogui.click()
            print(f'Clicked at {coordinate}.')
            sleep(click_delay)  # Optional delay after clicking
        else:
            print(f'Color at {coordinate} does not match the expected color {expected_color}.')
    else:
        print(f'No expected color for coordinate {coordinate}')

def is_expected_color(color, expected_colors):
    return color in expected_colors

def click_if_color_matches(expected_colors):
    x, y = pyautogui.position()
    color = pyautogui.pixel(x, y)

    if is_expected_color(color, expected_colors):
        print(f"Color {color} matches expected colors. Clicking at ({x}, {y})...")
        pyautogui.click(x, y)
    else:
        print(f"Color {color} does not match. Skipping click at ({x}, {y}).")


def coordinates_to_path(coordinates_array):
    # Convert each coordinate in the numpy array to a dictionary
    path = [{'x': int(coord[0]), 'y': int(coord[1])} for coord in coordinates_array]
    return path

paths_dict = {
    'path1': [{'x': 100, 'y': 200}, {'x': 150, 'y': 250}],
    'path2': [{'x': 300, 'y': 400}, {'x': 350, 'y': 450}],
    }

def move_to_and_click(x, y):
    pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)
    pyautogui.click()

def perform_path_navigation(path_name, path, log_data):
    print(f"Performing path navigation: {path_name}")
    for point in path:
        x, y = point['x'], point['y']
        print(f"Moving to {x}, {y}")
        move_to_and_click(x, y)
        # Log the action
        start_time = time()
        color = pyautogui.screenshot().getpixel((x, y))
        elapsed_time = time() - start_time
        log_action(log_data, (x, y), color, elapsed_time)
        # Simulate delay
        sleep(random.uniform(1, 3))  # Random delay

def pre_check_click_colors(filename):
    # Load events from the JSON file
    events = load_json(filename)
    
    # Load coordinates and extract colors from clicks
    coordinates = load_coordinates(events, True)
    click_events = filter_clicks(events)
    expected_colors = extract_colors_from_clicks(click_events)
    unique_colors = filter_duplicate_colors(expected_colors)

    print(f'Coordinates are {coordinates}')
    print(f'Expected colors are {expected_colors}, {len(expected_colors)}')
    print(f'Unique colors are {unique_colors}, {len(unique_colors)}')

    # Iterate over the coordinates and check/click if the color matches
    for idx, coord in enumerate(coordinates):
        coordinate = (int(coord[0]), int(coord[1]))
        check_and_click_if_color_matches(coordinate, expected_colors, idx)


def main():
    # filename = "color_range.json"
    # events = load_json(filename)
    
    # # Load coordinates and extract colors from clicks
    # coordinates = load_coordinates(events, True)
    # click_events = filter_clicks(events)
    # expected_colors = extract_colors_from_clicks(click_events)  # Assuming this provides expected colors
    # print(f'Coordinates are {coordinates}')
    # print(f'Expected colors are {expected_colors}, {len(expected_colors)}')
    
    # unique_colors = filter_duplicate_colors(expected_colors)
    # print(f'unique_colors are {unique_colors}, {len(unique_colors)}')



    ## move to own function?
    # 

    # Paths and Locations Data
 
    # path = coordinates_to_path(coordinates)
    # print(path)
    # path_name = "example_path"
    # log_data = []
    # perform_path_navigation(path_name, path, log_data)
    # filesave = 'main'
    # log_record_path = setup_logging(filesave)
    # save_log_data(log_data, log_record_path)


    pre_check_click_colors('default_name.json')
#     
if __name__ == "__main__":
    main()