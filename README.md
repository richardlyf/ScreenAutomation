# ScreenAutomation

This script allows you to record your key strokes and key presses and playback the events on demand.

This code should work on Windows 10, Mac, and Linux. However it was only tested on Windows10.

## Setup

Clone this repository:
```
git clone https://github.com/richardlyf/ScreenAutomation.git
```

Install requirements:
```
pip install -r requirements.txt
```


### Setup for Windows 10

Open the command prompt and navigate to this repo. 

You can click on the address bar at the top of the File Explorer and type in `cmd` in place of the address to directly open a command prompt.

If you want to setup a virtual environment (For convenience this is optional):
```
pip install virtualenv
virtualenv env -p python3
.\env\Scripts\activate.bat
```

### Setup for WSL (CANCELLED):

To fix Xming error
```
Xlib.error.XauthError: ~/.Xauthority: [Errno 2] No such file or directory: '/home/richardlyf/.Xauthority'
```

Update xlib from source: https://github.com/python-xlib/python-xlib

```
python setup.py install
```

Create virtualenv 3.5. Cannot be 3.7

uninstall python3-Xlib and reinstall from source

sudo apt-get install python3-tk

`ioctl` not supported so RIP...

## Running the example code

```
python main.py
```

The example code records all mouse and keyboard events until ESC is pressed. 

The events are saved and then played back to the user.

Pressing ESC again during playback cancels the playback.
