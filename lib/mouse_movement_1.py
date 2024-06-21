

import pyautogui
import random
import numpy as np
import time
from scipy import interpolate
from scipy.interpolate import splprep 
import math


pyautogui.MINIMUM_DURATION = 0.1
pyautogui.MINIMUM_SLEEP = 0.05
pyautogui.PAUSE = 0.1

# Function to generate random control points for mouse movement


def generate_control_points(start_position, end_position):
    # Randomly select the number of control points (between 3 and 5)
    cp = random.randint(3, 5)
    
    # Unpack start and end positions
    x1, y1 = start_position
    x2, y2 = end_position

    # Generate control points along the x and y axes
    x = np.linspace(x1, x2, num=cp, dtype='int')
    y = np.linspace(y1, y2, num=cp, dtype='int')

    # Add randomness to control points to create a more natural movement
    RND = 32
    xr = [random.randint(-RND, RND) for _ in range(cp)]
    yr = [random.randint(-RND, RND) for _ in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0  # Ensure start and end points are fixed
    x += xr
    y += yr

    return x, y

# Function to move the mouse cursor with easing effect between given points
def move_mouse_with_easing(points, duration, easing_function):
    # Simulate mouse button press
    # pyautogui.mouseDown()
    # Move the mouse cursor to each point with specified duration and easing function
    for point in points:
        pyautogui.moveTo(point[0], point[1], duration, easing_function)
        time.sleep(0.05)  # Adjust sleep time if needed for smoother movement
    # Release the mouse button
    # pyautogui.mouseUp()


def generate_spline_path(start_position, end_position):
  
    # Generate control points for mouse movement
    x, y = generate_control_points(start_position, end_position)
    # Determine the degree of the spline interpolation
    degree = 3 if len(x) > 3 else len(x) - 1
    # Perform spline interpolation on the generated control points
    tck, u = interpolate.splprep([x, y], k=degree)
    # Determine the parameter values (u) for interpolation based on distance between control points
    u = np.linspace(0, 1, num=2 + int(math.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2) / 50.0))
    # Evaluate the spline at the given parameter values to get interpolated points
    points = interpolate.splev(u, tck)
    return points

# #####BREAK######

def create_bezier_path(start_pos, end_pos, num_control_points=4, randomness=10, degree=3):

  x1, y1 = start_pos
  x2, y2 = end_pos

  # Distribute control points evenly
  x = np.linspace(x1, x2, num=num_control_points, dtype='int')
  y = np.linspace(y1, y2, num=num_control_points, dtype='int')

  # Randomize inner points a bit
  xr = [random.randint(-randomness, randomness) for k in range(num_control_points)]
  yr = [random.randint(-randomness, randomness) for k in range(num_control_points)]
  xr[0] = yr[0] = xr[-1] = yr[-1] = 0  # Fix first and last points
  x += xr
  y += yr

  # Ensure degree is valid
  degree = min(degree, num_control_points - 1)

  # Approximate using Bezier spline
  tck, u = splprep([x, y], k=degree)

  # Sample points along the curve based on distance
  distance = point_dist(x1, y1, x2, y2)
  num_points = 2 + int(distance / 50.0)
  u = np.linspace(0, 1, num=num_points)
  points = interpolate.splev(u, tck)

  return list(zip(*(i.astype(int) for i in points)))

def point_dist(x1, y1, x2, y2):
  """
  Calculates the Euclidean distance between two points.
  """
  return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
