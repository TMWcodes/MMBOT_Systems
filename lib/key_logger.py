from pynput import mouse, keyboard
from time import time
#pynput             1.7.6

# Declare mouse listener globally, so that keyboard on_release can stop it

mouse_listener = None
# declare our start_time globally so that the call back functions can reference it.
start_time = None

def main():
    runListeners()

def elapsed_time():
    global start_time
    return time() - start_time

def on_press(key):
    try:
        print('{0} pressed at {1}'.format(
            key.char, elapsed_time()))
    except AttributeError:
        print('special key {0} pressed at {1}'.format(
            key, elapsed_time()))
        
def on_release(key):
    print('{0} released'.format(key, elapsed_time()))
    
    if key == keyboard.Key.esc:
        # Stop listener
        global mouse_listener
        mouse_listener.stop()
        #stop keyboard listener
        raise keyboard.Listener.StopException
        
    
def on_click(x, y, button, pressed):
    if not pressed:
        print('clicked {0} on {1} at {2}'.format(button,(x, y), elapsed_time()))
 
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
