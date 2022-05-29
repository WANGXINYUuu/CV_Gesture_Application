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

def switch_right_page():
    keyboard.press(Key.ctrl)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.release(Key.ctrl)

def switch_left_page():
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.release(Key.shift)
    keyboard.release(Key.ctrl)

def narrow_page():
    keyboard.press(Key.ctrl)
    mouse.scroll(0, 0.01)
    keyboard.release(Key.ctrl)

def amplify_page():
    keyboard.press(Key.ctrl)
    mouse.scroll(0, -0.01)
    keyboard.release(Key.ctrl)