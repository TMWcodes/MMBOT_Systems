import pyautogui
from time import sleep
import os #import
import json #parse
def main():
    # initialize
   initialize_pyautogui()
   count_down_timer()
   playActions("actions_test_01.json")
    # change camera to birds eye view 
   

def initialize_pyautogui():
     pyautogui.FAILSAFE = True

def count_down_timer():
        # ten second count down
    print("starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
        sleep(1)
    print("Go")

def playActions(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(
        script_dir,
        'recordings', 
        filename
    )
    with open(file_path, "r") as jsonfile:
        #formatting
        data = json.load(jsonfile)
        print(data)

if __name__ == "__main__":
    main()
