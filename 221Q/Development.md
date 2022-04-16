# 221Qテーマ
1. ある方向の音声を増強し、それ以外の方向の音声を減衰させることによって、耳の認識を補助するデバイスの開発
2. 1Qで培ったSSTの技術やdlibでの顔認識技術を使って、音声のライフログを取る、人類ギャルゲー化計画

# ある方向の音声を増強し、それ以外の方向の音声を減衰させることによって、耳の認識を補助するデバイスの開発
## 具体的調査項目
- Respeakerを用いた音源音源定位のプロトタイプ作成
- Respeakerもしくは回転する指向性マイク等を使った特定の方向の音声を取ってくるシステムの開発
# 1Qで培ったSSTの技術やdlibでの顔認識技術を使って、音声のライフログを取る、人類ギャルゲー化計画
## 作業項目
- 声紋認識技術のプロトタイプ作成
- 画像からの人物特定技術のプロトタイプ作成
## 調査
### 声紋認識技術の調査
- OSSの音声認識エンジンJuliusを使った母音のクラスタリング
    - https://qiita.com/k-maru/items/4f12fd0f8344b9e093bd
- 人の声のフォルマントを特徴量として取ってきて、その特徴量によって誰が喋ったかを分類する？
    - だが、個人が特定できるレベルの普遍的なフォルマントの特徴量とかあるのか？
    - 上の例でもあるように、分類するのにDeeplearningを必要としそう
- 話者認識についての首都大の授業スライド
    - https://www.sp.ipc.i.u-tokyo.ac.jp/~saruwatari/SP-Grad2016_06.pdf
    - 話者認識とはSpeaker Verigficationという分野らしい
    - 話者を特定する普遍的なパラメータとしてMFCCというものがあるらしい
- SVMとLPC分析でPythonによるSpeaker Verification
    - https://heartstat.net/2021/05/12/python_sr_lpc_svm/
- PaizaにPython×機械学習の講座があり、この中で声優の話者認識をしている
    - https://paiza.jp/works/ai_ml/primer
### やってみること
- まずはPaizaの講座を受けてみようかな
    - とりあえず登録完了
### Paiza講習メモ
- とりあえずPythonで機械学習するためにJupyterNotebookというのを入れたほうが良いらしい
    - 使いやすいPythonの実行ツールとのこと
#### jupiter-notebookのインストール
```
pip install jupyter-notebook
```
- そもそもpipのversionが古いらしい
- pip入れなおすかーと思ってget-pip.pyを十個水曜と思ったらPython３のVersionが古いらしい
- ということでPython3のヴァージョンアップをしてからpipを入れなおすぞ

### 画像からの人物特定技術の調査
- OpenCVで顔を特定して追従まではできそうだけど、元々の顔写真を登録しておく必要がありそうだなぁ。これは声紋も一緒か？
    - https://qiita.com/Hironsan/items/8ad9b11bcc0c618ec5e2
