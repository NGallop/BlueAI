from pyboy import PyBoy
from pyboy.utils import WindowEvent
import random
import time
import argparse
import sys

### Constants

# Define possible actions and their corresponding release events
ACTIONS_MAP = [
    WindowEvent.PRESS_ARROW_UP,
    WindowEvent.PRESS_ARROW_DOWN,
    WindowEvent.PRESS_ARROW_LEFT,
    WindowEvent.PRESS_ARROW_RIGHT,
    WindowEvent.PRESS_BUTTON_A,
]
RELEASE_MAP = [
    WindowEvent.RELEASE_ARROW_UP,
    WindowEvent.RELEASE_ARROW_DOWN,
    WindowEvent.RELEASE_ARROW_LEFT,
    WindowEvent.RELEASE_ARROW_RIGHT,
    WindowEvent.RELEASE_BUTTON_A,
]

### Main loop

def main(sys_args):

    args = parse_args(sys_args)
    action_repeat = args.fine_control
    duration = args.duration
    speed = args.speed
    window_type = args.window
    start_point = args.start_point
    print(f"Running with action_repeat={action_repeat}, duration={duration}, speed={speed}, start_point={start_point}, window_type={window_type}")

    # For max speed in training later, use window="null"
    pyboy = PyBoy("resources/PokemonBlue.gb", window=window_type)
    pyboy.set_emulation_speed(0)

    # Select route to start from
    if start_point == "intro":
        # Requires play through intro
        progress_through_intro(pyboy)
        print("successfully got through intro")
    elif start_point == "lab":
        pyboy.load_state("resources/save_states/Lab_Pokedex.sgm")
    elif start_point == "grass":
        pyboy.load_state("resources/save_states/Grass_with_pokeballs.sgm")

    # Now: random actions (agent steps)
    # Run for 30 seconds
    start_time = time.time()
    while time.time() - start_time < 60:
        # Press the action
        for _ in range(action_repeat):
            pyboy.send_input(random.choice(ACTIONS_MAP))
            pyboy.tick()
            # Release the action
            for release_event in RELEASE_MAP:
                pyboy.send_input(release_event)
            pyboy.tick(action_repeat)

    pyboy.stop()

### Helper functions

def progress_through_intro(pyboy):
    """
    Progress through the intro sequence by pressing A multiple times.
    """
    intro_done = False
    intro_progress = 0
    while pyboy.tick():
        if not intro_done:
            if pyboy.frame_count % 60 == 0:
                pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            if pyboy.frame_count % 60 == 5:
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
                intro_progress += 1
            if intro_progress >= 100:
                intro_done = True
                break

def parse_args(sys_args):
    parser = argparse.ArgumentParser(description="Run a PyBoy Pokemon Blue agent.")

    parser.add_argument(
        "--start_point",
        choices=["intro", "lab", "grass"],
        default="intro",
        required=False,
        help="Whether to play through the intro sequence."
    )
    parser.add_argument(
        "--speed",
        choices=["max", "normal"], 
        default="max",
        required=False,
        help="Set the emulation speed."
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        required=False,
        help="Duration to run the agent in seconds."
    )
    parser.add_argument(
        "--window",
        choices=["SDL2", "null"],
        default="SDL2",
        required=False,
        help="Type of window to use for PyBoy."
    )
    parser.add_argument(
        "--fine_control",
        default=16,
        type=int,
        required=False,
        help="Number of frames to repeat each action."
    )
    return parser.parse_args(sys_args)

### Entry point

if __name__ == "__main__":
    main(sys.argv[1:])
