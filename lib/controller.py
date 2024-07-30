from playback_advanced import playActions
from time import sleep
from locate import get_starting_position
from my_utils import initialize_pyautogui, count_down_timer
from key_logger import main as start_key_logger

def run_key_logger(output_filename):
    start_key_logger(output_filename)

def play_multiple_actions(actions_with_params, locations, check_type):
    for filename, params in actions_with_params:
        delay = params.pop('delay', 0)  # Extract delay from params
        if get_starting_position(locations, check_type):  # Check locations before each action
            print(f"Location check passed for {filename}. Playing actions...")
            playActions(filename, **params)
            sleep(delay)
        else:
            print(f"Location check failed for {filename}. Actions not performed.")
            break
        print("All actions have been played.")

def check_and_run_actions(check_function, locations, actions_with_params, check_type):
    play_multiple_actions(actions_with_params, locations, check_type)

# def main():
#     initialize_pyautogui()
#     count_down_timer() # starting.....Go
#     # run {LOOP_REPS} times
#     for i in range(0, LOOP_REPS):

#         # glass()
#         # string()
#         # fletch()
#         # alch()
#         test()
       
      
  
#     print("Completed process")

# if __name__ == "__main__":
#     main()

# LOOP_REPS = 1

# def fletch():
#         print("fletching 1")
#         sleep(5)
#         playActions("fletch_bow_01.json") 
#         print("fletching 2")
#         sleep(5)
#         playActions("fletch_bow_02.json") 
# def string():
#         print("stringing 1")
#         playActions("string_bow_01.json")
#         print("stringing 2")
#         playActions("string_bow_02.json")
# def glass():
#         playActions("superglass_02.json")
#         print("sleeping for 45s")
#         sleep(45)
#         print("starting")
#         sleep(2)
#         playActions("superglass_03.json")
#         print("sleeping for 45s")
#         sleep(49)
#         print("starting")
#         sleep(2)
#         playActions("superglass_01.json")
#         print("Completed loop")
#         sleep(1)
# def alch():
#         playActions("alch_01.json")
#         sleep(3)
#         playActions("alch_02.json")
#         sleep(2)
#         playActions("alch_03.json")
# def test():
#         print("bezier")
#         sleep(4)
#         playActions("movement_test.json", path_type='bezier')
#         print("spline")
#         sleep(4)
#         playActions("movement_test.json", path_type='spline')
#         playActions("color_coord_test_01.json", path_type='spline', vary_coords=True, variation=0.01)
#         playActions("color_coord_test_pt2_01.json", path_type='spline', vary_coords=True, variation=0.01)
#         playActions("color_coord_ test_01.json")
#         playActions("color_coord_test_pt2_01.json")
