#!/usr/bin/env python3

import click
import logging

from controller_v2 import AdbController

@click.group()
def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


@main.command()
@click.option('--mode',
              type=click.Choice(['adb', 'screen'], case_sensitive=False),
              default='adb')
@click.option('--time-interval', default=2.0)
def run(mode, time_interval):
    if mode == 'adb':
        adb_controller = AdbController()
        adb_controller.looping_press_confirm(time_interval)
    elif mode == 'screen':
        import pyautogui
        pyautogui.PAUSE = time_interval
        while True:
            pyautogui.press('c')


if __name__ == '__main__':
    main()
