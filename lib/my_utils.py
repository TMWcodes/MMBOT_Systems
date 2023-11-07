import pyautogui
import time

def capture_coords(count, wait):
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

capture_coords(4, 20)
    # => [ { x: 1329, y: 541 }, { x: 1386, y: 603 }, { x: 1420, y: 690 } ]