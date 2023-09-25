- Pythonで，メインのループとは別に，ある関数を並列に回し続けようとしたところ結構ハマったので記録
# やりたかったこと
- メインのループで実行したある関数の実行時間が非常に長く，その関数の実行終了まで処理が止まってしまい困っていた
- なのでメインのループとは別に別スレッドである関数を回しておき，もし，別スレッドでの関数が終了したらもう一度その関数を実行したかった(メインループから永遠に別スレッドの関数を回しておきたかった)
# コード
```python
import threading

# 別スレッドで実行する関数
def thread_loop_function(var1,var2,var3):
    # 別スレッドで実行する処理


# メインループ       
def main():
    thread = None
    while True:
        # メインループで回したい処理

        if thread is None or not thread.is_alive() : # ThreadがNone(一つも立っていない)もしくはThreadが全く動いてなかったら
            thread = threading.Thread(target=thread_loop_function,args = (var1,var2,var3))
            thread.start()
               
if __name__ == '__main__':
    main()

```

# ポイント
- threadを定義するときに引数をargsで渡す．targetで渡すとこの場合ではthread_loop_functionを実行してからthreadがスタートするので並列処理にならない
- thread.is_aliveでスレッドが動作しているか確認できるので，必ず一つのThreadを使いまわすようにする


以上