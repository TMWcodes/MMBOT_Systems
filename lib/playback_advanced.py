import pyautogui
from time import sleep, time
import os
import json
from mouse_movement_1 import move_mouse_with_easing, generate_spline_path, create_bezier_path
from my_utils import vary_coordinates, check_color

# Function to log click events
def log_clicks(log_data, coordinates, color, elapsed_time):
    log_data.append({
        'time': elapsed_time,
        'type': 'click',
        'button': 'Button.left' if pyautogui.position() == coordinates else 'Button.right',
        'pos': coordinates,
        'color': color
    })

def playActions(filename, path_type='spline', vary_coords=False, variation=0.05):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'recordings', filename)
    
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

                # Apply coordinate variation if enabled
                if vary_coords:
                    x_var, y_var = vary_coordinates(target_pos[0], target_pos[1], variation)
                    target_pos = (target_pos[0] + x_var, target_pos[1] + y_var)

                if path_type == 'spline':
                    points = generate_spline_path(current_pos, target_pos)
                    print(f"moving to {target_pos}")
                    move_mouse_with_easing(zip(*(i.astype(int) for i in points)), duration=0.1, easing_function=pyautogui.easeInOutQuad)
                elif path_type == 'bezier':
                    path = create_bezier_path(current_pos, target_pos)
                    print(f"moving to {target_pos}")
                    for point in path:
                        pyautogui.moveTo(point[0], point[1], duration=0.1, tween=pyautogui.easeInQuad)
                if action['type'] == 'click':
                    # Log click event
                    color = check_color(target_pos)
                    log_clicks(log_data, target_pos, color, elapsed_time)

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

    base_filename, _ = os.path.splitext(filename)
    log_file_path = os.path.join(log_dir, f'{base_filename}_log.json')
    # If the log file already exists, find a new filename
    if os.path.exists(log_file_path):
        i = 1
        new_log_file_path = log_file_path
        while os.path.exists(new_log_file_path):
            new_log_file_path = os.path.join(log_dir, f'{base_filename}_log_{i}.json')
            i += 1
        log_file_path = new_log_file_path

    with open(log_file_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

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
