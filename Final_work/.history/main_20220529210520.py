# encodeing: utf-8
"""
@project = Final_work
@file = main
@author = XinYu
@create_time = 2022/5/22 15:05
"""
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import pynput
from pynput.keyboard import Key, Controller
import math
import ctrl


def stretch_detection(lmList, queue):
    try:
        result0 = lmList[8][1] - lmList[5][1]
        result1 = lmList[12][1] - lmList[9][1]
        result2 = (lmList[8][2] - lmList[5][2]) / result0
        result3 = (lmList[12][2] - lmList[9][2]) / result1
    except (ZeroDivisionError):
        return False, queue

    ##: 判断是否为伸展状态，并进行状态累加
    if result0 > 130 and result1 > 130 and abs(result2) < 0.2 and abs(
            result3) < 0.2:
        queue += 1
    else:
        queue = 0

    ##: 状态已经持续5帧，则判断为伸展状态
    if queue == 0x3:
        queue = 0
        return True, queue
    else:
        return False, queue


def fist_detection(lmList):
    result0 = lmList[7][1] - lmList[6][1]
    result1 = lmList[11][1] - lmList[10][1]
    result2 = lmList[15][1] - lmList[14][1]

    if result0 < 0 and result1 < 0 and result2 < 0:
        return True
    else:
        return False


def shot_detection(lmList, queue):
    result0 = lmList[8][1] - lmList[5][1]
    result1 = lmList[10][1] > lmList[11][1] and lmList[11][1] > lmList[12][1]
    result2 = lmList[14][1] > lmList[15][1] and lmList[15][1] > lmList[16][1]
    if result0 > 80 and result1 and result2:
        queue += 1
    else:
        queue = 0

    if queue == 0x20:
        return True, queue
    else:
        return False, queue

def switch_state(lmList):
    x_5, y_5 = lmList[5][1], lmList[5][2]
    x_8, y_8 = lmList[8][1], lmList[8][2]
    x_9, y_9 = lmList[9][1], lmList[9][2]
    x_12, y_12 = lmList[12][1], lmList[12][2]
    result0 = (y_8 - y_5) / (x_8 - x_5)
    result1 = (y_12 - y_9) / (x_12 - x_9)
    if result0 < -1.2 and result1 < -1.2:
        return True
    else:
        return False

def zoom_state(lmList):
    x_5, y_5 = lmList[5][1], lmList[5][2]
    x_8, y_8 = lmList[8][1], lmList[8][2]
    x_9, y_9 = lmList[9][1], lmList[9][2]
    x_12, y_12 = lmList[12][1], lmList[12][2]
    y_13, y_16 = lmList[13][2], lmList[16][2]
    result0 = (y_8 - y_5) / (x_8 - x_5)
    result1 = (y_12 - y_9) / (x_12 - x_9)
    if (result0 < -1.2) and (result1 < -1.2) and (not (y_16 < y_13)):
        return True
    else:
        return False

def updown_state(lmList):
    x_5, y_5 = lmList[5][1], lmList[5][2]
    x_8, y_8 = lmList[8][1], lmList[8][2]
    y_13, y_16 = lmList[13][2], lmList[16][2]
    result0 = (y_8 - y_5) / (x_8 - x_5)
    if (result0 < -1.2) and (not (y_16 < y_13)):
        return True
    else:
        return False

###########################
wCam, hCam = 648, 488
##########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

ctr = pynput.mouse.Controller() # 模拟鼠标
keyboard = Controller()         # 模拟键盘

pTime = 0
x_1, y_1 = 0, 0
x_3, y_3 = 0, 0
x_4, y_4 = 0, 0
x_5, y_5 = 0, 0
x_6, y_6 = 0, 0
x_7, y_7 = 0, 0
x_8, y_8 = 0, 0
x_9, y_9 = 0, 0
x_10, y_10 = 0, 0
x_11, y_11 = 0, 0
x_12, y_12 = 0, 0
x_13, y_13 = 0, 0
x_16, y_16 = 0, 0
thumb_state = 0
if_hand = 0
tab_ready_0 = 0
tab_ready_1 = 0
detectorFlip = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = detectorFlip.findHands(img)
    lmList = detectorFlip.findPosition(img, draw=False)
    if len(lmList) != 0:
        if_hand = 1                                         # 表示画面中有手
    else:
        if_hand = 0     # 表示画面中没手
    cTime = time.time()

    fps = 1/(cTime-pTime)
    pTime = cTime
    if if_hand:
        if x_4<x_1:
            thumb_state = 1
        elif x_4>x_1:
            thumb_state = 2
        else:
            pass

        if y_16 > y_13:
            tab_ready_0 = 0
            tab_ready_1 = 0
        else:
            tab_ready_0 = 1
    else:
        pass
    if thumb_state == 1:
        if switch_state(lmList) and (tab_ready_0 and (not tab_ready_1)):
            ctrl.switch_right_page()
            tab_ready_1 = tab_ready_0
        elif zoom_state(lmList):
            ctrl.narrow_page()
        elif updown_state(lmList):
            ctrl.page_down()
        else:
            pass
    elif thumb_state == 2:
        if switch_state(lmList) and (tab_ready_0 and (not tab_ready_1)):
            ctrl.switch_left_page()
            tab_ready_1 = tab_ready_0
        elif zoom_state(lmList):
            ctrl.amplify_page()
        elif updown_state(lmList):
            ctrl.page_up()
        else:
            pass
    else:
        pass
    
    

    cv2.putText(img, f'FPS:{int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
