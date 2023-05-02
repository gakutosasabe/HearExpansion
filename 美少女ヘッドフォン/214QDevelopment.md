# Projectの目的
- 身体拡張テーマということで、耳の身体拡張の可能性を探る
# 問い
- 耳機能を制限したり拡張したり、変換をかけたりしたら、人間はどういう感情になるのか？どういう思考が誘発されるのか？
# 具体的にやりたいこと
1. 具体的には音声の文字起こしとその文字を活用した耳機能拡張（あるワードを聞こえないようにする、あるワードが聞こえたら、聞こえる音をおおきくする等、文字起こした内容を要約して、視界に投影する等）
2. 聞こえる音を加工することによって、音の認識能力事態に変化を与える（リアルタイムで聞こえる音が恋声になるとか、目の前の人から発された声がイケボになるとか）
# 実装タスク
- Pythonの環境を整える（関連のライブラリなど,pip）- ぶちょー
    - Python
        - <参考にしたサイト> https://www.python.jp/install/windows/install.html
        - インストールver. python-3.9.1-amd64.exe
        - Add Python 3.x to PATH を忘れないこと
    - pip → 3.9.1にすでに入っているのでインストール不要
- Pythonでマイクからの音声を取り込む - SSB(完了)
- Speech Recognitionを使って文字起こししてみる - SSB(完了)
    - https://self-development.info/python%E3%81%A7%E9%9F%B3%E5%A3%B0%E3%81%8B%E3%82%89%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%81%B8%E5%A4%89%E6%8F%9B%E3%80%90speechrecognition%E3%80%91/
- 文字起こしの結果から、音声のフィードバックの仕方を変化させてみる
- 音の加工、ピッチの変更とかのライブラリを探る
- 音の加工やピッチの変更を実際に行ってみる。

# 開発メモ
## Speech Recognitionを使って文字起こしをする
### 実行環境
- Python 3.9
### SpeechRecognitionとPyaudioのinstall
- SpeechRecognitionをpip経由でインストールする
```
pip install SpeechRecognition
```
### WindowsのPyaudioインストール
- Python3.7~3.9だとPyaudioがpip経由でインストールできない。非公式版だが、下記URLからPython 3.9用 Pyaudio(PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl)をダウンロードする
    - https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- whlファイルがあるディレクトリでpip経由でインストールする
```
py -m pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```
### linuxのPyaudioインストール
- portaudioというライブラリに依存しておりそのままだとpip経由でpyAudioインストールしようとするとエラーを吐くため
```
sudo apt-get install portaudio19-dev
```
でportaudioをインストールしてから
```
pip install pyaudio
```
でOK
### 実装したコード
```
import speech_recognition as sr
import pyaudio

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

```
### 実行結果
- こんにちはといった場合<br>
![picture 1](images/a35dcf4658d7e437931abd0d093210c412e8b14be3bb8d644c8472fcaef4032c.png)  
- こんにちは私の名前は佐々部岳人ですといった場合
![picture 3](images/736d4d91efd984bcc42dac0261dc752970e36e29cda41e0195201f8e58608918.png) 
### まとめ
- そこそこの精度は出る。
- マイク入力の終わりを指定してないけど、何故か音声の終わりは検知している
### 参考資料
- Pythonでマイクを用いた音声認識を行う
    - https://heartstat.net/2021/05/27/python_speech_recognition/
    - http://xn--u9j207iixgbigp2p.xn--tckwe/archives/10584

## 文字起こしの結果から、音声のフィードバックの仕方を変化させてみる
### 要求
- マイクから入力した音声をそのままスピーカーに流す
- 検閲させるキーワードを設定する
- 文字起こしの内容から検閲ワードを見つける
- 検閲ワードを見つけたらマイクから得た音声に何かしらの加工をかけて（まずは簡単にP音を１０秒流す）検閲ワードをユーザーに聞かせないようにする
### 詳細タスク
- 検閲ワードをユーザーに入力させて配列に入れる
    - KeyInoutクラス　key_input関数
- 最新の文字起こししたセンテンスに検閲ワードが含まれていないか検索する 
    - AudioCensorshipクラス　character_search関数
- 検閲ワードが含まれていた場合は、スピーカーからの音量を予め設定していたボリュームに◯秒変える 
    - AudioControllerクラス　set_enhanced_volume関数
    - Timerクラス is_time_out関数
- 文字起こししたセンテンスを配列に保存する

## Pyaudioを使ってマイクから入力した音声をそのままスピーカーに流す
- Pyaudioを使えばマイクからの音の入力を並列処理できるということらしい。常にマイクから音を取り続けていることが必要なので、スレッドを作ってそちらで常に処理を行っておく必要があるがPyaudioのノンブロッキングモードを使えば勝手にPyaudioでThreadを作ってくれて実行してくれるようだ。
- なのでStreamがOpenしている（音をマイクから収集してスピーカーに流している間）間に音声認識なり、音調変換なりを行えば良さそう

### 実装コード
```
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

    # ノンブロッキングなのでこの中で音声認識・音の変換などを行う
    while af.stream.is_active():
        print("なんの処理をしてもOK")
        #r = sr.Recognizer()
        #with sr.Microphone() as source: # pyaudioを使ってマイクを認識？
        #    r.adjust_for_ambient_noise(source)
        #    print("音声を読み取っています")
        #    audio = r.listen(source)
        #    try:
        #        query = r.recognize_google(audio, language='ja-JP')
        #        print(query)
        #    except:
        #        print("エラー")
    # ストリーミングを止める
    af.stream.stop_stream()
    af.stream.close()
    af.close()
```
### 結果
- 若干実際の音声に対して遅れて出力されるが、音質的には問題なさそう
### 参考資料 
- PyAudioを用いてマイクの入力をそのまま出力する
    - https://ensekitt.hatenablog.com/entry/2018/09/07/200000
    - https://takeshid.hatenadiary.jp/entry/2016/01/10/153503

## 検閲ワードをユーザーから入力する
### ユースケース
1. アプリを立ち上げる
2. "検閲ワードを入力してください:”の表示
3. ユーザーが検閲ワードを入力してEnterを押す
4. "更に閲覧ワードの入力を続けますか？(Y/N)”の表示
5. Yが押された場合は2.から繰り返し
6. Nが押された場合は入力を終了する
### タスク
- アプリの立ち上げと同時にKeyInputクラスのインスタンスを作る
- KeyInputクラスの中のコンストラクタでkey_input関数を実行する
### 参考
- キー入力の例外処理
    - https://d-python.com/2020/03/22/try-except/
- yes noで処理
    - https://cortyuming.hateblo.jp/entry/2015/12/26/085736
    - https://qiita.com/u1and0/items/66a72fef8bc0a7ce5eda
## PyAudioとPyworldを使ってマイクから拾った音に対して加工をかけてからスピーカーに流す
- PyaudioとPyworldを使うことによって、リアルタイム音声合成が可能
- PyaudioでChunk毎に切り取った音声データをPyworldで加工した後、出力してあげるイメージ
- 参考資料
    - https://gist.github.com/tam17aki/8e702542f5e16c0815e7ddcc6e14bbb8
    - https://tam5917.hatenablog.com/entry/2022/01/10/155454
    - https://tam5917.hatenablog.com/entry/2019/04/28/123934
    - https://gist.github.com/lefirea/ca5141176507c8d543542f09dc401164

 - voice_converter.py　を使用する
 - 関連パッケージのインストール
    - pip install numpy
    - pip install scipy
    - pip install librosa
    - pip install wheel
    - pip install pyworld

 - pip install pyworldが通らない場合
    - "Build Tools for Visual Studio 2019"をインストールすることで解決。
    ※「C++ Build Tool」と「MSCV v140」にチェックしてインストールすること。
    - https://mebee.info/2020/07/18/post-13597/
    - https://qiita.com/yuki_2020/items/ecb3448c375ba0bec510

## Pycawを使ってWindowsのマスターボリュームをPythonから操作する
- Pycawというライブラリを使うと、Windowsのアプリケーション毎にPythonからボリュームを変えられる
- プロセス名を指定すればアプリケーション毎にボリュームの設定が可能
- win32APIのISimpleAudioVolumeインターフェースをPythonで使えるようなイメージ
    - https://docs.microsoft.com/en-us/windows/win32/api/audioclient/nn-audioclient-isimpleaudiovolume
### Pycawのインストール
- pip経由でPycawを落としてくる
```
pip install pycaw
```
### 使い方
- 例：全てのアプリ(全てのSession)をMuteする
```
"""
Per session GetMute() SetMute() using ISimpleAudioVolume.
"""
from __future__ import print_function

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        print("volume.GetMute(): %s" % volume.GetMute())
        volume.SetMute(1, None)


if __name__ == "__main__":
    main()
```
### 結果
- 全てのアプリをMuteすることができた。
![picture 1](images/cd78637348f97fb487733df1440e01b7ca260e44a252de9d09ebd17c6f011c72.png)  

### 参考資料
- https://stackoverflow.com/questions/20828752/python-change-master-application-volume
- https://openbase.com/python/pycaw/documentation
## Pyalsaudioを使ってラズパイのボリュームをPythonから操作する
- 参考資料
    - https://stackoverflow.com/questions/20828752/python-change-master-application-volume
    - https://openbase.com/python/pycaw/documentation
