from pynput import mouse, keyboard
from time import time, sleep
import json
import os
from my_utils import check_color

OUTPUT_FILENAME = 'color_coord_test_01'

mouse_listener = None
start_time = None
unreleased_keys = []
input_events = []

class EventType():
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'
    MOVE = 'move'

def main():
    print("start in 5")
    sleep(5)
    print("started")
    runListeners()
    global input_events
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'recordings', f'{OUTPUT_FILENAME}.json')
    with open(file_path, "w") as outfile:
        json.dump(input_events, outfile, indent=4)

def elapsed_time():
    global start_time
    return time() - start_time

def record_event(event_type, event_time, button, pos=None, color=None):
    if str(button) == "Key.esc":
        return
    
    global input_events
    input_events.append({
        'time': event_time,
        'type': event_type,
        'button': str(button),
        'pos': pos,
        'color': color
    })
    
    if event_type == EventType.CLICK:
        print(f'{event_type} on {button} pos {pos} color {color} at {event_time}')
    else:
        print(f'{event_type} on {button} at {event_time}')

def on_press(key):
    global unreleased_keys
    if key in unreleased_keys:
        return
    else:
        unreleased_keys.append(key)

    try:
        record_event(EventType.KEYDOWN, elapsed_time(), key.char)
    except AttributeError:
        record_event(EventType.KEYDOWN, elapsed_time(), key)
        
def on_release(key):
    global unreleased_keys
    try:
        unreleased_keys.remove(key)
    except ValueError:
        print(f'ERROR: {key} not in unreleased_keys')

    try:
        record_event(EventType.KEYUP, elapsed_time(), key.char)
    except AttributeError:
        record_event(EventType.KEYUP, elapsed_time(), key)
    
    if key == keyboard.Key.esc:
        global mouse_listener
        mouse_listener.stop()
        raise keyboard.Listener.StopException

def on_click(x, y, button, pressed):
    if not pressed:
        color = check_color((x, y))
        record_event(EventType.CLICK, elapsed_time(), button, (x, y), color)

MIN_MOVE_INTERVAL = 2
last_move_time = 0

def on_move(x, y):
    global last_move_time
    current_time = time()
    time_since_last_move = current_time - last_move_time

    if time_since_last_move >= MIN_MOVE_INTERVAL:
        record_event(EventType.MOVE, elapsed_time(), None, (x, y))
        last_move_time = current_time

def runListeners():
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
    mouse_listener.start()

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        global start_time
        start_time = time()
        listener.join()

    mouse_listener.join()

if __name__ == "__main__":
    main()
