import numpy
import cv2

cap = cv2.VideoCapture(0)
z = numpy.zeros(640)

numpy.set_printoptions(threshold=numpy.nan)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = numpy.array([175, 150, 0])
    upper_red = numpy.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    count = 0

    for dot in mask:
        if numpy.any(numpy.not_equal(dot, z)):
            count += 1

    if count >= 100:
        print('y')
    cv2.imshow('f', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
