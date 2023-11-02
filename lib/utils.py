import pyautogui
import time

def capture_coords(count, wait):
    captured_positions = []
    time.sleep(3)  # Sleep for 3 seconds
    for i in range(count):
        mouse = pyautogui.position()
        captured_positions.append({"x": mouse[0], "y": mouse[1]})
        print(captured_positions)
        time.sleep(wait)
    return captured_positions

capture_coords(5, 1)
    # => [ { x: 1329, y: 541 }, { x: 1386, y: 603 }, { x: 1420, y: 690 } ]