# coding: UTF-8
import speech_recognition as sr
import pyaudio
import time
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


censor_words = ["こんにちは","ドラえもん","みやさん","バカ","アホ","まぬけ"] #検閲ワード（仮）


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
    
    def mute_audio(self): #スピーカーへの音量を小さくする
        return


class AudioCensorship(): #音声検閲クラス
    def character_search(self, source_words, censor_words): # 文字起こしした文字から検閲ワードを見つける
        word_detect = False # 検閲ワード検出フラグ
        for item in censor_words:
            cw_locate = source_words.find(item)
            if cw_locate != -1:
                print("検閲ワード:" + item + " を発見しました")
                word_detect = True
        return word_detect

class AudioController(object): #スピーカーのボリューム調整クラス
    def __init__(self):
        self.process_name = "python.exe"
        self.defaultvolume = 0.1 #初期ボリューム
        self.enhancedvolume = 0.7 #耳拡張時のボリューム
        self.set_defaultvolume = self.set_volume(self.defaultvolume) #インスタンス生成時にデフォルトのボリュームをセット

    def mute(self): #アプリをミュートにする
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, 'has been muted.')
    
    def unmute(self): #アプリをアンミュートする
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, 'has been unmuted.')

    def set_volume(self, decibels): #アプリのボリュームを変える
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print('Volume set to', self.volume)  # debug
    
    def set_enhanced_volume(self): #self.enhancedvolumeにボリュームを変える
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, self.enhancedvolume))
                interface.SetMasterVolume(self.volume, None)
                print('Volume set to', self.volume)  # debug
    
    def process_volume(self): #現在のボリュームを取得する
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print('Volume:', interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()


class Timer(): #タイマークラス
    def __init__(self):
        self.timer = time.time()
    
    def is_time_out(self, settime): 
        if time.time() - self.timer > settime:
            return True
        else:
            return False
                

if __name__ == "__main__": #importされた場合に実行しないようにするらしい
    #AudioFileterのインスタンスを作る
    af = AudioFilter()
    #AudioCensorshipのインスタンスを作る
    ace = AudioCensorship()
    #AudioControllerのインスタンスを作る
    aco = AudioController()
    

    #ストリーミングを始める
    af.stream.start_stream()

    # ノンブロッキングなのでこの中で音声認識・音の変換などを行う
    while af.stream.is_active():
        #print("なんの処理をしてもOK")
        r = sr.Recognizer()
        with sr.Microphone() as source: # pyaudioを使ってマイクを認識？
            r.adjust_for_ambient_noise(source)
            print("音声を読み取っています")
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='ja-JP')
                print(query)
                words_detect = ace.character_search(query, censor_words)
                if words_detect == True:
                    aco.set_enhanced_volume()
                    mute_timer = Timer()
            except:
                print("エラー")
            
            volume_now = aco.process_volume()
            if round(volume_now, 2) == aco.enhancedvolume: # 現在のボリュームが耳拡張ボリュームだった場合にデフォルトボリュームに戻す
                if mute_timer.is_time_out(5) :
                    aco.set_volume(aco.defaultvolume)

    # ストリーミングを止める
    af.stream.stop_stream()
    af.stream.close()
    af.close()






