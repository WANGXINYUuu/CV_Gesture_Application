# encodeing: utf-8
"""
@project = Final_work
@file = main
@author = XinYu
@create_time = 2022/5/22 15:05
"""
from tkinter import FALSE
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
    if result0 > 130 and result1 > 130 and abs(result2) < 0.5 and abs(
            result3) < 0.5:
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

def Thumb_state(lmList):
    thumb_state = 0
    if lmList[4][1] < lmList[1][1]:
        thumb_state = 1
    elif lmList[4][1] > lmList[1][1]:
        thumb_state = 2
    return thumb_state

def switch_state(lmList):
    x_5, y_5 = lmList[5][1], lmList[5][2]
    x_6, y_6 = lmList[6][1], lmList[6][2]
    x_9, y_9 = lmList[9][1], lmList[9][2]
    x_10, y_10 = lmList[10][1], lmList[10][2]
    try:
        result0 = (y_6 - y_5) / (x_6 - x_5)
        result1 = (y_10 - y_9) / (x_10 - x_9)
    except(ZeroDivisionError):
        return False
    if result0 < -1.0 and result1 < -1.0:
        return True
    else:
        return False

def zoom_state(lmList):
    x_5, y_5 = lmList[5][1], lmList[5][2]
    x_6, y_6 = lmList[6][1], lmList[6][2]
    x_9, y_9 = lmList[9][1], lmList[9][2]
    x_10, y_10 = lmList[10][1], lmList[10][2]
    y_13, y_16 = lmList[13][2], lmList[16][2]
    try:
        result0 = (y_6 - y_5) / (x_6 - x_5)
        result1 = (y_10 - y_9) / (x_10 - x_9)
        print("result0=", result0)
        print("result1=", result1)
    except(ZeroDivisionError):
        return False
    if (result0 < -1.0) and (result1 < -1.0) and (not (y_16 < y_13)):
        return True
    else:
        return False

def updown_state(lmList):
    x_5, y_5 = lmList[5][1], lmList[5][2]
    x_6, y_6 = lmList[6][1], lmList[6][2]
    y_13, y_16 = lmList[13][2], lmList[16][2]
    try:
        result0 = (y_6 - y_5) / (x_6 - x_5)
    except(ZeroDivisionError):
        return False
    if (result0 < -1.0) and (not (y_16 < y_13)):
        return True
    else:
        return False



def main():
    ###########################
    wCam, hCam = 648, 488
    ##########################

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    ctr = pynput.mouse.Controller() # 模拟鼠标
    keyboard = Controller()         # 模拟键盘
    ################################################
    pTime = 0
    thumb_state = 0
    if_hand = 0
    tab_ready_0 = 0
    tab_ready_1 = 0
    ################################################
    stretch_queue = 0
    shot_queue = 0
    stretch_state = 0
    shot_state = 0
    # function_lock = False

    detectorFlip = htm.handDetector(detectionCon=0.7)

    while True:
        success, img = cap.read()
        img = detectorFlip.findHands(img)
        lmList = detectorFlip.findPosition(img, draw=False)
        if len(lmList) >= 21:
            if_hand = 1                                         # 表示画面中有手
        else:
            if_hand = 0    
        cTime = time.time()

        fps = 1/(cTime-pTime)
        pTime = cTime
        if if_hand:
            
            # 判断中间三指是否长时间处于伸展状态
            if stretch_state == 0 and shot_state == 0:
                # function_lock = False
                stretch_result, stretch_queue = stretch_detection(
                    lmList, stretch_queue)
                shot_result, shot_queue = shot_detection(
                    lmList, shot_queue)
                if stretch_result:
                    stretch_state = 1
                    targetTime = time.time()
                elif shot_result:
                    shot_state = 1
                    targetTime = time.time()
                print(stretch_state, shot_state)


            elif shot_state == 1:
                shot_state = 0
                ctrl.edge_exit()
                break

            elif stretch_state == 1:
                # function_lock = True
                interval_time = time.time() - targetTime
                if (interval_time) > 0.5 and interval_time < 1.5:
                    if fist_detection(lmList):
                        stretch_state = 0
                        ctrl.edge_screen_shot()
                elif (time.time() - targetTime) > 1.5:
                    stretch_state = 0



            thumb_state = Thumb_state(lmList)
            if lmList[16][2] > lmList[13][2]:
            #if y_16 > y_13:
                tab_ready_0 = 0
                tab_ready_1 = 0
            else:
                tab_ready_0 = 1


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

if __name__ == "__main__":
    main()