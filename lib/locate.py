import pyautogui
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "..", "images", "logo.PNG")
res = pyautogui.locateOnScreen(image_path)
if res is not None:
    print("Image found at:", res)
    print(pyautogui.center(res))
else:
    print("Image not found.")

  