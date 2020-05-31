import pyautogui as gui
import mouse
import keyboard
import time
import threading
from queue import Queue
from collections import namedtuple
from mouse._mouse_event import ButtonEvent, MoveEvent, WheelEvent, UP
from keyboard._keyboard_event import KEY_DOWN


class Recorder:
    """
    The Recorder class records the key strokes and mouse movements for a given screen resolution.
    The sequence of actions are saved and can then be played back on demand.
    """
    def __init__(screen_resolution, escape_key):
        """
        screen_resolution: (width, height)
        """
        self.screen_resolution = screen_resolution


    def record():
        """
        Records all the key press and mouse movements and return a list of recorded events.
        """
        pass


    def save_recording(filename, save_dir="saved_recordings"):
        """
        Saves the recording as a npy object that can be loaded and played back.
        """
        pass