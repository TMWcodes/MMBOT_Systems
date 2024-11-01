import pyautogui
from time import sleep, time
import os
import json
from mouse_movement_1 import threaded_mouse_movement, move_mouse_with_easing, generate_spline_path, create_bezier_path
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

                # Time calculation for sleep
                actual_elapsed_total = time() - playback_start_time

                # Break on ESC key action
                if action['button'] == 'Key.esc':
                    print("Escape key pressed, breaking the loop.")
                    break

                # Validate 'pos' for mouse-related actions
                if action['type'] in [EventType.MOUSE_DOWN, EventType.MOUSE_UP, EventType.MOVE]:
                    if 'pos' in action and (not isinstance(action['pos'], (list, tuple)) or len(action['pos']) != 2):
                        print(f"Invalid position data structure: {action['pos']}, skipping this action.")
                        continue

                    # Handle mouse events
                    current_pos = pyautogui.position()
                    target_pos = (action['pos'][0], action['pos'][1]) if action.get('pos') else current_pos

                    # Apply coordinate variation if needed
                    if vary_coords:
                        x_var, y_var = vary_coordinates(target_pos[0], target_pos[1], variation)
                        target_pos = (target_pos[0] + x_var, target_pos[1] + y_var)
                        print(f"Adjusted target position with variation: {target_pos}")

                    # Mouse movement based on path_type
                    if path_type == 'spline':
                        points = generate_spline_path(current_pos, target_pos)
                        # Use threaded_mouse_movement to keep the GUI responsive
                        threaded_mouse_movement(zip(*(i.astype(int) for i in points)), duration=0.1, easing_function=pyautogui.easeInOutQuad)
                    elif path_type == 'bezier':
                        path = create_bezier_path(current_pos, target_pos)
                        # Loop through points and use threading for each point to ensure responsiveness
                        for point in path:
                            threaded_mouse_movement([point], duration=0.1, easing_function=pyautogui.easeInQuad)
                    elif path_type == 'none':
                        # Direct movement without threading for simplicity
                        pyautogui.moveTo(target_pos[0], target_pos[1], duration=0.1)

                    # Handle mouse down events
                    if action['type'] == EventType.MOUSE_DOWN:
                        print(f"Mouse down at {target_pos}")
                        color_down = check_color(target_pos)
                        pyautogui.mouseDown(x=target_pos[0], y=target_pos[1], button=convertKey(action['button']))
                        # Store log for mouse down
                        log_data.append({'time': actual_elapsed_total, 'type': EventType.MOUSE_DOWN, 'button': action['button'], 'pos': target_pos, 'color': color_down})

                    # Handle mouse up events
                    elif action['type'] == EventType.MOUSE_UP:
                        print(f"Mouse up at {target_pos}")
                        color_up = check_color(target_pos)
                        pyautogui.mouseUp(x=target_pos[0], y=target_pos[1], button=convertKey(action['button']))
                        log_data.append({'time': actual_elapsed_total, 'type': EventType.MOUSE_UP, 'button': action['button'], 'pos': target_pos, 'color': color_up})

                # Handle typing events
                if action['type'] == EventType.KEYDOWN:
                    key = convertKey(action['button'])
                    print(f"Key down: {key}")
                    pyautogui.keyDown(key)
                    pressed_keys.add(key)
                    log_data.append({'time': actual_elapsed_total, 'type': EventType.KEYDOWN, 'button': action['button'], 'pos': None, 'color': None})

                elif action['type'] == EventType.KEYUP:
                    key = convertKey(action['button'])
                    print(f"Key up: {key}")
                    pyautogui.keyUp(key)
                    pressed_keys.discard(key)  # Remove key from pressed_keys set
                    log_data.append({'time': actual_elapsed_total, 'type': EventType.KEYUP, 'button': action['button'], 'pos': None, 'color': None})

                # Handle drag-and-drop (MOUSE_DOWN -> MOVE -> MOUSE_UP)
                if action['type'] == EventType.MOVE and pressed_keys:
                    # Drag and drop logic; assuming pressed_keys contains mouse button currently held
                    pyautogui.mouseUp(x=target_pos[0], y=target_pos[1], button='left')  # Release the mouse button after dragging

                # Calculate sleep time before the next action
                try:
                    next_action = data[index + 1]
                except IndexError:
                    print("End of actions list.")
                    break

                expected_time = next_action['time']
                adjusted_sleep_time = max(expected_time - actual_elapsed_total, 0.05)  # Added minimum sleep time
                print(f"Adjusted sleep time: {adjusted_sleep_time} seconds (after correction)")
                sleep(adjusted_sleep_time)

        # Logging the recorded actions
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
        return PYNPUT_SPECIAL_CASE_MAP.get(cleaned_key, cleaned_key)

    if button.startswith('Button.'):
        cleaned_key = button.replace('Button.', '')
        return PYNPUT_SPECIAL_CASE_MAP.get(cleaned_key, cleaned_key)

    return button
