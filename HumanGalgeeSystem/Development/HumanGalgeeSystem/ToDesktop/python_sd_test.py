import webuiapi
# APIのインスタンスを作成 ############################
api = webuiapi.WebUIApi()
# プロンプトを宣言 ##################################
PROMPT= "masterpiece, best quality, shinkai makoto, boy"
# 画像を生成する
result1 = api.txt2img(prompt=PROMPT)
# 画像を保存する
result1.image.save("testsd3.png")

