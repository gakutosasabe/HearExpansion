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
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)

    parser.add_argument('--use_brect', action='store_true')

    args = parser.parse_args()

    return args


def main():
    # 引数解析 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    min_detection_confidence = args.min_detection_confidence

    use_brect = args.use_brect

    # カメラ準備 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        min_detection_confidence=min_detection_confidence)

    # FPS計測モジュール ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=10)

    while True:
        display_fps = cvFpsCalc.get()

        # カメラキャプチャ #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # ミラー表示
        overlay_image = copy.deepcopy(image)

        # 検出実施 #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = face_detection.process(image)

        # 描画 ################################################################
        if results.detections is not None:
            for detection in results.detections:
                # 描画
                image,posX,posY,sizeW,sizeH = culculate_face_pos_and_size(image, detection)
                overlay_image = overlay_illust(image,posX,posY,sizeH)
    
        cv.putText(overlay_image, "FPS:" + str(display_fps), (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)

        # キー処理(ESC：終了) #################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映 #############################################################
        cv.imshow('MediaPipe Face Detection Demo', overlay_image)

    cap.release()
    cv.destroyAllWindows()



# 顔のx座標,y座標,幅，高さを抽出　###############################################################
def culculate_face_pos_and_size(image,detection):
    image_width, image_height = image.shape[1], image.shape[0]
    bbox = detection.location_data.relative_bounding_box
    sizeW = int(bbox.width * image_width)
    sizeH = int(bbox.height * image_height)
    posX = int(bbox.xmin * image_width + (sizeW/2))
    posY = int(bbox.ymin * image_height + (sizeH/2))
    
    cv.putText(image, "posX:" + str(posX) + " posY:" + str(posY) + " sizeW" + str(sizeW) + " sizeH" + str(sizeH),
               (10,30),cv.FONT_HERSHEY_SIMPLEX,1.0,(0,255,0),2,cv.LINE_AA)
    
    return image, posX,posY,sizeW,sizeH

# 笑い男画像をresizeして透明化して重ねる
def overlay_illust(bg,posX,posY,sizeH):
    laugh_man = cv.imread("/home/pi/hearexpansion/HumanGalgeeSystem/Development/HumanGalgeeSystem/ToRaspberrypi/warai_flat.png",cv.IMREAD_UNCHANGED)  # アルファチャンネル込みで読み込む)
    resize_laugh_man = cv.resize(laugh_man, dsize=None, fx=0.4, fy=0.4)
    resize_laugh_man_height = resize_laugh_man.shape[0]
    resize_laugh_man_width = resize_laugh_man.shape[1]

    #笑い男画像のアルファチャンネルだけ抜き出す(0~255の値が入っている)
    alpha = resize_laugh_man[:,:,3]
    alpha = cv.cvtColor(alpha, cv.COLOR_GRAY2BGR) # grayをBGRに変換(各ピクセルのα値を各チャンネル(B,G,Rにコピー))
    alpha = alpha /255.0 #0.0 ~ 1.0の間に変換
    
    laugh_man_color = resize_laugh_man[:,:,:3] #色情報のみを抜き出す

    # カメラ映像に笑い男画像が入りきる場合は重ね合わせ
    if (posY -(resize_laugh_man_height/2) > 0) & (posY +(resize_laugh_man_height/2) < bg.shape[0]) &  (posX - (resize_laugh_man_width/2) > 0) & (posX + (resize_laugh_man_width/2) < bg.shape[1]):  
        bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] = (bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] * (1.0 - alpha)).astype('uint8') #透明度がMaxの箇所はBGR値を0に(黒に)
        bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] = (bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] + (laugh_man_color * alpha)).astype('uint8') #合成

    return bg


def draw_detection(image, detection):
    image_width, image_height = image.shape[1], image.shape[0]

    print(detection)
    print(detection.location_data.relative_keypoints[0])
    print(detection.location_data.relative_keypoints[1])
    print(detection.location_data.relative_keypoints[2])
    print(detection.location_data.relative_keypoints[3])
    print(detection.location_data.relative_keypoints[4])
    print(detection.location_data.relative_keypoints[5])

    # バウンディングボックス
    bbox = detection.location_data.relative_bounding_box
    bbox.xmin = int(bbox.xmin * image_width)
    bbox.ymin = int(bbox.ymin * image_height)
    bbox.width = int(bbox.width * image_width)
    bbox.height = int(bbox.height * image_height)

    cv.rectangle(image, (int(bbox.xmin), int(bbox.ymin)),
                 (int(bbox.xmin + bbox.width), int(bbox.ymin + bbox.height)),
                 (0, 255, 0), 2)

    # スコア・ラベルID
    cv.putText(
        image,
        str(detection.label_id[0]) + ":" + str(round(detection.score[0], 3)),
        (int(bbox.xmin), int(bbox.ymin) - 20), cv.FONT_HERSHEY_SIMPLEX, 1.0,
        (0, 255, 0), 2, cv.LINE_AA)

    # キーポイント：右目
    keypoint0 = detection.location_data.relative_keypoints[0]
    keypoint0.x = int(keypoint0.x * image_width)
    keypoint0.y = int(keypoint0.y * image_height)

    cv.circle(image, (int(keypoint0.x), int(keypoint0.y)), 5, (0, 255, 0), 2)

    # キーポイント：左目
    keypoint1 = detection.location_data.relative_keypoints[1]
    keypoint1.x = int(keypoint1.x * image_width)
    keypoint1.y = int(keypoint1.y * image_height)

    cv.circle(image, (int(keypoint1.x), int(keypoint1.y)), 5, (0, 255, 0), 2)

    # キーポイント：鼻
    keypoint2 = detection.location_data.relative_keypoints[2]
    keypoint2.x = int(keypoint2.x * image_width)
    keypoint2.y = int(keypoint2.y * image_height)

    cv.circle(image, (int(keypoint2.x), int(keypoint2.y)), 5, (0, 255, 0), 2)

    # キーポイント：口
    keypoint3 = detection.location_data.relative_keypoints[3]
    keypoint3.x = int(keypoint3.x * image_width)
    keypoint3.y = int(keypoint3.y * image_height)

    cv.circle(image, (int(keypoint3.x), int(keypoint3.y)), 5, (0, 255, 0), 2)

    # キーポイント：右耳
    keypoint4 = detection.location_data.relative_keypoints[4]
    keypoint4.x = int(keypoint4.x * image_width)
    keypoint4.y = int(keypoint4.y * image_height)

    cv.circle(image, (int(keypoint4.x), int(keypoint4.y)), 5, (0, 255, 0), 2)

    # キーポイント：左耳
    keypoint5 = detection.location_data.relative_keypoints[5]
    keypoint5.x = int(keypoint5.x * image_width)
    keypoint5.y = int(keypoint5.y * image_height)

    cv.circle(image, (int(keypoint5.x), int(keypoint5.y)), 5, (0, 255, 0), 2)

    return image


if __name__ == '__main__':
    main()
