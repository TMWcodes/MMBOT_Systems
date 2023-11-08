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
    coal_coords = {
        'rock1': [{'x': 1432, 'y': 591}, {'x': 1403, 'y': 615}, {'x': 1451, 'y': 636}],
        'rock2': [{'x': 1532, 'y': 607}, {'x': 1497, 'y': 624}, {'x': 1526, 'y': 655}],
        'rock3': [{'x': 1422, 'y': 682}, {'x': 1473, 'y': 699}, {'x': 1434, 'y': 719}],
        'rock4': [{'x': 1221, 'y': 376}, {'x': 1232, 'y': 399}, {'x': 1219, 'y': 419}]
    }
    time.sleep(5)
    while True:
        for rock, coords in coal_coords.items():
            print(f"Performing tasks for {rock}")

            coord_set = random.choice(coords)  # Choose a random coordinate set for the current rock
            x, y = coord_set['x'], coord_set['y']
            print(f'Moving mouse to {x},{y}')
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
            print(f'Moving rand mouse to {x},{y}')
            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)
            time.sleep(1)
            pyautogui.click()

            base_wait_time = 14
            random_variation = random.uniform(-0.2 * base_wait_time, 0.2 * base_wait_time)
            print(f'Variation is {random_variation}')
            wait_time = base_wait_time + random_variation
            print(f'Wait time is {wait_time}')
            time.sleep(wait_time)

        # Add a delay between rocks (adjust as needed)
        time.sleep(1)



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
# bv_coal()
# main()

fl_smelt()