import pyautogui
from time import sleep, time
import os
import json
from mouse_movement_1 import move_mouse_with_easing, generate_spline_path, create_bezier_path
from my_utils import vary_coordinates, check_color
from key_logger import EventType

def playActions(filename, path_type='spline', vary_coords=False, variation=0.01):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'recordings', filename)
    print(f"file_path is {file_path}")
    log_data = []
    start_time = time() 
    with open(file_path, "r") as jsonfile:
        data = json.load(jsonfile)
        
        for index, action in enumerate(data):
            action_start_time = time()
            if action['button'] == 'Key.esc':
                break
            
            elapsed_time = time() - start_time 
            # Perform action
            if action['type'] == EventType.KEYDOWN:
                key = convertKey(action['button'])
                pyautogui.keyDown(key)
                print(f"keyDown on {action['button']}")

                # Log keyDown event
                log_data.append({
                    'time': elapsed_time,
                    'type': EventType.KEYDOWN,
                    'button': action['button'],
                    'pos': None,
                    'color': None
                })

            elif action['type'] == EventType.KEYUP:
                key = convertKey(action['button'])
                pyautogui.keyUp(key)
                print(f"keyUp on {action['button']}")

                # Log keyUp event
                log_data.append({
                    'time': elapsed_time,
                    'type': EventType.KEYUP,
                    'button': action['button'],
                    'pos': None,
                    'color': None
                })

            elif action['type'] == EventType.MOVE or action['type'] == EventType.CLICK:
                current_pos = pyautogui.position()
                target_pos = (action['pos'][0], action['pos'][1])

                # Apply coordinate variation if enabled
                if vary_coords:
                    x_var, y_var = vary_coordinates(target_pos[0], target_pos[1], variation)
                    target_pos = (target_pos[0] + x_var, target_pos[1] + y_var)

                print(f"Target position before check: {target_pos}")
                if not isinstance(target_pos, (tuple, list)) or len(target_pos) != 2:
                    raise ValueError("target_pos must be a tuple or list of two integers")
                
                x, y = target_pos
                if not isinstance(x, int) or not isinstance(y, int):
                    raise ValueError("Both elements of target_pos must be integers")

                if path_type == 'spline':
                    points = generate_spline_path(current_pos, target_pos)
                    print(f"moving to {target_pos}")
                    move_mouse_with_easing(zip(*(i.astype(int) for i in points)), duration=0.1, easing_function=pyautogui.easeInOutQuad)
                elif path_type == 'bezier':
                    path = create_bezier_path(current_pos, target_pos)
                    print(f"moving to {target_pos}")
                    for point in path:
                        pyautogui.moveTo(point[0], point[1], duration=0.1, tween=pyautogui.easeInQuad)
                
                if action['type'] == EventType.CLICK:
                    color = check_color(target_pos)
                    # Log click event
                    log_data.append({
                        'time': elapsed_time,
                        'type': EventType.CLICK,
                        'button': action['button'],
                        'pos': target_pos,
                        'color': color
                    })
                    pyautogui.click(target_pos[0], target_pos[1], button='left' if action['button'] == 'Button.left' else 'right', duration=0.25)
                    print(f"{action['button']} click on {action['pos']}")
            
            # Sleep until next action
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
    
    # Save logged data to a new JSON file in the log_records folder with a single .json extension
    log_dir = os.path.join(script_dir, 'log_records')
    os.makedirs(log_dir, exist_ok=True)  # Create the log_records directory if it doesn't exist
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    log_record_path = os.path.join(log_dir, f'{base_filename}_log.json')

    if os.path.exists(log_record_path):
        i = 1
        new_log_record_path = log_record_path
        while os.path.exists(new_log_record_path):
            new_log_record_path = os.path.join(log_dir, f'{base_filename}_log_{i}.json')
            i += 1
        log_record_path = new_log_record_path

    with open(log_record_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

    print(f"Log data saved to: {log_record_path}")

def convertKey(button):
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

    cleaned_key = button.replace('Key.', '')
    print(cleaned_key)
    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key

# Example usage
# playActions('your_filename.json', path_type='spline', vary_coords=True, variation=0.05)
