# coding: UTF-8
import speech_recognition as sr
import pyaudio
import time




class AudioFilter():
    def __init__(self):# classの初期設定
        self.p = pyaudio.PyAudio()
        self.channels = 2 #マイクがモノラルの場合は1
        self.rate = 48000 #DVDレベルなので重かったら16000
        self.format = pyaudio.paInt16
        self.stream = self.p.open(
            format = self.format,
            channels = self.channels,
            rate = self.rate,
            output = True,
            input = True,
            stream_callback=self.callback)#音声が流れてきた時に叩くCallBack関数を指定する


#  format  : ストリームを読み書きするときのデータ型
#  channels: ステレオかモノラルかの選択 1でモノラル 2でステレオ
#  rate    : サンプル周波数
#  output  : 出力モード
    
    # コールバック関数（再生が必要なときに呼び出される）
    def callback(self, in_data, frame_count, time_info, status):
        out_data = in_data
        return (out_data, pyaudio.paContinue)
    # 音声取り込みをやめるとき
    def close(self):
        self.p.terminate() 

if __name__ == "__main__": #importされた場合に実行しないようにするらしい
    #AudioFileterのインスタンスを作る
    af = AudioFilter()
    #ストリーミングを始める
    af.stream.start_stream()

    # ノンブロッキングなので好きなことをしていい場所
    while af.stream.is_active():
        time.sleep(0.1)

    # ストリーミングを止める
    af.stream.stop_stream()
    af.stream.close()
    af.close()


    r = sr.Recognizer()
    with sr.Microphone() as source: # pyaudioを使ってマイクを認識？
        r.adjust_for_ambient_noise(source)
        print("音声を読み取っています")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='ja-JP')
            print(query)
        except:
            print("エラー")





