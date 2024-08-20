from pynput import mouse, keyboard
from time import time, sleep
import json
import os
from my_utils import check_color, count_down_timer

OUTPUT_FILENAME = 'tkinter'

class EventType:
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'
    MOVE = 'move'

class KeyLogger:
    def __init__(self, record_move_actions, min_move_interval):
        self.record_move_actions = record_move_actions
        self.min_move_interval = min_move_interval
        self.mouse_listener = None
        self.start_time = None
        self.unreleased_keys = []
        self.input_events = []
        self.last_move_time = 0  # Initialize last move time

    def elapsed_time(self):
        return time() - self.start_time

    def record_event(self, event_type, event_time, button, pos=None, color=None):
        if str(button) == "Key.esc":
            return
       

        self.input_events.append({
            'time': event_time,
            'type': event_type,
            'button': str(button),
            'pos': pos,
            'color': color
        })
        
        if event_type == EventType.CLICK:
            print(f'{event_type} on {button} pos {pos} color {color} at {round(event_time, 4)}')
        else:
            pos_str = f'pos {pos}' if pos else 'no position'
            print(f'{event_type} {pos_str} at {round(event_time, 4)}')
            
    def on_press(self, key):
        if key in self.unreleased_keys:
            return
        else:
            self.unreleased_keys.append(key)

        try:
            self.record_event(EventType.KEYDOWN, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(EventType.KEYDOWN, self.elapsed_time(), key)
        
    def on_release(self, key):
        try:
            self.unreleased_keys.remove(key)
        except ValueError:
            print(f'ERROR: {key} not in unreleased_keys')

        try:
            self.record_event(EventType.KEYUP, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(EventType.KEYUP, self.elapsed_time(), key)
    
        if key == keyboard.Key.esc:
            self.mouse_listener.stop()
            raise keyboard.Listener.StopException

    def on_click(self, x, y, button, pressed):
        if not pressed:
            color = check_color((x, y))
            self.record_event(EventType.CLICK, self.elapsed_time(), button, (x, y), color)

    def on_move(self, x, y):
        if self.record_move_actions:
            current_time = time()
            time_since_last_move = current_time - self.last_move_time

            if time_since_last_move >= self.min_move_interval:
                self.record_event(EventType.MOVE, self.elapsed_time(), None, (x, y))
                self.last_move_time = current_time

    def run_listeners(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.mouse_listener.start()

        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            self.start_time = time()
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


