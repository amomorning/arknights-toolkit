#!/usr/bin/env python3

import os
import time
import logging

from pynput.keyboard import Key, Listener
from AppKit import NSWorkspace


class AdbController:
    def __init__(self):
        self.keyboard2func = {
            "q": self.press_quit,
            "a": self.press_accelerate,
            "s": self.press_pause,
            "w": self.press_retreat,
            "e": self.press_skill,
            "c": self.press_confirm,
        }

    def _execute(self, cmd, retry=10):
        for _ in range(max(1, retry)):
            if len(os.popen(cmd).read()) == 0:
                break
            time.sleep(0.1)

    def response(self, key : Key):
        key= str(key).strip('\'')
        logging.info("+" + key)
        if key in self.keyboard2func:
            self.keyboard2func[key]()

    def press_quit(self):
        self._execute("adb shell input tap 100 50")
    def press_accelerate(self):
        self._execute("adb shell input tap 1600 50")
    def press_pause(self):
        self._execute("adb shell input tap 1800 50")
    def press_retreat(self):
        self._execute("adb shell input tap 900 350")
    def press_skill(self):
        self._execute("adb shell input tap 1250 600")
    def press_confirm(self):
        self._execute("adb shell input tap 1650 960")


class KeybaordMonitor:
    def __init__(self):
        self.adb_controller = AdbController()
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key : Key):
        # We should not make any response if the event is not from arknights.
        if NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'] == "qemu-system-aarch64":
            self.adb_controller.response(key)

    def on_release(self, key):
        pass

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    monitor = KeybaordMonitor()
