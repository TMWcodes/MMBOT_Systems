import pyautogui
import time
import random
from my_utils import holdKey


def main():
    # initialize
   initialize_pyautogui()
   count_down_timer()
   holdKey('up', 2)
    # change camera to birds eye view 
   

def initialize_pyautogui():
     pyautogui.FAILSAFE = True

def count_down_timer():
        # ten second count down
    print("starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
  
        time.sleep(1)
    print("Go")



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
            random_variation = random.uniform(-0.3 * base_wait_time, 0.3 * base_wait_time)
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

bank_coords = {'silver ore': {'x': 1254, 'y': 145},'silver bar': {'x': 1161, 'y': 179} }

def fl_furnace(item):
    position = bank_coords[item]
    turn_counter = 0
    while True:
        base_wait_time = 13

        route_a = [position, {'x': 1853, 'y': 81}, {'x': 1872, 'y': 79}, {'x': 1883, 'y': 124}, {'x': 1848, 'y': 140}, {'x': 1737, 'y': 574}] #worked from B1
        route_a2 = [position, {'x': 1879, 'y': 64}, {'x': 1897, 'y': 124}, {'x': 1849, 'y': 133}, {'x': 1740, 'y': 520}] #worked from B1
      
        route_b = [{'x': 1823, 'y': 85}, {'x': 1812, 'y': 92}, {'x': 1799, 'y': 97}, {'x': 1817, 'y': 136}, {'x': 1818, 'y': 127}, {'x': 1429, 'y': 776}]
        route_b2 = [{'x': 1852, 'y': 89}, {'x': 1829, 'y': 141}, {'x': 1791, 'y': 102}, {'x': 1797, 'y': 123}, {'x': 1819, 'y': 73}, {'x': 1818, 'y': 111}, {'x': 1430, 'y': 856}] 
                
        switch_every_x_turns = 2  # Adjust this value as needed

    
        print(f'turn counter {turn_counter}')
        print('heading to furnace')
        time.sleep(1)
        print('heading to furnace')
        selected_route = 'route_a2' if turn_counter % switch_every_x_turns == 0 else 'route_a'
        print(f'Choosing {selected_route}')
        for point in (route_a2 if turn_counter % switch_every_x_turns == 0 else route_a):
            x, y = point['x'], point['y']
            print(f'moving mouse to {x},{y}')
            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)  # Move to the position
            time.sleep(1)  # Wait for 1 second to allow the mouse to move
            pyautogui.click()  # Click the mouse
            random_variation = random.uniform(-0.2 * base_wait_time, 0.2 * base_wait_time)
            wait_time = base_wait_time + random_variation
            # print(f'Wait time is {wait_time}')
            time.sleep(wait_time)
            
        print('pressing space')
        pyautogui.press('space')

        ## smelting
        print('smelting break')
        if (item == "silver bar"): 
            print("sleeping 60")
            time.sleep(60)
        else:
            print("sleeping 90")
            time.sleep(90)

        # return
        print('heading to bank')
        if turn_counter % switch_every_x_turns == 0:
            selected_route = route_b2
            print('Choosing route_b2')
        else:
            selected_route = route_b
            print('Choosing route_b')
        
        for point in selected_route:
            x, y = point['x'], point['y']
            print(f'moving mouse to {x},{y}')
            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInQuad)  # Move to the position
            time.sleep(1)  # Wait for 1 second to allow the mouse to move
            pyautogui.click()
            random_variation = random.uniform(-0.2 * base_wait_time, 0.2 * base_wait_time)  # Click the 
            wait_time = base_wait_time + random_variation
            # print(f'Wait time is {wait_time}')
            time.sleep(wait_time) 

        turn_counter += 1
        print(turn_counter)
        print('banking inventory')
        time.sleep(2)
        # pyautogui.click(1513, 827) # all
        pyautogui.click(1793, 761) # second inv pos.



