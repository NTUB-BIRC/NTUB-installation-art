# import
import cv2
import numpy
from time import sleep
from myGUI import ShowResultGUI


DEBUG = False


def init():
    cap = cv2.VideoCapture(0)  # 宣告攝影機
    z = numpy.zeros(640)  # 製造 640 個 0 的陣列
    if DEBUG:
        numpy.set_printoptions(threshold=numpy.nan)
        # 設定 print numpy array 時會全部 print 出來，不會省略

    gui = ShowResultGUI()
    gui.start()

    return z, cap, gui


def identification(z, cap, gui):
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
        gui.change_text('紅燈')  # change gui text
        print('y')
    else:
        gui.change_text('綠燈')  # change gui text
        print('n')

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


def close(cap, gui):
    # 釋放所有的資源
    cv2.destroyAllWindows()
    cap.release()
    gui.close()


def main():
    z, cap, gui = init()
    while True:
        try:
            r = identification(z, cap, gui)
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
    input('press any key to exit......')


if __name__ == '__main__':
    main()