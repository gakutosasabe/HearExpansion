import socket
import tkinter
import numpy as np
import PIL.Image, PIL.ImageTk
import cv2
import threading

def update_image(data):
    global photo

    img = np.frombuffer(data, dtype =np.uint8) # 受け取ったバイナリーデータを8ビット符号なし整数型で配列に変換
    img = cv2.imdecode(img, 1) #配列に変換された画像データをOpenCVの画像形式にカラーでデコード
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #BGR形式の画像をRGBに変換(tkinterがRGBの画像を処理するため)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img)) #PhotoImageオブジェクトを生成
    canvas.create_image(0,0,image = photo, anchor = tkinter.NW)


window = tkinter.Tk()
canvas = tkinter.Canvas(window, width = 300, height = 300)