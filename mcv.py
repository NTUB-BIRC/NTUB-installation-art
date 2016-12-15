"""
Opencv 的 HSV 與一般的 HSV 有所不同

一般：
    Ｈ：色相      0~360度
    Ｓ：飽和度    0~1
    Ｖ：明度      (黑) 0~1 (白)

轉換公式如下

Opencv 版：
    Ｈ：0~180 --> H (一般) / 2
    Ｓ：0~255 --> S (一般) * 255
    Ｖ：0~255 --> V (一般) * 255

參考：http://vincecc.blogspot.tw/2013/09/opencv-extract-colors-hsv.html

RGB、HSV 轉換器：
    RGB to HSV (一般)：http://www.rapidtables.com/convert/color/rgb-to-hsv.htm
    HSV 一般 to RGB：http://www.rapidtables.com/convert/color/hsv-to-rgb.htm
"""


# import
import cv2
import imutils
import numpy as np
from myGUI import ShowResultGUI
# from imutils.object_detection import non_max_suppression


DEBUG = False


def init():
    cap = cv2.VideoCapture(0)  # 宣告攝影機
    z = np.zeros(640)  # 製造 640 個 0 的陣列
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    if DEBUG:
        # 設定 print numpy array 時會全部 print 出來，不會省略
        np.set_printoptions(threshold=np.nan)

    # GUI init and start
    gui = ShowResultGUI()
    gui.start()

    return z, cap, gui, hog


def identification(z, cap, gui, hog):
    # 啟用攝影機
    _, frame = cap.read()

    # 讀取攝影機影像
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 設定下限（H, S, V）
    lower_red = np.array([175, 150, 0])

    # 設定上限（H, S, V）
    upper_red = np.array([255, 255, 255])

    # 設定遮罩，在遮罩範圍內的顏色為白色其他黑色
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # 將 mask 中的白色部份套回原來的顏色，其餘部份維持黑色
    res = cv2.bitwise_and(frame, frame, mask=mask)

    count = 0

    # 計算有多少點
    for dot in mask:
        if np.any(np.not_equal(dot, z)):
            count += 1

    # test red in 100 up row
    if count >= 100:
        result, image = detect_human(mask, hog)
        if result and image is not None:
            cv2.imshow("After NMS", image)  # show red human
            print('detect red human')
            gui.change_text('出現小紅人')
        else:
            print('red detect')
            gui.change_text('出現紅物體')
    else:
        print('nothing red')
        gui.change_text('沒有紅色物體')

    # 將抓到的東西顯示出來
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    # 按 Esc 退出
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        return False
    else:
        return True


def detect_human(mask, hog):
    # resize
    image = imutils.resize(mask, width=min(400, mask.shape[1]))

    # detect human
    (rects, weights) = hog.detectMultiScale(image,
                                            winStride=(4, 4),
                                            padding=(8, 8),
                                            scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

    # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    # for (xA, yA, xB, yB) in pick:
    # cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    if np.any(rects):
        return True, image
    else:
        return False, None


def close(cap, gui):
    # 釋放所有的資源
    cv2.destroyAllWindows()
    cap.release()
    gui.close()


def main():
    z, cap, gui, hog = init()
    while True:
        try:
            r = identification(z, cap, gui, hog)
        except KeyboardInterrupt as k:
            print('\nbreak by user')
            break
        except RuntimeError:
            print('\nGUI close by user')
            break
        except Exception as e:
            raise e
        else:
            if not r:
                print('\nbreak by user')
                break

    close(cap, gui)


if __name__ == '__main__':
    main()
