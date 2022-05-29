from HandTrackingModule import HandDetector
import cv2, time
import ctrl
import numpy as np


def stretch_detection(lmList, queue):
    result0 = lmList[7][1] - lmList[6][1]
    result1 = lmList[11][1] - lmList[10][1]
    result2 = lmList[15][1] - lmList[14][1]

    ##: 判断是否为伸展状态，并进行状态累加
    if result0 > 30 and result1 > 30 and result2 > 30:
        queue += 1
    else:
        queue = 0

    ##: 状态已经持续5帧，则判断为伸展状态
    if queue == 0x6:
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
    result1 = lmList[11][1] - lmList[12][1]

    if result0 > 4 * result1:
        queue += 1
    else:
        queue = 0

    if queue == 0x6:
        return True, queue
    else:
        return False, queue


def main():
    pTime = 0
    cTime = 0
    targetTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    stretch_queue = 0
    pinch_queue = 0

    stretch_status = 0
    shot_state = 0

    while True:
        if not ctrl.edge_activate():
            time.sleep(2)
        else:
            success, img = cap.read()
            img = detector.findands(img, )
            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                # 判断中间三指是否长时间处于伸展状态
                if stretch_status == 1:
                    interval_time = time.time() - targetTime
                    if (interval_time) > 0.5 and interval_time < 3:
                        if fist_detection(lmList):
                            stretch_status = 0
                            ctrl.edge_screen_shot()
                            # print("catch")
                    elif (time.time() - targetTime) > 3:
                        stretch_status = 0
                        # print("catch_cancel")
                else:
                    stretch_result, stretch_queue = stretch_detection(
                        lmList, stretch_queue)
                    if stretch_result:
                        stretch_status = 1
                        targetTime = time.time()
                        # print("stretch")

                if shot_state == 1:
                    pinch_result, pinch_queue = shot_detection(
                        lmList, pinch_queue)
                    if pinch_result:
                        shot_state = 1
                        targetTime = time.time()
                        print("pinch")

            # cTime = time.time()
            # fps = 1 / (cTime - pTime)
            # pTime = cTime2

            cv2.imshow("img", img)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()