from playback import initialize_pyautogui, count_down_timer, playActions
from time import sleep

LOOP_REPS = 2
def main():
    initialize_pyautogui()
    count_down_timer()
    for i in range(0, LOOP_REPS):

        # start at position FB1, open screen, withdrawn item_1 go to furnace 1, return to FB1 deposit.
        playActions("tiara_01.json")
        print("tiara finished")
        sleep(10.00)
        playActions("smith_01.json")
        print("smelt finished")
        sleep(10.00)

        # start at FB1, withdraw unique_item_1, 

        # with screen open withdraw item_2

        print("Completed loop")

    print("Completed process")
if __name__ == "__main__":
    main()