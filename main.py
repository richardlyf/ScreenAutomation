import os, sys
import pyautogui as gui
import webbrowser
import time
import cv2
import numpy as np
import mouse
import keyboard

MAX_DELAY = 15 # Seconds

def init():
    # Throw exception if mouse is at top left corner
    gui.FAILSAFE = True
    # Change CWD to this file's directory
    os.chdir(sys.path[0])
    size = gui.size()
    return size


def check_timeout(start_time):
    if time.time() - start_time > MAX_DELAY:
        print("Request timed out")
        sys.exit(1)


def open_axess(screen_resolution):
    width, height = screen_resolution
    img_dir = os.path.join(os.getcwd(), "images/axess/")

    urL = "axess.stanford.edu"
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path), 1)
    webbrowser.get("chrome").open(urL)
    time.sleep(3)

    # Attempt to login
    # login_loc = None
    # region = (0, 0, width, height)
    # start_time = time.time()
    # while not login_loc:
    #     check_timeout(start_time)
    #     start = time.time()
    #     login_loc = gui.locateOnScreen(img_dir + "login.png", region=region, grayscale=True, confidence=0.6)
    #     print(time.time() - start)
    # gui.moveTo(*login_loc[:2])
    # gui.click()
    # time.sleep(2)

    img = gui.screenshot()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("grey", img)
    template = cv2.imread(img_dir + "login.png",0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    print(res)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)


    cv2.imshow("result", img)
    cv2.waitKey(0)


def main():
    screen_resolution = init()
    open_axess(screen_resolution)


if __name__ == '__main__':
    main()