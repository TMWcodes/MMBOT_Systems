import pyautogui
import random
import numpy as np
import time
from scipy import interpolate
from scipy.interpolate import splprep
import math
import threading

# Constants for movement
DEFAULT_DURATION = 0.05
DEFAULT_SLEEP = 0.01

# Function to move the mouse cursor with easing effect between given points
def move_mouse_with_easing(points, duration, easing_function):
    for point in points:
        pyautogui.moveTo(point[0], point[1], duration, easing_function)
        time.sleep(DEFAULT_SLEEP)  # Adjust sleep time for smoother movement

def threaded_mouse_movement(points, duration, easing_function):
    """
    Runs mouse movement in a separate thread to avoid GUI freezing.
    """
    threading.Thread(target=move_mouse_with_easing, args=(points, duration, easing_function)).start()

# Function to generate random control points for mouse movement
def generate_control_points(start_position, end_position):
    cp = random.randint(3, 5)  # Randomly select the number of control points
    x1, y1 = start_position
    x2, y2 = end_position
    x = np.linspace(x1, x2, num=cp, dtype='int')
    y = np.linspace(y1, y2, num=cp, dtype='int')
    RND = 32
    xr = [random.randint(-RND, RND) for _ in range(cp)]
    yr = [random.randint(-RND, RND) for _ in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0  # Ensure start and end points are fixed
    x += xr
    y += yr
    return x, y

def generate_spline_path(start_position, end_position):
    x, y = generate_control_points(start_position, end_position)
    degree = 3 if len(x) > 3 else len(x) - 1
    tck, _ = interpolate.splprep([x, y], k=degree)
    u = np.linspace(0, 1, num=2 + int(math.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2) / 50.0))
    points = interpolate.splev(u, tck)
    return points

def create_bezier_path(start_pos, end_pos, num_control_points=4, randomness=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    x = np.linspace(x1, x2, num=num_control_points, dtype='int')
    y = np.linspace(y1, y2, num=num_control_points, dtype='int')
    xr = [random.randint(-randomness, randomness) for _ in range(num_control_points)]
    yr = [random.randint(-randomness, randomness) for _ in range(num_control_points)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr
    degree = min(3, num_control_points - 1)  # Max degree of 3 for Bezier curves
    try:
        tck, _ = splprep([x, y], k=degree)
    except Exception as e:
        print(f"Error creating Bezier path with x: {x}, y: {y}, degree: {degree}. Error: {e}")
        return []  # Return an empty path on error
    distance = point_dist(x1, y1, x2, y2)
    num_points = 2 + int(distance / 50.0)
    u = np.linspace(0, 1, num=num_points)
    points = interpolate.splev(u, tck)
    return list(zip(*(i.astype(int) for i in points)))

def point_dist(x1, y1, x2, y2):
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
