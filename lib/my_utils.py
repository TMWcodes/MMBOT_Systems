import pyautogui
import time
import random

DELAY_BETWEEN_COMMANDS = 1.0
def holdKey(key, second =10):
    pyautogui.keyDown(key)
    time.sleep(second)
    pyautogui.keyUp(key)
    time.sleep(DELAY_BETWEEN_COMMANDS) 
    print("Done")

def initialize_pyautogui():
     pyautogui.FAILSAFE = True

def count_down_timer():
        # ten second count down
    print("starting", end="", flush=True)
    for i in range(0, 5):
        print(".", end="", flush=True)
        time.sleep(1)
    print("Go")

def capture_num_coords(count, wait):
    captured_positions = []
    print(f'waiting three second, then counting {count} positions, with a {wait} second interval')
    time.sleep(3)  # Sleep for 3 seconds
    for i in range(count):
        mouse = pyautogui.position()
        print(mouse)
        captured_positions.append({"x": mouse[0], "y": mouse[1]})
        print(captured_positions)
        time.sleep(wait)
    return captured_positions

def const_record_coords(seconds=20):
    print(f"capturing coordinates every 3 seconds for {seconds} seconds, after 2 seconds")
    time.sleep(2)
    for i in range(0,seconds):
        print(pyautogui.position())
        time.sleep(3)
    
def vary_coordinates(x, y, variation):
    x_variation = random.uniform(-variation * x, variation * x)
    y_variation = random.uniform(-variation * y, variation * y)
    return x_variation, y_variation

# checks colour, checks against expected colour, checks methods against eachother
def check_color(coordinates=(1741,95)):
    # method 1
    im = pyautogui.screenshot()
    pixel_color = im.getpixel((coordinates))
    # method 2 (redundancy)
    pixel = pyautogui.pixel(*coordinates)
    
    # method match
    if pixel_color == pixel:
        pass
    else:
        print("two different pixel readings")

    # color match
    
    return pixel

def compare_colors(coordinates=(1741,95), expected_color=(33, 37, 43)):
    match = pyautogui.pixelMatchesColor(coordinates[0],coordinates[1], (expected_color))
    # print(result1)
    # print(result3)
    if match == False:
        print("does not match expected color")
    else:
        print("color matches expected value."
        )

print(f"color = {check_color()}")
 