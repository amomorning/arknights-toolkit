import keyboard
import os
import time

from AppKit import NSWorkspace

mp_keys = {
    "q": "adb shell input tap 100 50",
    "w": "adb shell input tap 1600 50",
    "e": "adb shell input tap 1800 50",
    "a": "adb shell input tap 900 350",
    "d": "adb shell input tap 1250 600",
    "c": "adb shell input tap 1650 960",
        }

while True:
    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    if activeAppName == "qemu-system-aarch64":
        for k in mp_keys:
            if keyboard.is_pressed(k):
                stream = os.popen(mp_keys[k])
                if len(stream.read()) > 0:
                    print(stream.read())
                time.sleep(0.1)
        if keyboard.is_pressed('x'):
            while True:
                os.popen(mp_keys['c'])
                time.sleep(2)

                if keyboard.is_pressed('c'):
                    break
        

