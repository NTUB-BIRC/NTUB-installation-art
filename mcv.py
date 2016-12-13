# import
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

# 宣告攝影機
cap = cv2.VideoCapture(0)
z = np.zeros(640)

# np.set_printoptions(threshold=np.nan)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    # 啟用攝影機
    _, frame = cap.read()
    # 讀取攝影機影像
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 設定下限（R, G, B）
    lower_red = np.array([175, 150, 0])
    # 設定上限（R, G, B）
    upper_red = np.array([255, 255, 255])
    # 設定遮罩，在遮罩範圍內的顏色為白色其他黑色
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # 將 mask 中的白色部份套回原來的顏色，其餘部份維持黑色
    res = cv2.bitwise_and(frame, frame, mask=mask)
    count = 0

    for dot in mask:
        if np.any(np.not_equal(dot, z)):
            count += 1

    # test red in 100 up row
    if count >= 100:
        print('red detect')

        # resize
        image = imutils.resize(mask, width=min(400, mask.shape[1]))

        # detect human
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	# draw the final bounding boxes
        # for (xA, yA, xB, yB) in pick:
        #     cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        if np.any(rects):
            print('detect red human')
            cv2.imshow("After NMS", image)

    # 將抓到的東西顯示出來
    cv2.imshow('f', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
