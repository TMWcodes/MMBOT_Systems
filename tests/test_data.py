import pytest
import os
import json
from unittest import mock
from lib.data import load_json, load_coordinates, combine_json, calculate_shannon_entropy, detect_repetition,detect_repeated_sequences ,calculate_time_differences, cluster, plot_autocorrelation
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.stats import entropy
from collections import Counter
import pandas as pd


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

def test_combine_json():
    mock_open_file1 = mock.mock_open(read_data='[{"key": "value1"}]')
    mock_open_file2 = mock.mock_open(read_data='[{"key": "value2"}]')
    mock_open_output = mock.mock_open()

    with mock.patch("builtins.open", side_effect=[mock_open_file1.return_value, mock_open_file2.return_value, mock_open_output.return_value]), \
         mock.patch("os.path.exists", return_value=True), \
         mock.patch("os.path.join", return_value="recordings/combined_file.json"):

        combine_json("file1.json", "file2.json")

        # Join all the args into a single string to assert the complete output
        written_content = "".join(call.args[0] for call in mock_open_output().write.call_args_list)
        expected_content = '[\n  {\n    "key": "value1"\n  },\n  {\n    "key": "value2"\n  }\n]'

        assert written_content == expected_content


def test_combine_json_file_not_found(capsys):
    with mock.patch("os.path.exists", side_effect=[False, True]), \
         mock.patch("os.path.join", return_value="recordings/file1.json"):
        
        combine_json("file1.json", "file2.json")
        
        captured = capsys.readouterr()
        assert "Error: recordings/file1.json not found." in captured.out

### data analysis ##

def test_calculate_shannon_entropy():
    # Test case 1: All points are the same (entropy should be 0)
    coordinates = np.array([[1425, 469], [1425, 469], [1425, 469], [1425, 469]])
    expected_entropy = 0  # All points are identical, entropy is zero
    assert np.isclose(calculate_shannon_entropy(coordinates), expected_entropy, atol=1e-6)

    # Test case 2: Two different points (entropy should reflect equal distribution)
    coordinates = np.array([[1425, 469], [1425, 470], [1425, 469], [1425, 470]])
    expected_entropy = entropy([0.5, 0.5])  # Two types of points, equal probability
    assert np.isclose(calculate_shannon_entropy(coordinates), expected_entropy, atol=1e-6)

    # Test case 3: Multiple different points with equal frequency
    coordinates = np.array([[1425, 469], [1425, 470], [1426, 471], [1427, 472],
                            [1425, 469], [1425, 470], [1426, 471], [1427, 472]])
    expected_entropy = entropy([0.25, 0.25, 0.25, 0.25])  # Four types of points, equal probability
    assert np.isclose(calculate_shannon_entropy(coordinates), expected_entropy, atol=1e-6)

    # Test case 4: Random points (entropy should be calculated correctly)
    coordinates = np.random.randint(0, 2000, size=(100, 2))
    unique, counts = np.unique(coordinates, axis=0, return_counts=True)
    probs = counts / len(coordinates)
    expected_entropy = entropy(probs)
    assert np.isclose(calculate_shannon_entropy(coordinates), expected_entropy, atol=1e-6)

def test_calculate_time_differences():
    events = [
        {"time": 0.3036661148071289},
        {"time": 1.777268409729004},
        {"time": 2.977268409729004}
    ]
    expected = [1.473602294921875, 1.2]
    result = calculate_time_differences(events)
    assert result == pytest.approx(expected, rel=1e-9), f"Expected {expected}, but got {result}"


def test_detect_repetition():
    coordinates = np.array([
        [1425, 469],
        [1425, 469],
        [1426, 470],
        [1425, 469]
    ])
    threshold = 0.25
    expected = [(1425, 469)]
    result = detect_repetition(coordinates, threshold)
    assert result == expected, f"Expected {expected}, but got {result}"

def test_cluster():
    coordinates = np.array([
        [1425, 469],
        [1425, 469],
        [1426, 470],
        [1425, 469],
        [1427, 471]
    ])
    num_clusters = 2
    kmeans = cluster(coordinates, num_clusters)
    assert len(kmeans.cluster_centers_) == num_clusters

def test_calculate_autocorrelation_metric():
    sequence = np.array([
        [1425, 469],
        [1426, 470],
        [1425, 469],
        [1426, 470]
    ])
    repetitions = 2

    # Replace with the correct expected metric based on your manual calculation
    expected_metric = 0.0053614198790852274 # Example placeholder value

    result = plot_autocorrelation(sequence, repetitions)
    assert abs(result - expected_metric) < 1e-6, f"Expected {expected_metric}, but got {result}"

def test_detect_repeated_sequences():
    events = [
        {"time": 0.0, "type": "click", "pos": [1425, 469]},
        {"time": 1.0, "type": "click", "pos": [1425, 469]},
        {"time": 2.0, "type": "click", "pos": [1430, 470]},
        {"time": 3.0, "type": "click", "pos": [1425, 469]},
        {"time": 4.0, "type": "click", "pos": [1425, 469]},
        {"time": 5.0, "type": "click", "pos": [1430, 470]},
        {"time": 6.0, "type": "click", "pos": [1425, 469]},
        {"time": 7.0, "type": "click", "pos": [1425, 469]},
        {"time": 8.0, "type": "click", "pos": [1430, 470]},
        {"time": 9.0, "type": "click", "pos": [1500, 480]},  # Not part of the repeated sequence
        {"time": 10.0, "type": "click", "pos": [1425, 469]},
        {"time": 11.0, "type": "click", "pos": [1425, 469]},
        {"time": 12.0, "type": "click", "pos": [1430, 470]},
        {"time": 13.0, "type": "click", "pos": [1425, 469]}
    ]

    coordinates = load_coordinates(events)
    expected_repeated_sequences = {
        ((1425, 469), (1425, 469), (1430, 470)): [0, 3, 6, 10],
        ((1425, 469), (1430, 470), (1425, 469)): [1, 4, 11],
        ((1430, 470), (1425, 469), (1425, 469)): [2, 5]
    }

    repeated_sequences = detect_repeated_sequences(coordinates)
    assert repeated_sequences == expected_repeated_sequences, f"Expected {expected_repeated_sequences}, but got {repeated_sequences}"