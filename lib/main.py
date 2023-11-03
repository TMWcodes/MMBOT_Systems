import pyautogui
import time

def main():
    # initialize
    pyautogui.FAILSAFE = True

    print("starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
  
        time.sleep(1)
    print("Go")

    pyautogui.keyDown('right')
    time.sleep(1)
    pyautogui.keyUp('right')
    print("Done")

# main()

def AKsilver(coordinates_list):
    # Delay before starting
    time.sleep(5)

    # Iterate through the list and move to each coordinate and click
    for coords in coordinates_list:
        x, y = coords['x'], coords['y']
        pyautogui.moveTo(x, y, duration=1)  # Move to the coordinate
        pyautogui.click()  # Click at the current position

    # Optional delay after clicking
        time.sleep(10)

# Define the list of coordinates
coordinates_list = [{'x': 1435, 'y': 758},
                   {'x': 1376, 'y': 696},
                   {'x': 1475, 'y': 302},
                   {'x': 1444, 'y': 763}]

# Call the AKsilver function
AKsilver(coordinates_list)