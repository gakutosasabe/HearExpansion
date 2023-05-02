# ライブラリ等の準備
Pythonのバージョン変更や、標準で入っていないPythonライブラリをインストール。

## pythonのバージョン切り替え
Raspberry piではインストール直後はpython2.x系がデフォルトになっている。
python3,x系を使用したいため、下記サイトを参照してpythonにpython3を紐づけなおす。

参考：https://python-academia.com/raspberry-pi-python-version/

## pyaudio
そのまま`pip`でインストールしようとすると、`src/pyaudio/main.c:31:10: fatal error: portaudio.h: そのようなファイルやディレクトリはありません`といったエラーが発生するため、下記リンクを参考にインストール。

参考：https://plaza.rakuten.co.jp/qualis00/diary/202105150000/
```
sudo apt-get install python-dev portaudio19-dev
sudo pip3 install pyaudio
```
## numpy
```
pip install numpy
```

## scipy
`pip`ではインストールできなかったため、下記コマンドでインストール。
```
sudo apt-get install python3-scipy
```

## librosa
`pip`でインストールしようとすると`piwheel`周りの依存関係で失敗する。このため、下記の通りバージョンを下げて`librosa`をインストールした。
ただ、そもそもなくても動きそう。

参考：https://tomokiit.hatenablog.jp/entry/2020/05/19/145750
```
pip3 install librosa==0.4.2
```

## pyworld
普通に`pip`でインストールすると、下記のようなエラーが出た。
```
ValueError: numpy.ndarray size changed, may indicate binary incompatibility.
```
これは、`pyworld`がインストールの高速化のために`Wheel`を使用するようで、これによってビルド済み（バイナリ）の`numpy`を使用しており、今回、この`pyworld`が使用している`numpy`と自環境の`numpy`とでバージョンが異なる状態でコンパイルしようとしているため、上記のようなエラーが出た模様。

このため、下記の通り`numpy`のアップデートの実施、`pyworld`内で使用している`Cython`および`pyworld`自体をバイナリファイルを使用しないように下記の通り指定してインストールしなおしたところ、コンパイルが通った。
実際はどれかのコマンドのみでも動くかもしれないが、どれが要因だったかは不明。
```
pip install --upgrade numpy
pip install Cython --no-binary Cython
pip install pyworld --no-binary pyworld
```
参考：https://zenn.dev/ymd_h/articles/934a90e1468a05

参考：https://kurozumi.github.io/pip/user_guide.html

参考：https://stackoverflow.com/questions/66060487/valueerror-numpy-ndarray-size-changed-may-indicate-binary-incompatibility-exp

参考：https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder/blob/master/README.md
