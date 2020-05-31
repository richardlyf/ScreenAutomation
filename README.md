# ScreenAutomation

For WSL:

Xming
```
Xlib.error.XauthError: ~/.Xauthority: [Errno 2] No such file or directory: '/home/richardlyf/.Xauthority'
```

Update xlib from source: https://github.com/python-xlib/python-xlib

```
python setup.py install
```

create virtualenv 3.5. Cannot be 3.7
pip install pyautogui
uninstall python3-Xlib and reinstall from source
sudo apt-get install python3-tk

ioctl not supported so rip