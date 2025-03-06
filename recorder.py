import os
import pyautogui as gui
import mouse
import keyboard
import pickle
import time
import threading
from queue import Queue
from collections import namedtuple
from mouse._mouse_event import ButtonEvent, MoveEvent, WheelEvent, UP
from keyboard._keyboard_event import KEY_DOWN

Event = namedtuple('Event', ['type', 'event'])


class Recorder:
    """
    The Recorder class records the key strokes and mouse movements for a given screen resolution.
    The sequence of actions are saved and can then be played back on demand.
    """
    def __init__(self):
        """
        screen_resolution: (width, height)
        """
        screen_resolution = gui.size()
        self.resolution = str(screen_resolution[0]) + "_" + str(screen_resolution[1])
        self.mouse_events_queue = Queue()
        self.keyboard_events_queue = Queue()
        self.events = None
        self.stop_replay = False


    def record(self, escape_key="esc"):
        """
        Records all the key press and mouse movements and return a list of recorded events.
        Pressing the escape_key stops the recording.
        Returns the recorded events.
        """
        self.stop_replay = False
        mouse.hook(self.mouse_events_queue.put)
        keyboard.start_recording(self.keyboard_events_queue)
        print("Recoding until esc is pressed...")
        keyboard.wait(escape_key)
        mouse.unhook(self.mouse_events_queue.put)
        keyboard.stop_recording()

        events_queue = self.merge(self.mouse_events_queue, self.keyboard_events_queue)
        self.events = list(events_queue.queue)
        print("Recording completed.")
        return self.events


    def play(self, record_file=None, escape_key="esc"):
        """
        Optionally takes in a record_file and replays the recorded events.
        If no such file is provided, replay events that are already in the recorder.
        Pressing the escape_key stops the play back immediately.
        """
        if record_file != None:
            file_name = os.path.basename(record_file)
            resolution = file_name[:file_name.find("_", file_name.find("_") + 1)]
            if resolution != self.resolution:
                print("The resolution of the playback doesn't match current screen resolution!")
                return
            with open(record_file, 'rb') as f:
                self.events = pickle.load(f)
        if self.events == None:
            return

        cv = threading.Event()
        play_thread = threading.Thread(target=self._thread_play, args=(cv, self.events,))
        interrupt_thread = threading.Thread(target=self._thread_interrupt, args=(cv, escape_key,))
        interrupt_thread.daemon = True
        print("Playing recorded events...")
        interrupt_thread.start()
        play_thread.start()
        play_thread.join()
        print("Playback Finished!")


    def save_recording(self, filename, save_dir="saved_recordings"):
        """
        Saves the recording as a pickle object that can be loaded and played back.
        """
        if self.events == None:
            print("No recording to save!")
            return
        os.makedirs(save_dir, exist_ok=True)
        filename = self.resolution + "_" + filename
        save_path = os.path.join(save_dir, filename)
        with open(save_path, 'wb') as f:
            pickle.dump(self.events, f)
        print("Recording saved as: " + save_path)


    def merge(self, mouse_events_queue, keyboard_events_queue):
        """
        Merge recorded mouse and keyboard events into one queue based on recorded time.
        """
        events_queue = Queue()
        mouse_event = None
        keyboard_event = None
        while mouse_events_queue.qsize() != 0 or keyboard_events_queue.qsize() != 0:
            if mouse_event == None and mouse_events_queue.qsize() != 0:
                mouse_event = mouse_events_queue.get()
            if keyboard_event == None and keyboard_events_queue.qsize() != 0:
                keyboard_event = keyboard_events_queue.get()

            if mouse_event and (not keyboard_event or mouse_event.time <= keyboard_event.time):
                events_queue.put(Event('mouse', mouse_event))
                mouse_event = None
                mouse_events_queue.task_done()
            elif keyboard_event and (not mouse_event or keyboard_event.time < mouse_event.time):
                events_queue.put(Event('keyboard', keyboard_event))
                keyboard_event = None
                keyboard_events_queue.task_done()
        return events_queue


    def _thread_play(self, cv, events, speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True):
        """
        Thread that plays both the mouse and keyboard events back.
        This thread will stop the playback if stop_replay == True
        """
        last_time = None
        state = keyboard.stash_state()
        start = time.time()
        total_wait_time = 0
        for event_type, event in events:
            # Awaken interrupt thread to check for exit status
            cv.set()
            if self.stop_replay:
                return
            if speed_factor > 0 and last_time is not None:
                wait_time = (event.time - last_time) / speed_factor
                # Compensate for delays in execution
                # Compare actual time taken to time we should have waited for and compensate
                delay = (time.time() - start) - total_wait_time
                time.sleep(max(0, wait_time - delay))
                total_wait_time += wait_time
            last_time = event.time

            if event_type == 'mouse':
                if isinstance(event, ButtonEvent) and include_clicks:
                    if event.event_type == UP:
                        gui.mouseUp(button=event.button)
                    else:
                        gui.mouseDown(button=event.button)
                elif isinstance(event, MoveEvent) and include_moves:
                    mouse.move(event.x, event.y)
                elif isinstance(event, WheelEvent) and include_wheel:
                    mouse.wheel(event.delta)
            elif event_type == 'keyboard':
                key = event.name or event.scan_code
                keyboard.press(key) if event.event_type == KEY_DOWN else keyboard.release(key)
            else:
                raise Exception("Incorrect type of event")
        keyboard.restore_modifiers(state)


    def _thread_interrupt(self, cv, escape_key):
        while True:
            cv.wait()
            cv.clear()
            if keyboard.is_pressed(escape_key):
                self.stop_replay = True
                print("Play back cancelled!")
                break


