import keyboard
from time import sleep


def move_left(interval):
    keyboard.press("left")
    sleep(interval)
    keyboard.release("left")


def move_right(interval):
    keyboard.press("right")
    sleep(interval)
    keyboard.release("right")


def jump(interval):
    keyboard.press("up")
    sleep(interval)
    keyboard.release("up")


def kick(interval):
    keyboard.press("space")
    sleep(interval)
    keyboard.release("space")


def wait_for_space_press():
    keyboard.wait("space")


def start_listening_for_s_press(callback):
    keyboard.add_hotkey("s", callback)


def stop_listening_for_s_press():
    keyboard.remove_hotkey("s")
