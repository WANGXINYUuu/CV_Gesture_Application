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
###########################
wCam, hCam = 648, 488
##########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

ctr = pynput.mouse.Controller() # 模拟鼠标
keyboard = Controller()         # 模拟键盘

pTime = 0
x_p, y_p = 0, 0
x_c, y_c = 0, 0
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
        if_hand = 1     # 表示画面中有手
        # print(lmList[8])
        x_c, y_c = lmList[8][1], lmList[8][2]

        x_1, y_1 = lmList[1][1], lmList[1][2]
        x_3, y_3 = lmList[3][1], lmList[3][2]
        x_4, y_4 = lmList[4][1], lmList[4][2]
        x_5, y_5 = lmList[5][1], lmList[5][2]
        x_6, y_6 = lmList[6][1], lmList[6][2]
        x_7, y_7 = lmList[7][1], lmList[7][2]
        x_8, y_8 = lmList[8][1], lmList[8][2]
        x_9, y_9 = lmList[9][1], lmList[9][2]
        x_10, y_10 = lmList[10][1], lmList[10][2]
        x_11, y_11 = lmList[11][1], lmList[11][2]
        x_12, y_12 = lmList[12][1], lmList[12][2]
        x_13, y_13 = lmList[13][1], lmList[13][2]
        x_16, y_16 = lmList[16][1], lmList[16][2]

        
    else:
        if_hand = 0     # 表示画面中没手
    cTime = time.time()

    # flip_y = (y_c-y_p)/(cTime-pTime)
    fps = 1/(cTime-pTime)
    # x_p, y_p =x_c, y_c
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
        if (y_8 < y_7) and (y_7 < y_6) and (y_6 < y_5) and (y_12 < y_11) and (y_11 < y_10) and (y_10 < y_9) and (tab_ready_0 and (not tab_ready_1)):
            ctrl.switch_right_page()
            tab_ready_1 = tab_ready_0
        elif (y_8 < y_7) and (y_7 < y_6) and (y_6 < y_5) and (y_12 < y_11) and (y_11 < y_10) and (y_10 < y_9):
            ctrl.narrow_page()
        elif (y_8<y_7) and (y_7<y_6) and (y_6<y_5):
            ctrl.page_down()
        else:
            pass
    elif thumb_state == 2:
        if (y_8 < y_7) and (y_7 < y_6) and (y_6 < y_5) and (y_12 < y_11) and (y_11 < y_10) and (y_10 < y_9) and (tab_ready_0 and (not tab_ready_1)):
            ctrl.switch_left_page()
            tab_ready_1 = tab_ready_0
        elif (y_8 < y_7) and (y_7 < y_6) and (y_6 < y_5) and (y_12 < y_11) and (y_11 < y_10) and (y_10 < y_9):
            ctrl.amplify_page()
        elif (y_8<y_7) and (y_7<y_6) and (y_6<y_5):
            ctrl.page_up()
        else:
            pass
    else:
        pass
    
    
    cv2.putText(img, f'FPS:{int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
