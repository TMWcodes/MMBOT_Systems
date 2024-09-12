import pyautogui
import time

# checks colour, checks against expected colour, checks methods against eachother
def check_color(coordinates, delay=0.1):
    if not isinstance(coordinates, (tuple, list)) or len(coordinates) != 2:
        raise ValueError("Coordinates must be a tuple or list of two integers")
    
    x, y = coordinates
    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("Both coordinates must be integers")

    time.sleep(delay)
    im = pyautogui.screenshot()
    pixel_color= im.getpixel(coordinates)
    
    if pixel_color == (255, 0, 0):
        print("Red x recorded at", coordinates)
        pixel_color = pyautogui.pixel(x, y)
    elif pixel_color ==(255, 255, 255):
        print("white recorded at", coordinates)
        pixel_color = pyautogui.pixel(x, y)
    elif pixel_color ==(0, 0, 0):
        print("black recorded at", coordinates)
        pixel_color = pyautogui.pixel(x, y)

    return pixel_color

def compare_colors(coordinate, expected_color):
    """
    Compares the color at a given coordinate with the expected color.
    
    Parameters:
    - coordinate: A tuple (x, y) representing the screen coordinates.
    - expected_color: A tuple (R, G, B) representing the expected color.
    
    Returns:
    - bool: True if the color matches, False otherwise.
    """
    print(f"Checking color at coordinate: {coordinate}")
    print(f"Expected color: {expected_color}")

    # Validate coordinate
    if not (isinstance(coordinate, tuple) and len(coordinate) == 2 and all(isinstance(c, int) for c in coordinate)):
        print(f"Invalid coordinate format: {coordinate}")
        return False

    # Validate expected color
    if not (isinstance(expected_color, tuple) and len(expected_color) == 3 and all(isinstance(c, int) for c in expected_color)):
        print(f"Invalid color format: {expected_color}")
        return False

    try:
        # Retrieve the current color at the coordinate
        current_color = pyautogui.pixel(coordinate[0], coordinate[1])
        print(f"Actual color at {coordinate}: {current_color}")
        
        # Compare the current color with the expected color
        match = pyautogui.pixelMatchesColor(coordinate[0], coordinate[1], expected_color, tolerance=10)
    except Exception as e:
        print(f"Error checking color: {e}")
        return False

    if match:
        print(f"Color at {coordinate} matches expected value {expected_color}.")
    else:
        print(f"Color at {coordinate} does not match expected color {expected_color}.")

    return match


def are_colors_similar(color1, color2, tolerance):
    squared_distance = sum((comp1 - comp2) ** 2 for comp1, comp2 in zip(color1, color2))
    return squared_distance <= tolerance ** 2

def is_color_in_samples(color, samples, tolerance):
    for sample in samples:
        if are_colors_similar(color, sample, tolerance):
            return sample
    return None