import pyautogui as gui
import mouse
import keyboard
import time
import threading
from queue import Queue
from collections import namedtuple
from mouse._mouse_event import ButtonEvent, MoveEvent, WheelEvent, UP
from keyboard._keyboard_event import KEY_DOWN

Event = namedtuple('Event', ['type', 'event'])
stop_thread = False

def merge(mouse_events_queue, keyboard_events_queue):
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


def play(events, speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True):
    """
    Plays both the mouse and keyboard events back.
    """
    print("Playing recorded events...")
    last_time = None
    for event_type, event in events:
        if stop_thread:
            return
        if speed_factor > 0 and last_time is not None:
            time.sleep((event.time - last_time) / speed_factor)
        last_time = event.time

        if event_type == 'mouse':
            if isinstance(event, ButtonEvent) and include_clicks:
                if event.event_type == UP:
                    mouse.release(event.button)
                else:
                    mouse.press(event.button)
            elif isinstance(event, MoveEvent) and include_moves:
                mouse.move(event.x, event.y)
            elif isinstance(event, WheelEvent) and include_wheel:
                mouse.wheel(event.delta)
        elif event_type == 'keyboard':
            state = keyboard.stash_state()
            key = event.name or event.scan_code
            keyboard.press(key) if event.event_type == KEY_DOWN else keyboard.release(key)
            keyboard.restore_modifiers(state)
        else:
            raise Exception("Incorrect type of event")


def interrupt(interrupt_key):
    keyboard.wait(interrupt_key)
    global stop_thread
    stop_thread = True
    print("Play back cancelled!")


def main():
    mouse_events_queue = Queue()
    keyboard_events_queue = Queue()

    mouse.hook(mouse_events_queue.put)
    keyboard.start_recording(keyboard_events_queue)
    print("Recoding until esc is pressed...")
    keyboard.wait("esc")
    mouse.unhook(mouse_events_queue.put)
    keyboard.stop_recording()

    events_queue = merge(mouse_events_queue, keyboard_events_queue)

    play_thread = threading.Thread(target=play, args=(list(events_queue.queue),))
    interrupt_thread = threading.Thread(target=interrupt, args=("esc",))
    interrupt_thread.daemon = True
    interrupt_thread.start()
    play_thread.start()
    play_thread.join()
    print("Program Finished!")


if __name__ == '__main__':
    main()