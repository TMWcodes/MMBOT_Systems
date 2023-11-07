import pyautogui
import time
import random

def main():
    # initialize
    pyautogui.FAILSAFE = True
    # ten second count down
    print("starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
  
        time.sleep(1)
    print("Go")

    # change camera to birds eye view 
    pyautogui.keyDown('up')
    time.sleep(2)
    pyautogui.keyUp('up')
    print("Done")

# main()
def bv_coal():
    coal_coords = [{'x': 1431, 'y': 586}, {'x': 1519, 'y': 587}, {'x': 1467, 'y': 685}, {'x': 1244, 'y': 405}]
    time.sleep(5)
    while True:
        # Iterate through the list and move to each coordinate and click
        for coords in coal_coords:
            x, y = coords['x'], coords['y']

            # Add random offsets to the target coordinates
            x += random.randint(-5, 5)  # Adjust the offset range as needed
            y += random.randint(-5, 5)  # Adjust the offset range as needed

            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)  # Move to the coordinate with easeInQuad
            pyautogui.click()  # Click at the current position

            # Add a delay after clicking
            time.sleep(20)  # Adjust this delay as needed

        # Wait for 30 seconds before running the loop again
        time.sleep(1)  # Adjust 
        
def vr_silver(coordinates_list):
    # Delay before starting
    time.sleep(5)

    while True:
        # Iterate through the list and move to each coordinate and click
        for coords in coordinates_list:
            x, y = coords['x'], coords['y']

            # Add random offsets to the target coordinates
            x += random.randint(-5, 5)  # Adjust the offset range as needed
            y += random.randint(-5, 5)  # Adjust the offset range as needed

            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)  # Move to the coordinate with easeInQuad
            pyautogui.click()  # Click at the current position

            # Add a delay after clicking
            time.sleep(12)  # Adjust this delay as needed

        # Wait for 30 seconds before running the loop again
        time.sleep(35)  # Adjust this delay as needed
# Define the list of coordinates
coordinates_list = [
                   {'x': 1435, 'y': 758},
                   {'x': 1376, 'y': 696},
                   {'x': 1475, 'y': 302},
                   ]
def fl_smelt():
    route_to =[{'x': 1425, 'y': 590 + random.randint(-5, 5)}, {'x': 1254, 'y': 363}, {'x': 1879, 'y': 64}, {'x': 1897, 'y': 124}, {'x': 1848, 'y': 156}, {'x': 1629, 'y': 519}]
    route_back = [{'x': 1820, 'y': 76}, {'x': 1771, 'y': 109}, {'x': 1797, 'y': 165}, {'x': 1425, 'y': 676}]
    for point in route_to:
        x, y = point['x'], point['y']
        print(f'moving mouse to {x},{y}')
        pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)  # Move to the position
        time.sleep(1)  # Wait for 1 second to allow the mouse to move
        pyautogui.click()  # Click the mouse
        time.sleep(12)  # Wait for 5 seconds before th
    # smelting break
    time.sleep(90)

    for point in route_back:
        x, y = point['x'], point['y']
        print(f'moving mouse to {x},{y}')
        pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)  # Move to the position
        time.sleep(1)  # Wait for 1 second to allow the mouse to move
        pyautogui.click()  # Click the mouse
        time.sleep(12)  
# Call the AKsilver function
# vr_silver(coordinates_list)
bv_coal()
# main()

# fl_smelt()