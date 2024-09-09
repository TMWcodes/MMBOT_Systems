import pyautogui
from time import time, sleep
import random
from my_utils import holdKey, initialize_pyautogui, compare_colors, check_color
from data import load_json, filter_clicks
import json
import numpy as np
import os
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def setup_logging(filename):
    log_dir = os.path.join(os.path.dirname(__file__), 'log_records')
    os.makedirs(log_dir, exist_ok=True)
    base_filename = os.path.splitext(filename)[0]
    log_record_path = os.path.join(log_dir, f'{base_filename}_log.json')

    i = 1
    while os.path.exists(log_record_path):
        log_record_path = os.path.join(log_dir, f'{base_filename}_log_{i}.json')
        i += 1

    return log_record_path


def save_log_data(log_data, log_record_path):
    with open(log_record_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)
    print(f"Log data saved to: {log_record_path}")


def log_action(log_data, coordinates, color, elapsed_time):
    log_data.append({
        'time': elapsed_time,
        'type': 'click',
        'button': 'Button.left' if pyautogui.position() == coordinates else 'Button.right',
        'pos': coordinates,
        'color': color
    })


def load_coordinates(events, ignore_moves=False):
    return np.array([
        event.get('pos') for event in events 
        if not (ignore_moves and event.get('type') == 'move') and event.get('pos') and len(event.get('pos')) == 2
    ])


def extract_colors_from_clicks(click_events):
    return [tuple(event['color']) for event in click_events if event.get('color')]


def filter_duplicate_colors(colors):
    return list(set(colors))


def are_colors_similar(color1, color2, tolerance):
    squared_distance = sum((comp1 - comp2) ** 2 for comp1, comp2 in zip(color1, color2))
    return squared_distance <= tolerance ** 2

def is_color_in_samples(color, samples, tolerance):
    for sample in samples:
        if are_colors_similar(color, sample, tolerance):
            return sample
    return None


def process_coordinates(coordinates, unique_colors, tolerance=10):
    for coordinate in coordinates:
        x, y = map(int, coordinate)
        try:
            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)
            current_color = pyautogui.pixel(x, y)
            print(f'Checking coordinate ({x}, {y})')
            print(f'  Retrieved color: {current_color}')

            matching_color = is_color_in_samples(current_color, unique_colors, tolerance)
            if matching_color:
                print(f'  Color {current_color} matches the sample {matching_color} with tolerance {tolerance}. Action required: Click!')
                pyautogui.click()
            else:
                print(f'  Color {current_color} does not match any of the samples. Action required: Do not click.')

        except Exception as e:
            print(f'Error at coordinate ({x}, {y}): {e}')


def check_colors_and_click(filename, unique_colors, match_by_index=False, click_delay=0.1, tolerance=10):
    """
    Checks colors at coordinates and clicks if they match.
    
    Parameters:
    - filename: The name of the JSON file containing the events.
    - unique_colors: A list of unique colors to match against.
    - match_by_index: If True, matches colors by index (original functionality). If False, matches against unique colors.
    - click_delay: Delay in seconds to wait before clicking (optional).
    - tolerance: The tolerance level for color matching (optional).
    """
    events = load_json(filename)
    coordinates = load_coordinates(events, True)
    expected_colors = extract_colors_from_clicks(filter_clicks(events))
    
    if match_by_index:
        print("Matching colors by index...")
        # Match colors by index, using the original functionality
        for idx, coordinate in enumerate(coordinates):
            if idx < len(expected_colors):
                expected_color = expected_colors[idx]
                x, y = map(int, coordinate)
                
                try:
                    pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)
                    current_color = pyautogui.pixel(x, y)

                    if are_colors_similar(current_color, expected_color, tolerance):
                        print(f'Color at {coordinate} matches the expected color {expected_color}. Clicking...')
                        pyautogui.click()
                        sleep(click_delay)
                    else:
                        print(f'Color at {coordinate} does not match the expected color {expected_color}. No action taken.')
                except Exception as e:
                    print(f'Error at coordinate ({x}, {y}): {e}')
            else:
                print(f'No expected color for coordinate {coordinate}')
    else:
        print("Matching against unique colors...")
        # Match colors against the unique colors, using the refactored functionality
        process_coordinates(coordinates, unique_colors, tolerance)

#    creates file with coordinates and unique colors
def extract_and_export_data(filename, output_filename=None):
    # Load events from the JSON file
    events = load_json(filename)
    
    # Load coordinates
    coordinates = load_coordinates(events, True)
    
    # Extract click events
    click_events = filter_clicks(events)
    
    # Extract colors and filter unique colors
    expected_colors = extract_colors_from_clicks(click_events)
    unique_colors = filter_duplicate_colors(expected_colors)
    
    # If output_filename is not provided, create one based on input filename
    if output_filename is None:
        output_filename = f"{os.path.splitext(filename)[0]}_coordinate_and_color_data.txt"

    # Export the data to text file
    with open(output_filename, 'w') as file:
        # Write coordinates
        file.write(f"{filename} coordinate and color data:\n\n")
        
        file.write("Coordinates:\n")
        for coord in coordinates:
            file.write(f"{coord[0]}, {coord[1]}\n")

        file.write("\nUnique Colors:\n")
        
        # Format unique colors as a single line
        formatted_colors = ", ".join(f"({color[0]}, {color[1]}, {color[2]})" for color in unique_colors)
        file.write(f"[{formatted_colors}]\n")

    print(f"Data exported to {output_filename}")


def find_and_move_to_color(color_samples, tolerance=10, region=None, sample_count=100):
    """
    Move the mouse to the first screen position that matches one of the given color samples.
    
    Parameters:
    - color_samples: List of tuples (R, G, B) representing color samples to search for.
    - tolerance: Tolerance level for color matching.
    """
    screen = pyautogui.screenshot(region=region)
    pixel_map = screen.load()
    width, height = screen.size

    sample_positions = [(random.randint(0, width - 1), random.randint(0, height - 1)) for _ in range(sample_count)]

    for x, y in sample_positions:
        pixel_color = pixel_map[x, y]
        for color in color_samples:
            if are_colors_similar(pixel_color, color, tolerance):
                print(f"Color match, Pixel color: {pixel_color}, found at ({x}, {y})")
                print(f"  Matches sample color: {color}")
                pyautogui.moveTo(x, y)
                # display_color(pixel_color)
                return  # Exit after the first match is found

    print("No matching color found on the screen.")


def display_color(color):
    """
    Create and display a plot with a solid color.

    Parameters:
    - color: A tuple (R, G, B) representing the RGB color to display.
    """
    normalized_color = tuple(component / 255.0 for component in color)  # Move the mouse to the matching color

    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Create a square patch with the color
    square = patches.Rectangle((0, 0), 1, 1, color=normalized_color)
    ax.add_patch(square)
    
    # Set limits and aspect
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    
    # Remove axis
    ax.axis('off')
    
    # Display the plot
    plt.show()

def main():
   
    # extract_and_export_data("hard_color_sample.json")
    # filename = 'hard_color_sample_2.json'
    # unique_colors = [(129, 134, 8), (195, 145, 136), (196, 149, 141), (78, 51, 46), (163, 118, 98), (163, 114, 75), (198, 160, 142), (161, 110, 71), (170, 110, 100)]

    # checks against unique colors
    # process_coordinates("hard_color_sample_2.json")
    # check_colors_and_click(filename, unique_colors, match_by_index=False, click_delay=0.1, tolerance=10)


    color_samples = [(129, 134, 8), (195, 145, 136), (196, 149, 141), (78, 51, 46), (163, 118, 98), (163, 114, 75), (198, 160, 142), (161, 110, 71), (170, 110, 100)]
    find_and_move_to_color(color_samples, tolerance=10, sample_count=100)








if __name__ == "__main__":
    main()

 