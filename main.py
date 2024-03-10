from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
import time
import os
import configparser

import os.path

mouse_controller = mouse.Controller()

step_size = 1

# Read config file
config = configparser.ConfigParser()
config_file = os.path.expanduser("~/.config/mouse_keys/config")
if os.path.isfile(config_file):
    config.read(config_file)
    speed = float(config.get("MouseKeys", "speed", fallback="0.0025"))
    shift_speed = float(config.get("MouseKeys", "shift_speed", fallback="4"))
    ctrl_speed = float(config.get("MouseKeys", "ctrl_speed", fallback="0.25"))
else:
    speed = 0.0025 # smaller is faster
    shift_speed = 4
    ctrl_speed = 0.25
    # Generate config file with default values
    config["MouseKeys"] = {
        "speed": str(speed),
        "shift_speed": str(shift_speed),
        "ctrl_speed": str(ctrl_speed)
    }
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, "w") as file:
        config.write(file)

key_state = {
    Key.up: False,
    Key.down: False,
    Key.left: False,
    Key.right: False,

    # vim bindings
    KeyCode.from_char('h'): False,
    KeyCode.from_char('j'): False,
    KeyCode.from_char('k'): False,
    KeyCode.from_char('l'): False,

    Key.shift: False,
    Key.ctrl: False,

    Key.space: False,
    KeyCode.from_char('r'): False,
    KeyCode.from_char('e'): False,
    KeyCode.from_char('w'): False,
    KeyCode.from_char('s'): False,
    KeyCode.from_char('a'): False,
    KeyCode.from_char('d'): False,

    Key.esc: False
}

def on_press(key):
    if key in key_state:
        key_state[key] = True
    if key == Key.esc:  # If Esc key is pressed, exit the script
        os._exit(0)

def on_release(key):
    if key in key_state:
        key_state[key] = False

listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)
listener.start()

accumulated_dx, accumulated_dy = 0, 0

# Main loop
while True:
    dx, dy = 0, 0
    if key_state[Key.up] or key_state[KeyCode.from_char('k')]:
        dy -= step_size
    if key_state[Key.down] or key_state[KeyCode.from_char('j')]:
        dy += step_size
    if key_state[Key.left] or key_state[KeyCode.from_char('h')]:
        dx -= step_size
    if key_state[Key.right] or key_state[KeyCode.from_char('l')]:
        dx += step_size

    # Adjust the cursor speed size based on the state of the shift and ctrl keys
    if key_state[Key.shift]:
        dx *= shift_speed
        dy *= shift_speed
    elif key_state[Key.ctrl]:
        dx *= ctrl_speed
        dy *= ctrl_speed

    accumulated_dx += dx
    accumulated_dy += dy

    if abs(accumulated_dx) >= 1:
        dx = int(accumulated_dx)
        accumulated_dx -= dx
    else:
        dx = 0

    if abs(accumulated_dy) >= 1:
        dy = int(accumulated_dy)
        accumulated_dy -= dy
    else:
        dy = 0

    # mouse scroll
    mx, my = 0, 0
    if key_state[KeyCode.from_char('w')]:
        my += step_size
    if key_state[KeyCode.from_char('s')]:
        my -= step_size
    if key_state[KeyCode.from_char('a')]:
        mx -= step_size
    if key_state[KeyCode.from_char('d')]:
        mx += step_size

    if key_state[Key.space]:
        mouse_controller.press(mouse.Button.middle)
    elif key_state[KeyCode.from_char('e')]:
        mouse_controller.press(mouse.Button.left)
    elif key_state[KeyCode.from_char('r')]:
        mouse_controller.press(mouse.Button.right)

    if not key_state[Key.space]:
        mouse_controller.release(mouse.Button.middle)
    if not key_state[KeyCode.from_char('e')]:
        mouse_controller.release(mouse.Button.left)
    if not key_state[KeyCode.from_char('r')]:
        mouse_controller.release(mouse.Button.right)

    mouse_controller.move(dx, dy)
    mouse_controller.scroll(mx, my)
    time.sleep(speed)
