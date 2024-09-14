from pynput import mouse, keyboard
from time import time
import json
import os
from my_utils import count_down_timer
from color_check import check_color

class EventType:
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'
    MOVE = 'move'
    MOUSE_DOWN = 'mouseDown'
    MOUSE_UP = 'mouseUp'

class KeyLogger:
    def __init__(self, record_move_actions, min_move_interval):
        self.record_move_actions = record_move_actions
        self.min_move_interval = min_move_interval
        self.mouse_listener = None
        self.start_time = None
        self.input_events = []
        self.last_move_time = 0  # Initialize last move time

    def elapsed_time(self):
        return time() - self.start_time

    def record_event(self, event_type, event_time, button, pos=None, color=None):
        if str(button) == "Key.esc":
            return

          # Convert button to string if it's a special key
        button_str = str(button)
        if hasattr(button, 'char') and button.char:
            button_str = button.char
        elif hasattr(button, 'name'):
            button_str = button.name

        self.input_events.append({
            'time': event_time,
            'type': event_type,
            'button': str(button),
            'pos': pos,
            'color': color
        })
        
        # Improved terminal output ###
        if event_type == EventType.CLICK:
            print(f'{event_type} on {button_str} at {pos} with color {color} at {round(event_time, 4)}')
        elif event_type == EventType.KEYDOWN:
            print(f'{event_type} "{button_str}" at {round(event_time, 4)}')
        elif event_type == EventType.KEYUP:
            print(f'{event_type} "{button_str}" at {round(event_time, 4)}')
        else:
            pos_str = f'at {pos}' if pos else 'no position'
            print(f'{event_type} {pos_str} at {round(event_time, 4)}')

    def on_press(self, key):
        try:
            self.record_event(EventType.KEYDOWN, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(EventType.KEYDOWN, self.elapsed_time(), key)

    def on_release(self, key):
        try:
            self.record_event(EventType.KEYUP, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(EventType.KEYUP, self.elapsed_time(), key)
    
        if key == keyboard.Key.esc:
            self.mouse_listener.stop()
            raise keyboard.Listener.StopException
    
    def on_click(self, x, y, button, pressed):
        color = None
        try:
            if pressed:
                color = check_color((x, y))
                self.record_event(EventType.MOUSE_DOWN, self.elapsed_time(), button, (x, y), color)
            else:
                self.record_event(EventType.MOUSE_UP, self.elapsed_time(), button, (x, y))
                # self.record_event(EventType.CLICK, self.elapsed_time(), button, (x, y), color)
        except Exception as e:
            print(f"Error in on_click: {e}")

            
    def on_move(self, x, y):
        if self.record_move_actions:
            current_time = time()
            time_since_last_move = current_time - self.last_move_time

            if time_since_last_move >= self.min_move_interval:
                self.record_event(EventType.MOVE, self.elapsed_time(), None, (x, y))
                self.last_move_time = current_time

    def run_listeners(self):
        self.start_time = time()
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.mouse_listener.start()

        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

        self.mouse_listener.join()

        print("Key logger has been stopped.")

    def start(self, output_filename):
        self.input_events = []
        count_down_timer()
        self.run_listeners()
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'recordings', f'{output_filename}.json')
        with open(file_path, "w") as outfile:
            json.dump(self.input_events, outfile, indent=4)
