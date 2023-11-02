import pyautogui
import time

def main():
    # initialize
    pyautogui.FAILSAFE = True

    print("starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
  
        time.sleep(1)
    print("Go")

    pyautogui.keyDown('right')
    time.sleep(1)
    pyautogui.keyUp('right')
    print("Done")

main()