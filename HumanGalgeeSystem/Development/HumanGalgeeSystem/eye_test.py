import cv2 as cv
import numpy as np


def main():
    cap_width = 960
    cap_height = 540

    # カメラ準備1　###############################################################
    cap1 = cv.VideoCapture(0)
    cap1.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap1.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # カメラ準備2　###############################################################
    cap2 = cv.VideoCapture(1)
    cap2.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap2.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    while True:
        # カメラキャプチャ1　###############################################################
        ret1, image1 = cap1.read()
        if not ret1:
            break
        image1 = cv.flip(image1, 1) #ミラー表示

        # カメラキャプチャ1　###############################################################
        ret2, image2 = cap2.read()
        if not ret2:
            break
        image2 = cv.flip(image2, 1) #ミラー表示

        # キー処理(ESC：終了) #################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映 #############################################################
        cv.imshow('right', image1)
        cv.imshow('left', image2)



if __name__ == '__main__':
    main()
