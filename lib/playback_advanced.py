import pyautogui
from time import sleep, time
import os
import json
from mouse_movement_1 import move_mouse_with_easing, generate_spline_path, create_bezier_path
from my_utils import vary_coordinates
from color_check import check_color
from key_logger import EventType

def playActions(filename, path_type='spline', vary_coords=False, variation=0.01, ignore_move_actions=False):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    print(f"file_path is {file_path}")

    log_data = []
    playback_start_time = time()
    pressed_keys = set()  # Track currently pressed keys

    try:
        with open(file_path, "r") as jsonfile:
            data = json.load(jsonfile)

            for index, action in enumerate(data):
                print(f"\nProcessing action at index {index}: {action}")

                # Ignore mouse movement actions if specified
                if ignore_move_actions and action['type'] == EventType.MOVE:
                    continue

                # Handle mouse button actions
                elif ignore_move_actions and action['type'] in [EventType.MOUSE_DOWN, EventType.MOUSE_UP]:
                    current_pos = pyautogui.position()
                    target_pos = (action['pos'][0], action['pos'][1]) if action.get('pos') else current_pos
                    if path_type == 'spline':
                        points = generate_spline_path(current_pos, target_pos)
                        move_mouse_with_easing(zip(*(i.astype(int) for i in points)), duration=0.1, easing_function=pyautogui.easeInOutQuad)
                    elif path_type == 'bezier':
                        path = create_bezier_path(current_pos, target_pos)
                        for point in path:
                            pyautogui.moveTo(point[0], point[1], duration=0.1, tween=pyautogui.easeInQuad)
                    elif path_type == 'none':
                        pyautogui.moveTo(target_pos[0], target_pos[1], duration=0.1)

                # Break on ESC key action
                if action['button'] == 'Key.esc':
                    print("Escape key pressed, breaking the loop.")
                    break

                actual_elapsed_total = time() - playback_start_time

                # Check for action type and validate 'pos' only for mouse-related actions
                if action['type'] in [EventType.MOUSE_DOWN, EventType.MOUSE_UP, EventType.CLICK, EventType.MOVE]:
                    if 'pos' in action:
                        print(f"Raw position data: {action['pos']}")
                        if not isinstance(action['pos'], (list, tuple)) or len(action['pos']) != 2:
                            print(f"Invalid position data structure: {action['pos']}, skipping this action.")
                            continue

                # Handle key down events
                if action['type'] == EventType.KEYDOWN:
                    key = convertKey(action['button'])
                    print(f"Key down: {key}")
                    pyautogui.keyDown(key)
                    pressed_keys.add(key)
                    log_data.append({'time': actual_elapsed_total, 'type': EventType.KEYDOWN, 'button': action['button'], 'pos': None, 'color': None})

                # Handle key up events
                elif action['type'] == EventType.KEYUP:
                    key = convertKey(action['button'])
                    print(f"Key up: {key}")
                    pyautogui.keyUp(key)
                    pressed_keys.discard(key)  # Remove key from pressed_keys set
                    log_data.append({'time': actual_elapsed_total, 'type': EventType.KEYUP, 'button': action['button'], 'pos': None, 'color': None})

                # Handle mouse down events
                elif action['type'] == EventType.MOUSE_DOWN:
                    if action.get('pos') and len(action['pos']) == 2:
                        target_pos = (action['pos'][0], action['pos'][1])  # Explicitly unpack pos as a tuple
                        print(f"Mouse down at {target_pos}")
                        color = check_color(target_pos)
                        pyautogui.mouseDown(x=target_pos[0], y=target_pos[1], button=convertKey(action['button']))
                        log_data.append({'time': actual_elapsed_total, 'type': EventType.MOUSE_DOWN, 'button': action['button'], 'pos': target_pos, 'color': color})
                    else:
                        print(f"Invalid position data: {action.get('pos')}")

                # Handle mouse up events
                elif action['type'] == EventType.MOUSE_UP:
                    if action.get('pos') and len(action['pos']) == 2:
                        target_pos = (action['pos'][0], action['pos'][1])
                        print(f"Mouse up at {target_pos}")
                        pyautogui.mouseUp(x=target_pos[0], y=target_pos[1], button=convertKey(action['button']))
                        log_data.append({'time': actual_elapsed_total, 'type': EventType.MOUSE_UP, 'button': action['button'], 'pos': action['pos'], 'color': None})
                    else:
                        print(f"Invalid position data for mouse up: {action.get('pos')}")

                # Handle mouse click and move events
                elif action['type'] in [EventType.CLICK, EventType.MOVE]:
                    current_pos = pyautogui.position()
                    target_pos = (action['pos'][0], action['pos'][1]) if action.get('pos') else current_pos
                    print(f"Current position: {current_pos}, Target position: {target_pos}")

                    if vary_coords:
                        x_var, y_var = vary_coordinates(target_pos[0], target_pos[1], variation)
                        target_pos = (target_pos[0] + x_var, target_pos[1] + y_var)
                        print(f"Adjusted target position with variation: {target_pos}")

                    if path_type == 'spline':
                        points = generate_spline_path(current_pos, target_pos)
                        move_mouse_with_easing(zip(*(i.astype(int) for i in points)), duration=0.1, easing_function=pyautogui.easeInOutQuad)
                    elif path_type == 'bezier':
                        path = create_bezier_path(current_pos, target_pos)
                        for point in path:
                            pyautogui.moveTo(point[0], point[1], duration=0.1, tween=pyautogui.easeInQuad)
                    elif path_type == 'none':
                        pyautogui.moveTo(target_pos[0], target_pos[1], duration=0.1)

                    if action['type'] == EventType.CLICK:
                        color = check_color(target_pos)
                        log_data.append({'time': actual_elapsed_total, 'type': EventType.CLICK, 'button': action['button'], 'pos': target_pos, 'color': color})
                        pyautogui.click(target_pos[0], target_pos[1], button='left' if action['button'] == 'Button.left' else 'right', duration=0.25)

                try:
                    next_action = data[index + 1]
                except IndexError:
                    print("End of actions list.")
                    break

                expected_time = next_action['time']
                actual_elapsed_total = time() - playback_start_time
                adjusted_sleep_time = max(expected_time - actual_elapsed_total, 0.05)  # Added minimum sleep time

                print(f"Expected time: {expected_time}")
                print(f"Actual elapsed time since start: {actual_elapsed_total}")
                print(f"Adjusted sleep time: {adjusted_sleep_time} seconds (after correction)")

                sleep(adjusted_sleep_time)

        log_dir = os.path.join(script_dir, 'log_records')
        os.makedirs(log_dir, exist_ok=True)
        base_filename = os.path.splitext(os.path.basename(file_path))[0]
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

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

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
        'Button.left': 'left',
        'Button.right': 'right',
        '\u001a': 'z',  # Special handling for Ctrl+Z
    }

    if button.startswith('Key.'):
        cleaned_key = button.replace('Key.', '')
        if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
            return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]
        return cleaned_key

    if button.startswith('Button.'):
        cleaned_key = button.replace('Button.', '')
        return PYNPUT_SPECIAL_CASE_MAP.get(cleaned_key, cleaned_key)

    return button
