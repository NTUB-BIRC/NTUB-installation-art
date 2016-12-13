# import
import numpy
import cv2
from time import sleep

cap = cv2.VideoCapture(0)  # 宣告攝影機
z = numpy.zeros(640)

numpy.set_printoptions(threshold=numpy.nan)

while True:
    # 啟用攝影機
    _, frame = cap.read()
    # 讀取攝影機影像
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 設定下限（R, G, B）
    lower_red = numpy.array([175, 150, 0])
    # 設定上限（R, G, B）
    upper_red = numpy.array([255, 255, 255])
    # 設定遮罩，在遮罩範圍內的顏色為白色其他黑色
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # 將 mask 中的白色部份套回原來的顏色，其餘部份維持黑色
    res = cv2.bitwise_and(frame, frame, mask=mask)
    count = 0
    # 計算有多少點
    for dot in mask:
        if numpy.any(numpy.not_equal(dot, z)):
            count += 1

    # 如果超過 100 個點，就印 y 不然印 n
    if count >= 100:
        print('y')
    else:
        print('n')

    # 將抓到的東西顯示出來
    cv2.imshow('f', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    # 按 Esc 退出
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


# 釋放所有的資源
cv2.destroyAllWindows()
cap.release()
