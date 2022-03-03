import speech_recognition as sr
import pyaudio
import time



class AudioFilter():
    def __init__(self):










if __name__ == "__main__": #importされた場合に実行しないようにするらしい
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





