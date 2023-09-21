import webuiapi
import cv2 as cv
import base64
from PIL import Image
# APIのインスタンスを作成 ############################
api = webuiapi.WebUIApi(host='192.168.0.30', port=7860)
# プロンプトを宣言 ##################################
PROMPT= "masterpiece, best quality, shinkai makoto, boy"
faceimage = Image.open("facetrim.png")   

girlimage = api.img2img(images = [faceimage], prompt=PROMPT, seed=5555, cfg_scale=6.5, denoising_strength=0.5)
# 画像を保存する
girlimage.image.save("girlimage.png")

