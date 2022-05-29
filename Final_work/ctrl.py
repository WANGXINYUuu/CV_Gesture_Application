# encodeing: utf-8
"""
@project = Final_work
@file = ctrl
@author = XinYu
@create_time = 2022/5/24 16:43
"""
import win32gui as w
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

def page_down():
    mouse.scroll(0, 0.01)

def page_up():
    mouse.scroll(0, -0.01)

def edge_activate():
    title = w.GetWindowText(w.GetForegroundWindow())
    if ("Microsoft​ Edge" not in title):
        return False
    else:
        return True

def edge_screen_shot():
    keyboard.press(Key.shift)
    keyboard.press(Key.ctrl)
    keyboard.press('s')
    keyboard.release('s')
    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)

def edge_exit():
    keyboard.press(Key.alt)
    keyboard.press(Key.f4)
    keyboard.release(Key.f4)
    keyboard.release(Key.alt)