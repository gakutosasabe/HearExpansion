#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse

import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--model_complexity",
                        help='model_complexity(0,1(default))',
                        type=int,
                        default=1)

    parser.add_argument("--max_num_hands", type=int, default=2)
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    parser.add_argument('--use_brect', action='store_true')
    parser.add_argument('--plot_world_landmark', action='store_true')

    args = parser.parse_args()

    return args


def main():
    # 引数解析 ###############################################################
    args = get_args()

    cap_device = args.device
    cap_width = 960
    cap_height = 540

    model_complexity = args.model_complexity

    max_num_hands = args.max_num_hands
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = args.use_brect
    plot_world_landmark = args.plot_world_landmark



    # カメラ準備　###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    while True:
        # カメラキャプチャ　###############################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1) #ミラー表示

        # 検出実施　###############################################################
        image = cv.cvtColor(image, cv.COLOR_BAYER_BG2RGB)

        # 顔位置＆場所検出 ###############################################################
        posX,posY,posZ,sizeW,sizeH = culculate_face_pos_and_size(cap)
    
    
    
    
    
    faceimage = trim_face(posX,posY,posZ,sizeW,sizeH,video)
    girlimage = conv_face2girl(faceimage)

    
    return

def culculate_face_pos_and_size(image):

    
    
    return posX,posY,posZ,sizeW,sizeH

def resize_illustsize(image,posZ):

    return resize_image

def trim_face(posX,posY,posZ,sizeW,sizeH,video):
    
    return faceimage

def conv_face2girl(faceimage):

    return girlimage




if __name__ == '__main__':
    main()

