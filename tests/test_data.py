import pytest
from unittest import mock
from lib.data import (
    load_json, load_coordinates_from_dicts, merge_json_files,
    filter_clicks, compare_entries, calculate_time_differences, compute_statistics,
    compute_time_stats, calculate_shannon_entropy, count_repeated_sequences,
    detect_repeated_sequences, plot_autocorrelation, flatten_json, unflatten_json,
    json_to_csv, csv_to_json
)
import numpy as np
from scipy.stats import entropy
import pandas as pd
import os

# Test load_json function
def test_load_json_from_recordings():
    with mock.patch("builtins.open", mock.mock_open(read_data='{"key": "value"}')), \
         mock.patch("os.path.exists", return_value=True), \
         mock.patch("os.path.join", return_value="recordings/test.json"):
        
        result = load_json("test.json")
        assert result == {"key": "value"}

def test_load_json_from_log_records():
    with mock.patch("builtins.open", mock.mock_open(read_data='{"key": "value"}')), \
         mock.patch("os.path.exists", side_effect=[False, True]), \
         mock.patch("os.path.join", return_value="log_records/test.json"):
        
        result = load_json("test.json")
        assert result == {"key": "value"}

def test_load_json_file_not_found():
    with mock.patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_json("nonexistent.json")

# Test load_coordinates function
# def test_load_coordinates():
#     events = [
#         {"pos": [1, 2], "type": "click"},
#         {"pos": [3, 4], "type": "move"},
#         {"pos": [5, 6], "type": "click"}
#     ]
#     result = load_coordinates(events, ignore_moves=True)
#     expected = np.array([[1, 2], [5, 6]])
#     assert np.array_equal(result, expected)

def test_load_coordinates_from_dicts():
    coordinates_list = [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
    result = load_coordinates_from_dicts(coordinates_list)
    expected = np.array([[1, 2], [3, 4]])
    assert np.array_equal(result, expected)

# Test merge_json_files function
def test_merge_json_files():
    filenames = ["file1.json", "file2.json"]
    with mock.patch("builtins.open", mock.mock_open(read_data='[{"time": 1}, {"time": 2}]')), \
         mock.patch("os.path.exists", side_effect=[True, True]), \
         mock.patch("os.path.join", side_effect=lambda dir, file: file):
        
        result = merge_json_files(filenames)
        assert len(result) == 4
        assert result[0]['time'] == 1
        assert result[2]['time'] == 3

# Test filter_clicks function
def test_filter_clicks():
    events = [
        {"type": "click"},
        {"type": "move"},
        {"type": "click"}
    ]
    result = filter_clicks(events)
    expected = [{"type": "click"}, {"type": "click"}]
    assert result == expected

# Test compare_entries function
def test_compare_entries():
    data1 = [
        {"time": 1.0, "pos": [1, 2], "color": [255, 0, 0]},
        {"time": 2.0, "pos": [3, 4], "color": [0, 255, 0]}
    ]
    data2 = [
        {"time": 1.0, "pos": [1, 2], "color": [255, 0, 0]},
        {"time": 2.5, "pos": [3, 5], "color": [0, 0, 255]}
    ]
    result = compare_entries(data1, data2, compare_time=True, compare_color=True, compare_position=True)
    expected = [
        "Index 1:\n  File 1 - Time: 2.0, Pos: [3, 4], Color: [0, 255, 0]\n  File 2 - Time: 2.5, Pos: [3, 5], Color: [0, 0, 255]"
    ]
    assert result == expected

# Test calculate_time_differences function
def test_calculate_time_differences():
    events = [
        {"time": 1},
        {"time": 3},
        {"time": 6}
    ]
    result = calculate_time_differences(events)
    expected = [2, 3]
    assert result == expected

# Test compute_statistics function
def test_compute_statistics():
    time_diffs = [1, 2, 3, 4, 5]
    min_time, max_time, avg_time, std_time = compute_statistics(time_diffs)
    assert min_time == 1
    assert max_time == 5
    assert avg_time == 3
    assert np.isclose(std_time, np.std(time_diffs))

# Test compute_time_stats function
def test_compute_time_stats():
    with mock.patch("lib.data.load_json", return_value=[
        {"time": 1.0},
        {"time": 3.0},
        {"time": 5.0},
        {"time": 7.0}
    ]):
        min_time, max_time, avg_time, std_time = compute_time_stats("test.json")
        time_diffs = [3.0 - 1.0, 5.0 - 3.0, 7.0 - 5.0]
        assert min_time == min(time_diffs)
        assert max_time == max(time_diffs)
        assert avg_time == sum(time_diffs) / len(time_diffs)
        assert std_time == np.std(time_diffs)

# Test calculate_shannon_entropy function
def test_calculate_shannon_entropy():
    sequence = np.array([[1, 2], [1, 2], [3, 4]])
    expected_entropy = entropy([2/3, 1/3])
    assert np.isclose(calculate_shannon_entropy(sequence), expected_entropy)

# Test detect_repetition function
# def test_detect_repetition():
#     coordinates = np.array([[1, 2], [1, 2], [3, 4], [1, 2]])
#     threshold = 0.5
#     result = detect_repetition(coordinates, threshold)
#     expected = [(1, 2)]
#     assert result == expected

# Test count_repeated_sequences function
def test_count_repeated_sequences():
    coordinates = np.array([[1499, 741], [1499, 741], [1499, 741], [1400, 735], [1499, 741]])
    result = count_repeated_sequences(coordinates, min_sequence_length=2)
    expected = 1  # Adjust this based on actual logic; verify if only one sequence is counted
    assert result == expected

# Test detect_repeated_sequences function
# def test_detect_repeated_sequences():
#     events = [
#         {"time": 0.0, "type": "click", "pos": [1425, 469]},
#         {"time": 1.0, "type": "click", "pos": [1425, 469]},
#         {"time": 2.0, "type": "click", "pos": [1430, 470]},
#         {"time": 3.0, "type": "click", "pos": [1425, 469]},
#         {"time": 4.0, "type": "click", "pos": [1425, 469]},
#         {"time": 5.0, "type": "click", "pos": [1430, 470]},
#         {"time": 6.0, "type": "click", "pos": [1425, 469]},
#         {"time": 7.0, "type": "click", "pos": [1425, 469]},
#         {"time": 8.0, "type": "click", "pos": [1430, 470]},
#         {"time": 9.0, "type": "click", "pos": [1500, 480]},  # Not part of the repeated sequence
#         {"time": 10.0, "type": "click", "pos": [1425, 469]},
#         {"time": 11.0, "type": "click", "pos": [1425, 469]},
#         {"time": 12.0, "type": "click", "pos": [1430, 470]},
#         {"time": 13.0, "type": "click", "pos": [1425, 469]}
#     ]

#     coordinates = load_coordinates(events)
#     expected_repeated_sequences = {
#         ((1425, 469), (1425, 469), (1430, 470)): [0, 3, 6, 10],
#         ((1425, 469), (1430, 470), (1425, 469)): [1, 4, 11],
#         ((1430, 470), (1425, 469), (1425, 469)): [2, 5]
#     }

#     repeated_sequences = detect_repeated_sequences(coordinates)
#     assert repeated_sequences == expected_repeated_sequences, f"Expected {expected_repeated_sequences}, but got {repeated_sequences}"


# Test plot_autocorrelation function
def test_plot_autocorrelation():
    sequence = np.array([[1, 2], [3, 4]])
    repetitions = 2
    result = plot_autocorrelation(sequence, repetitions)
    assert isinstance(result, float)  # Check that a metric value is returned

# Test flatten_json function
def test_flatten_json():
    nested_json = {"a": {"b": [1, 2, 3]}}
    result = flatten_json(nested_json)
    expected = {"a_b": '[1, 2, 3]'}
    assert result == expected

# Test unflatten_json function
def test_unflatten_json():
    flat_json = {"a_b": '[1, 2, 3]'}
    result = unflatten_json(flat_json)
    expected = {"a": {"b": [1, 2, 3]}}
    assert result == expected

# Test json_to_csv function
def test_json_to_csv():
    json_filename = 'test.json'
    csv_filename = 'test/test.csv'
    
    with mock.patch("lib.data.load_json", return_value=[{"a": 1, "b": 2}]), \
         mock.patch("pandas.DataFrame.to_csv") as mock_to_csv:
        
        json_to_csv(json_filename, csv_filename)
        mock_to_csv.assert_called_once()

# Test csv_to_json function
def test_csv_to_json():
    csv_filename = 'test/test.csv'
    json_filename = 'test/test.json'
    
    with mock.patch("pandas.read_csv", return_value=pd.DataFrame([{"a": 1, "b": 2}])), \
         mock.patch("builtins.open", mock.mock_open()) as mock_open:
        
        csv_to_json(csv_filename, json_filename)
        mock_open.assert_called_once()
