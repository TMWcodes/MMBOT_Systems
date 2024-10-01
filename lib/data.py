import numpy as np
import matplotlib.pyplot as plt
import json
import os
from scipy.stats import entropy
from collections import Counter
import pandas as pd
from itertools import islice
from data_loader import load_json



def filter_clicks(events):
    return [event for event in events if event.get('type') in ['mouseDown', 'mouseUp']]

def compare_entries(data1, data2, compare_time=False, compare_color=True, compare_position=True):
    differences = []
    
    for i, (entry1, entry2) in enumerate(zip(data1, data2)):
        pos1, color1, time1, type1 = entry1.get('pos'), entry1.get('color'), entry1.get('time'), entry1.get('type')
        pos2, color2, time2, type2 = entry2.get('pos'), entry2.get('color'), entry2.get('time'), entry2.get('type')

        pos_diff = pos1 != pos2 if compare_position else False
        color_diff = color1 != color2 if compare_color else False
        time_diff = time1 != time2 if compare_time else False
        type_diff = type1 != type2  # Always compare the type

        if pos_diff or color_diff or time_diff or type_diff:
            diffs_file1 = []
            diffs_file2 = []

            if type_diff:
                diffs_file1.append(f"Type: {type1}")
                diffs_file2.append(f"Type: {type2}")
            if compare_time and time_diff:
                diffs_file1.append(f"Time: {time1}")
                diffs_file2.append(f"Time: {time2}")
            if compare_position and pos_diff:
                diffs_file1.append(f"Pos: {pos1}")
                diffs_file2.append(f"Pos: {pos2}")
            if compare_color and color_diff:
                diffs_file1.append(f"Color: {color1}")
                diffs_file2.append(f"Color: {color2}")

            differences.append(f"Index {i}: \"type\": \"{type1}\"\n  File 1 - {', '.join(diffs_file1)}\n  File 2 - {', '.join(diffs_file2)}")

    return differences
# Calculate time differences between consecutive events with an option to ignore move actions
def calculate_mouse_click_differences(events):
    time_diffs = []
    
    # Filter for only mouseDown and mouseUp events
    filtered_events = [event for event in events if event['type'] in ['mouseDown', 'mouseUp']]
    
    for i in range(1, len(filtered_events)):
        if filtered_events[i-1]['type'] == 'mouseDown' and filtered_events[i]['type'] == 'mouseUp':
            time_diff = filtered_events[i]['time'] - filtered_events[i-1]['time']
            time_diffs.append(time_diff)
    
    return time_diffs

def calculate_time_differences_between_mousedown(events):
    time_diffs = []
    mousedown_events = [event for event in events if event.get('type') == 'mouseDown']
    
    for i in range(1, len(mousedown_events)):
        time_diff = mousedown_events[i]['time'] - mousedown_events[i-1]['time']
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

def compute_click_time_stats(filename):
    events = load_json(filename)
    
    # Get time differences for clicks (mouseDown -> mouseUp)
    click_time_diffs = calculate_mouse_click_differences(events)
    min_click, max_click, avg_click, std_click = compute_statistics(click_time_diffs) if click_time_diffs else (None, None, None, None)

    # Get time differences between mouseDown events (mouseDown -> mouseDown)
    mousedown_time_diffs = calculate_time_differences_between_mousedown(events)
    min_mousedown, max_mousedown, avg_mousedown, std_mousedown = compute_statistics(mousedown_time_diffs) if mousedown_time_diffs else (None, None, None, None)

    # Return both sets of stats instead of printing
    return (min_click, max_click, avg_click, std_click), (min_mousedown, max_mousedown, avg_mousedown, std_mousedown)



# def main():
    
#   
# if __name__ == "__main__":
#     main()