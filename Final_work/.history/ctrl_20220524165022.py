# encodeing: utf-8
"""
@project = Final_work
@file = ctrl
@author = XinYu
@create_time = 2022/5/24 16:43
"""

from pynput.keyboard import Key, Controller
import pynput

mouse = pynput.mouse.Controller()
keyboard = Controller()

def switch_page():
    keyboard.press(Key.ctrl)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.release(Key.ctrl)
    