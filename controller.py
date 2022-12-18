#!/usr/bin/env python3

import os
import time
import logging

from pynput.keyboard import Key, Listener
from AppKit import NSWorkspace
import threading


class AdbController:
    def __init__(self):
        self.keyboard2func = {
            "q": self.press_quit,
            "a": self.press_accelerate,
            "d": self.press_pause_via_tap,
            "s": self.press_pause_via_keyevent,
            "w": self.press_retreat,
            "e": self.press_skill,
            "c": self.press_confirm,
            "l": self.toggle_looping_press_confirm,
            "m": self.toggle_mute,
        }
        self._looping_press_confirm_event = threading.Event()
        self._looping_press_confirm_thread = threading.Thread(
            target = self._looping_press_confirm,
            daemon=True
        )
        self._looping_press_confirm_thread.start()

    def _execute(self, cmd, retry=3):
        for _ in range(retry+1):
            if len(os.popen(cmd).read()) == 0:
                break
            time.sleep(0.01)

    def _looping_press_confirm(self, time_interval=2.0):
        while True:
            self._looping_press_confirm_event.wait()
            self.press_confirm()
            time.sleep(time_interval)

    def toggle_looping_press_confirm(self):
        if self._looping_press_confirm_event.is_set():
            self._looping_press_confirm_event.clear()
        else:
            self._looping_press_confirm_event.set()

    def response(self, key : Key):
        key= str(key).strip('\'')
        logging.info("+" + key)
        if key in self.keyboard2func:
            self.keyboard2func[key]()

    def press_quit(self):
        self._execute("adb shell input tap 100 50")
    def press_accelerate(self):
        self._execute("adb shell input tap 1600 50")
    def press_pause_via_tap(self):
        self._execute("adb shell input tap 1800 50")
    def press_pause_via_keyevent(self):
        self._execute("adb shell input keyevent 4")
    def press_retreat(self):
        self._execute("adb shell input tap 900 350")
    def press_skill(self):
        self._execute("adb shell input tap 1250 600")
    def press_confirm(self):
        self._execute("adb shell input tap 1650 960")
    def toggle_mute(self):
        self._execute("adb shell service call audio 9 i32 3 i32 101 i32 1", retry=0)


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
