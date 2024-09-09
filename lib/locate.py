import pyautogui
import os
from time import sleep
from hard_coded import are_colors_similar
      
def create_screenshot():
    filename = 'test_screenshot.png'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "..", 'images', filename)
    pyautogui.screenshot(file_path)

def new_tab_search(web_address="www.youtube.com"):
    sleep(2)
    # open tab 
    pyautogui.hotkey("ctrl", "t")
    sleep(1)
    # search and enter
    pyautogui.write(web_address, interval=0.3)
    sleep(4)
    pyautogui.hotkey("enter")
 
def found_img_message(filename="edit.PNG"):
    
    filename = pyautogui.prompt(text="", title="enter filename")
    print(filename)
    sleep(2)
    # img = pyautogui.locateCenterOnScreen("..\\images\\edit.PNG")
    image_path = os.path.join("..", "images", filename)
    img = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
    fixed_input = f"Found them at {img}"
    
    if img is not None:
        print("Image found at:", img)
        pyautogui.moveTo(img)
        sleep(2)
        pyautogui.write(fixed_input, interval=0.2)
    else:
        print("Image not found.")

def screen_image(filename="edit.PNG"):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "..", "images", filename)
    res = pyautogui.locateOnScreen(image_path)
    if res is not None:
        print("Image found at:", res)
        icon = pyautogui.center(res)
        print(f"moving mouse to {icon}")
        pyautogui.moveTo(icon)

    else:
        print("Image not found.")

def get_starting_position(locations, target_key):

    for dictionary in locations:
        if target_key in dictionary:
            values = dictionary[target_key]
            for value in values:
                # print(f"Value for key '{target_key}': {value}")
                script_dir = os.path.dirname(os.path.abspath(__file__))
                image_path = os.path.join(script_dir, "..", "images", value)
                img = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
                if img is not None:
                    print(f"Found image {value} at {img}")
                    return True  # Found the image, return True
                else:
                    print(f"Image {value} not found.")
    return False  # None of the images were found, return False
#
