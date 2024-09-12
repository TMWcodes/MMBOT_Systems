import pyautogui
from time import sleep, time
import os #import
import json #parse
from color_check import check_color
from mouse_movement_1 import move_mouse_with_easing, generate_spline_path, create_bezier_path
   



def playActions(filename, path_type='spline'):
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
            elif action['type'] == 'move' or action['type'] == 'click':
                current_pos = pyautogui.position()
                target_pos = (action['pos'][0], action['pos'][1])
                if path_type == 'spline':
                    points = generate_spline_path(current_pos, target_pos)
                    print(f"moving to {target_pos}")
                    pyautogui.mouseDown() 
                    move_mouse_with_easing(zip(*(i.astype(int) for i in points)), duration=0.1, easing_function=pyautogui.easeInOutQuad)
                    pyautogui.mouseUp()
                elif path_type == 'bezier':
                    path = create_bezier_path(current_pos, target_pos)
                    print(f"moving to {target_pos}")
                    pyautogui.mouseDown() 
                    for point in path:
                        pyautogui.moveTo(point[0], point[1], duration=0.1, tween=pyautogui.easeInQuad)
                    pyautogui.mouseUp()
                
                if action['type'] == 'click':
                    pyautogui.click(target_pos[0], target_pos[1], button='left' if action['button'] == 'Button.left' else 'right', duration=0.25)
                    print(f"{action['button']} click on {action['pos']}")
            # sleep until next action
      
            try:
                next_action = data[index + 1]
            except IndexError:
                break
            # Calculate and apply sleep time until the next action
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
