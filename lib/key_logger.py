from pynput import mouse, keyboard
from time import time
import json
import os
#pynput             1.7.6

OUTPUT_FILENAME = 'actions_test_01'


# Declare mouse listener globally, so that keyboard on_release can stop it
mouse_listener = None
# declare our start_time globally so that the call back functions can reference it.
start_time = None

unreleased_keys = []
# storing input events
input_events = []

class EventType():
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'

def main():
    runListeners()
    print("Recording duration: {} seconds".format(elapsed_time))
    global input_events
    print(json.dumps(input_events))

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'recordings','{}.json'.format(OUTPUT_FILENAME)
    )
    with open(file_path, "w") as outfile:
        #formatting
        json.dump(input_events, outfile, indent=4)

def elapsed_time():
    global start_time
    return time() - start_time

def record_event(event_type, event_time, button, pos=None):
    global input_events
    input_events.append({'time': event_time,
                         'type': event_type,
                         'button': str(button),
                         'pos': pos
    })
    
    if event_type == EventType.CLICK:
        print('{} on {} pos {} at {}'.format(event_type, button, pos, event_time))
    else:
        print('{} on {} at {}'.format(event_type, button, event_time))

def on_press(key):
    # we only want to record the first key pressed until released.
    global unreleased_keys
    if key in unreleased_keys:
        return
    else:
        unreleased_keys.append(key)

    try:
        record_event(EventType.KEYDOWN, elapsed_time(), key.char)
        # print('{0} pressed at {1}'.format(
        #     key.char, elapsed_time()))
    except AttributeError:
         record_event(EventType.KEYDOWN, elapsed_time(), key)
        # print('special key {0} pressed at {1}'.format(
        #     key, elapsed_time()))
        
def on_release(key):
    # mark key as no longer pressed
    global unreleased_keys
    try:
        unreleased_keys.remove(key)
    except ValueError:
        print('ERROR: {} not in unreleased_keys'.format(key))

    try:
        record_event(EventType.KEYUP, elapsed_time(), key.char)
    except AttributeError:
         record_event(EventType.KEYUP, elapsed_time(), key)
       

    # print('{0} released'.format(key, elapsed_time()))
    
    if key == keyboard.Key.esc:
        # Stop listener
        global mouse_listener
        mouse_listener.stop()
        #stop keyboard listener
        raise keyboard.Listener.StopException
        
    
def on_click(x, y, button, pressed):
    if not pressed:
        record_event(EventType.CLICK, elapsed_time(), button, (x, y))
        # print('clicked {0} on {1} at {2}'.format(button,(x, y), elapsed_time()))
 
def runListeners():

# mouse 
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    mouse_listener.wait() # wait for listener to become ready

# keyboard 
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        global start_time
        start_time = time()
        listener.join()
    # collect keyboard input

if __name__ == "__main__":
    main()
