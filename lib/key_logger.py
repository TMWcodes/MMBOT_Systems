from pynput import mouse, keyboard
#pynput             1.7.6

# Declare mouse listener globally, so that keyboard on_release can stop it

mouse_listener = None

def main():
    runListeners()

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        
def on_release(key):
    print('{0} released'.format(key))
    
    if key == keyboard.Key.esc:
        # Stop listener
        global mouse_listener
        mouse_listener.stop()
        #stop keyboard listener
        raise keyboard.Listener.StopException
        
    
def on_click(x, y, button, pressed):
    if not pressed:
        print('{0} at {1}'.format('Released',(x, y)))
 
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
        listener.join()
    # collect keyboard input

if __name__ == "__main__":
    main()
