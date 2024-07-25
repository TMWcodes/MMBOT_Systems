import pytest 
import random

from lib.my_utils import vary_coordinates

# Mock random.uniform to make tests predictable
# Mock random.uniform to make tests predictable
def mock_uniform(a, b):
    # Return a predictable value for testing (e.g., midpoint)
    return (a + b) / 2

def test_vary_coordinates():
    # Replace random.uniform with a mock
    original_uniform = random.uniform
    random.uniform = mock_uniform

    x, y, variation = 10, 20, 0.1
    x_variation, y_variation = vary_coordinates(x, y, variation)

    # Calculate expected variation range
    expected_x = int(variation * x * (mock_uniform(0, 1) - 0.5))
    expected_y = int(variation * y * (mock_uniform(0, 1) - 0.5))

    print(f"x_variation: {x_variation}, expected_x: {expected_x}")
    print(f"y_variation: {y_variation}, expected_y: {expected_y}")

    # Check that the variations are within the expected range
    assert -abs(expected_x) <= x_variation <= abs(expected_x)
    assert -abs(expected_y) <= y_variation <= abs(expected_y)

    # Restore the original function
    random.uniform = original_uniform

def test_vary_coordinates_zero_variation():
    x, y, variation = 10, 20, 0
    x_variation, y_variation = vary_coordinates(x, y, variation)

    print(f"x_variation: {x_variation}")
    print(f"y_variation: {y_variation}")

    # With zero variation, the output should be (0, 0)
    assert x_variation == 0
    assert y_variation == 0