# import pytest 
from lib.utils import capture_coords

def test_capture_coords():
    # Define test input values
    count = 1
    wait = 1
    # Run the capture_coords function
    captured_positions = capture_coords(count, wait)
    # captured positions should have the correct length
    assert len(captured_positions) == count

    # Check if the time.sleep call has been invoked with the correct arguments
   
def test_capture_coords_returns_list():
    captured_positions = capture_coords(1, 1)
    assert isinstance(captured_positions, list)

def test_capture_coords_list_contains_dicts():
    captured_positions = capture_coords(1, 1)
    for item in captured_positions:
        assert isinstance(item, dict)

