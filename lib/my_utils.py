import pyautogui
import time
import random

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
    print(f"capturing coordinates for {seconds} seconds")
    time.sleep(2)
    for i in range(0,seconds):
        print(pyautogui.position())
        time.sleep(3)
    
def vary_coordinates(x, y, variation):
    x_variation = random.uniform(-variation * x, variation * x)
    y_variation = random.uniform(-variation * y, variation * y)
    return x_variation, y_variation

# checks colour, checks against expected colour, checks methods against eachother
def check_color(coordinates=(1741,95), expected_color=(33, 37, 43)):
    # method 1
    im = pyautogui.screenshot()
    pixel_color = im.getpixel((coordinates))
    # method 2
    pixel = pyautogui.pixel(*coordinates)
    
    # method match
    if pixel_color == pixel:
        pass
    else:
        print("too different pixel readings")

    # color match
    match = pyautogui.pixelMatchesColor(coordinates[0],coordinates[1], (expected_color))
    # print(result1)
    # print(result3)
    if match == False:
        print("does not match expected colour")
    else:
        print("colour match"
        )
    return pixel

    # => [ { x: 1329, y: 541 }, { x: 1386, y: 603 }, { x: 1420, y: 690 } ]


# data = capture_num_coords(1, 5)
# x_value = data[0]['x']
# print(f"x value: {x_value}")

# # Accessing and printing the 'y' value
# y_value = data[0]['y']
# print(f"y value: {y_value}")
# color = check_color((x_value, y_value))
# print(color)
#1741, 95 should be 176, 8 ,4 if not eat (click inventory slot 1), check color, repeat.
# empty health is 19,19,19
# special - 1771, 188 should be 53, 155, 181.