# Keyboard Mouse Controller (aka mouse keys)

This Python script allows you to control your mouse cursor using your keyboard. It uses the `pynput` library to capture keyboard inputs and move the mouse cursor accordingly.

## Features

- Move the cursor using the arrow keys or Vim bindings (h, j, k, l).
- Accelerate cursor speed by holding the Shift key.
- Decelerate cursor speed by holding the Ctrl key.
- Scroll using the keys w, a, s, d.
- Press the middle mouse button by pressing the Space key.
- Press the left mouse button by pressing the 'e' key.
- Press the right mouse button by pressing the 'r' key.
- Exit the script by pressing the Esc key.

## Note
- This script is only tested on Linux. It may not work on Windows or macOS.
- This script will supress your keyboard input. So, you can't use your keyboard while using this script. by pressing the Esc key you can exit the script.
- This script is not perfect. It may have some bugs. If you find any bugs, please report them.
- This script has to re-open in order to be used again after exiting. that's why it's better to use it with sxhkd or similar tools to start it with a keybinding.

## Use it with sxhkd
1. Download the executable file from the <a href="https://github.com/rootamin/mouse_keys/releases" target="_blank"><b>release</b></a> page.
2. Make the file executable:
```bash
chmod +x mouse_keys-x.run
```
3. You can use the executable file with sxhkd to start it with a keybinding.
4. Add the following line to your `sxhkdrc` file:
```bash
super + m #change this to your desired keybinding
    /path/to/mouse_keys-x.run #change this to the path of the executable file
```
5. Reload the sxhkd configuration:
```bash
pkill -USR1 -x sxhkd
```
6. You can change cursor speed from a config file located in `~/.config/mouse_keys/config` file. The default value is 0.0025 You can change it to your desired value. default generated config:
```bash
[MouseKeys]
speed = 0.0025 # lower is faster
shift_speed = 4 # higher is faster
ctrl_speed = 0.25 # higher is faster
```

## Build it yourself
- This script has good cursor speed for 1920x1080 resolution. If you have a different resolution, you can change the cursor speed by changing the `speed` variable in the `main.py` file. so for that you have to build it yourself.
### Requirements
- Python 3
- pynput library
- pyinstaller library

### Installation 

1. Clone this repository:
```bash
git clone https://github.com/rootamin/mouse_keys.git
cd mouse_keys
```

2. Install the required libraries using pip (a virtual environment is recommended):
```bash
pip install pynput, pyinstaller
```
3. Modify the main.py file to change the cursor speed.
```python
speed = 10 # Change this value to change the cursor speed
```
4. Build the script using pyinstaller:
```bash
pyinstaller --onefile main.py
```
5. The executable file will be in the `dist` folder as `main`.
