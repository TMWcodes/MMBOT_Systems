import pyautogui
import time
import random


    

def initialize_pyautogui():
     pyautogui.FAILSAFE = True

def count_down_timer():
        # ten second count down
    print("starting", end="", flush=True)
    for i in range(0, 5):
        print(".", end="", flush=True)
        time.sleep(1)
    print("Go")

def holdKey(key, second =10, delay=1):
    pyautogui.keyDown(key)
    time.sleep(second)
    pyautogui.keyUp(key)
    time.sleep(delay) 

def capture_coordinates(num_positions=None, duration=None, interval=3):
    """
    Capture mouse coordinates either for a fixed number of positions or for a fixed duration.
    
    Parameters:
    - num_positions: Number of coordinates to capture.
    - duration: Duration in seconds to capture coordinates.
    - interval: Time interval (in seconds) between captures.
    """
    if num_positions is None and duration is None:
        raise ValueError("Either 'num_positions' or 'duration' must be specified.")
    
    if num_positions is not None and duration is not None:
        raise ValueError("Specify only one of 'num_positions' or 'duration', not both.")

    captured_positions = []
    
    print("Starting capture...")
    
    if num_positions is not None:
        print(f"Capturing {num_positions} positions with a {interval}-second interval.")
        time.sleep(3)  # Initial delay
        for _ in range(num_positions):
            mouse = pyautogui.position()
            captured_positions.append({"x": mouse[0], "y": mouse[1]})
            print(f"Captured: {captured_positions[-1]}")
            time.sleep(interval)
    
    elif duration is not None:
        print(f"Capturing coordinates for {duration} seconds with a {interval}-second interval.")
        time.sleep(2)  # Initial delay
        start_time = time.time()
        while time.time() - start_time < duration:
            mouse = pyautogui.position()
            captured_positions.append({"x": mouse[0], "y": mouse[1]})
            print(f"Captured: {captured_positions[-1]}")
            time.sleep(interval)
    
    print(f"Capture complete. {len(captured_positions)} positions captured.")
    return captured_positions


# # percentage based variation
def vary_coordinates(x, y, variation):
    x_variation = int(random.uniform(-variation, variation) * x)
    y_variation = int(random.uniform(-variation, variation) * y)
    return x_variation, y_variation

# pixel based variation
# def vary_coordinates(x, y, variation):
#     x_variation = random.uniform(-variation, variation)  # Variation in pixel units
#     y_variation = random.uniform(-variation, variation)  # Variation in pixel units
#     new_x = int(x + x_variation)
#     new_y = int(y + y_variation)
    
#     # Debugging output to check the variation and result
#     print(f"Original position: ({x}, {y})")
#     print(f"Variation applied: ({x_variation}, {y_variation})")
#     print(f"New position with variation: ({new_x}, {new_y})")
    
#     return new_x, new_y