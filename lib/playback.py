import pyautogui
from time import sleep, time
import os #import
import json #parse
# def main():
#     # initialize
#    initialize_pyautogui()
 
#    count_down_timer()
#    for i in range(0, 10):
#         playActions("smith_01.json")
#         print(i)
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
            action_start_time = time()
            if action['button'] == 'Key.esc':
                break

            #perform action
            if action['type'] == 'keyDown':
                key = convertKey(action['button'])
                pyautogui.keyDown(key)
                print("keyDown on {}". format(action['button']))
            elif action['type'] == 'keyUp':
                key = convertKey(action['button'])
                pyautogui.keyUp(key)
                print("keyUp on {}". format(action['button']))
            elif action['type'] == 'click':
                if action['button'] == 'Button.left':
                    pyautogui.moveTo(action['pos'][0], action['pos'][1], duration=1, tween=pyautogui.easeInQuad)
                    sleep(1)
                    pyautogui.click('left', duration=0.25)
                    print(f"left click on {action['pos']}")
                elif action['button'] == 'Button.right':
                    pyautogui.moveTo(action['pos'][0], action['pos'][1], duration=1, tween=pyautogui.easeInQuad)
                    sleep(1)
                    pyautogui.click('right', duration=0.25)
                    print(f"right click on {action['pos']}")
            # sleep until next action
            try:
                next_action = data[index + 1]
            except IndexError:
                break
            elapsed_time = next_action['time'] - action['time']

            if elapsed_time < 0:
                raise Exception('Unexpected action ordering')

            elapsed_time -= (time() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            print("sleeping for {}".format(elapsed_time))
            sleep(elapsed_time)

def convertKey(button):
    # 'Key.F9' should return 'F9', 'w' should return 'w'
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'caps_lock': 'capslock',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
        'Key.space': ' ',
        'enter': '\n',
        'backspace': '\b',
    }

    # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
    cleaned_key = button.replace('Key.', '')
    print(cleaned_key)
    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key

# if __name__ == "__main__":
#     main()
