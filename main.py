from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
import time
import os

mouse_controller = mouse.Controller()

step_size = 1

# Define the speed of the mouse
speed = 0.0025
scroll_speed = 0.2

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
        dx *= 4
        dy *= 4
    elif key_state[Key.ctrl]:
        dx /= 4
        dy /= 4

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
