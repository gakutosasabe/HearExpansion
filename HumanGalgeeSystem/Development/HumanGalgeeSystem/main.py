#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse

import cv2 as cv
import numpy as np
import mediapipe as mp
import webuiapi

from utils import CvFpsCalc

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="beautiful boy,shinkai makoto")
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument("--model_selection", type=int, default=0)
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)

    parser.add_argument('--use_brect', action='store_true')

    args = parser.parse_args()

    return args

def main():
    # 引数解析 ###############################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    prompt = args.prompt

    model_selection = args.model_selection
    min_detection_confidence = args.min_detection_confidence

    use_brect = args.use_brect

    # StableDiffusionのAPIのインスタンスを作成 ############################
    api = webuiapi.WebUIApi()
    # カメラ準備　###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード　###############################################################
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=model_selection,
        min_detection_confidence=min_detection_confidence,
    )

    # FPS計測モジュール ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len = 10)

    while True:
        # カメラキャプチャ　###############################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1) #ミラー表示
        overlay_image = copy.deepcopy(image)

        # 検出実施　###############################################################
        #image = cv.cvtColor(image, cv.COLOR_RGB)
        results = face_detection.process(image)

        # 顔位置＆場所検出 ###############################################################
        if results.detections is not None:
            for detection in results.detections:
               # 検出された顔の場所を取得
               image,posX, posY,posCX,posCY,sizeW,sizeH = culculate_face_pos_and_size(image, detection)
               # 顔の切り抜き画像を取得
               faceimage = trim_face(posX,posY,sizeW,sizeH,image)
               # StableDiffusion変換後画像を取得
               # sdimage = conv_face2girl(api,faceimage,prompt)
               # StableDiffusion返還後画像を重ねる
               overlay_image = overlay_illust(image,posCX,posCY,sizeH)
    
        # キー処理(ESC：終了) #################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映 #############################################################
        cv.imshow('MediaPipe Face Detection Demo', overlay_image)
        cv.imshow('FaceTrim', faceimage)
    
    cap.release()
    cv.destroyAllWindows()
    
    
    
    #faceimage = trim_face(posX,posY,posZ,sizeW,sizeH,image)
    #girlimage = conv_face2girl(faceimage)

    
    return

# 顔のx座標,y座標,x中心座標,y中心座標, 幅，高さを抽出　###############################################################
def culculate_face_pos_and_size(image,detection):
    image_width, image_height = image.shape[1], image.shape[0]
    bbox = detection.location_data.relative_bounding_box
    sizeW = int(bbox.width * image_width) # 幅
    sizeH = int(bbox.height * image_height) # 高さ
    posX = int(bbox.xmin * image_width) #X座標
    posY = int(bbox.ymin * image_height) #Y座標
    posCX = int(bbox.xmin * image_width + (sizeW/2)) #X中心座標
    posCY = int(bbox.ymin * image_height + (sizeH/2)) #Y中心座標
    
    cv.putText(image, "posX:" + str(posX) + " posY:" + str(posY) + " sizeW" + str(sizeW) + " sizeH" + str(sizeH),
               (10,30),cv.FONT_HERSHEY_SIMPLEX,1.0,(0,255,0),2,cv.LINE_AA)
    
    return image, posX, posY, posCX,posCY,sizeW,sizeH

# 重ね合わせ画像をresizeして透明化して重ねる
def overlay_illust(bg,posX,posY,sizeH):
    laugh_man = cv.imread("C:\\Users\\user\\Desktop\\HearExpansion\\HumanGalgeeSystem\\Development\\HumanGalgeeSystem\\warai_flat.png",cv.IMREAD_UNCHANGED)  # アルファチャンネル込みで読み込む)
    resize_laugh_man = cv.resize(laugh_man, dsize=None, fx=0.4, fy=0.4)
    resize_laugh_man_height = resize_laugh_man.shape[0]
    resize_laugh_man_width = resize_laugh_man.shape[1]

    #重ね合わせ画像のアルファチャンネルだけ抜き出す(0~255の値が入っている)
    alpha = resize_laugh_man[:,:,3]
    alpha = cv.cvtColor(alpha, cv.COLOR_GRAY2BGR) # grayをBGRに変換(各ピクセルのα値を各チャンネル(B,G,Rにコピー))
    alpha = alpha /255.0 #0.0 ~ 1.0の間に変換
    
    laugh_man_color = resize_laugh_man[:,:,:3] #色情報のみを抜き出す

    # カメラ映像に笑い男画像が入りきる場合は重ね合わせ
    if (posY -(resize_laugh_man_height/2) > 0) & (posY +(resize_laugh_man_height/2) < bg.shape[0]) &  (posX - (resize_laugh_man_width/2) > 0) & (posX + (resize_laugh_man_width/2) < bg.shape[1]):  
        bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] = (bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] * (1.0 - alpha)).astype('uint8') #透明度がMaxの箇所はBGR値を0に(黒に)
        bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] = (bg[int(posY-(resize_laugh_man_height/2)):int(posY+(resize_laugh_man_height/2)),int(posX-(resize_laugh_man_width/2)):int(posX+(resize_laugh_man_width/2))] + (laugh_man_color * alpha)).astype('uint8') #合成

    return bg

# 顔の部分を切り抜き
def trim_face(posX,posY,sizeW,sizeH,image):
    faceimage = image[posY:posY+sizeH,posX:posX+sizeW] 
    return faceimage

# StableDiffusionのimg2imgで画像を生成する
def conv_face2girl(api,faceimage,prompt):
    # 画像を生成する
    girlimage = api.img2img(images = faceimage, prompt=prompt, seed=5555, cfg_scale=6.5, denoising_strength=0.2)
    
    if girlimage is None:
        laugh_man = cv.imread("C:\\Users\\user\\Desktop\\HearExpansion\\HumanGalgeeSystem\\Development\\HumanGalgeeSystem\\warai_flat.png",cv.IMREAD_UNCHANGED)  # アルファチャンネル込みで読み込む)
        girlimage = laugh_man

    return girlimage


if __name__ == '__main__':
    main()

