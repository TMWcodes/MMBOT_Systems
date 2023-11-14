import pyautogui
import os
from time import sleep

def screen_image():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "..", "images", "reddit_icon.PNG")
    res = pyautogui.locateOnScreen(image_path)
    if res is not None:
        print("Image found at:", res)
        print(pyautogui.center(res))
    else:
        print("Image not found.")
    print("sleeping for 3 seconds")
    sleep(3)

def write():
    subreddit_name = "r/ArtificialInteligence"
    # subreddit_name = pyautogui.prompt(text="", title="enter the channel name")
    # opens tab
    pyautogui.hotkey("ctrl", "t")
    sleep(1)
    # search 
    pyautogui.write("https://www.reddit.com/")
    sleep(1)
    pyautogui.hotkey("enter")
    sleep(4)
    search_bar = pyautogui.locateCenterOnScreen("..\images\search_icon.PNG")
    if search_bar is not None:
        print("Image found at:", search_bar)
        pyautogui.moveTo(search_bar, 1)
        pyautogui.click()
        pyautogui.write(subreddit_name)
    else:
        print("Image not found.")

      
def create_screenshot():
    filename = 'test_screenshot.png'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "..", 'images', filename)
    image = pyautogui.screenshot(file_path)

locations = [{'reddit': "reddit_icon.PNG"}, {"edit": "capture.png"}]

def get_starting_position(locations, target_key):
    for dictionary in locations:
        if target_key in dictionary:
            value = dictionary[target_key]
            # print(f"Value for key '{target_key}': {value}")
            print(value)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "..", "images", value)
            img = pyautogui.locateOnScreen(image_path)
            if img is not None:
                print("Image found at:", img)
                print(pyautogui.center(img))
            else:
                print("Image not found.")
                print("sleeping for 3 seconds")
    # Example usage:
# get_starting_position(locations, "reddit")
# create_screenshot()
# 