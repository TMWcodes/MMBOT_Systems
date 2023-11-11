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
        # parse json first
        data = json.load(jsonfile)
        for index, action in enumerate(data):
            # look for esc
            if action['button'] == 'Key.esc':
                break

            #perform action
            if action['type'] == 'keyDown':
                pyautogui.keyDown(action['button'])
                print("keyDown on {}". format(action['button']))
            elif action['type'] == 'keyUp':
                pyautogui.keyUp(action['button'])
                print("keyUp on {}". format(action['button']))
            elif action['type'] == 'click':
                pyautogui.click(action['pos'][0],action['pos'][1], duration=0.25)
                print("click on {}". format(action['pos']))

            # sleep until next action
            try:
                next_action = data[index + 1]
            except IndexError:
                break
            elapsed_time = next_action['time'] -action['time']
            if elapsed_time >= 0:
                print("sleeping for {}".format(elapsed_time))
                sleep(elapsed_time)
            else:
                raise Exception('Unexpected action ordering')
        # print(data)

if __name__ == "__main__":
    main()
