from pyboy import PyBoy
from pyboy.utils import WindowEvent
import random

pyboy = PyBoy("resources/PokemonBlue.gb", window="SDL2")

advance_through_intro = 0
intro_done = False

actions = [
    WindowEvent.PRESS_ARROW_UP,
    WindowEvent.PRESS_ARROW_DOWN,
    WindowEvent.PRESS_ARROW_LEFT,
    WindowEvent.PRESS_ARROW_RIGHT,
    WindowEvent.PRESS_BUTTON_A,
]
release_actions = [
    WindowEvent.RELEASE_ARROW_UP,
    WindowEvent.RELEASE_ARROW_DOWN,
    WindowEvent.RELEASE_ARROW_LEFT,
    WindowEvent.RELEASE_ARROW_RIGHT,
    WindowEvent.RELEASE_BUTTON_A,
]

while pyboy.tick():

    if not intro_done:
        # Press A every 60 frames, release after 5 frames, count releases
        if pyboy.frame_count % 60 == 0:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)

        if pyboy.frame_count % 60 == 5:
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
            advance_through_intro += 1
            print(f"Frame: {pyboy.frame_count}, Advance Count: {advance_through_intro}")

            if advance_through_intro >= 100:
                intro_done = True

    else:
        # After intro: random action every 20 frames
        if pyboy.frame_count % 20 == 0:
            pyboy.send_input(random.choice(actions))
        if pyboy.frame_count % 20 == 5:
            for release_action in release_actions:
                try:
                    pyboy.send_input(release_action)
                except:
                    # try a different release if the first fails
                    continue

pyboy.stop()
