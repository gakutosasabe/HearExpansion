# Stable Difussion の処理を別スレッドで回す
    - マルチスレッドはthreading機能を使うらしい
      - https://qiita.com/virusyun/items/f3716e4ec42b6b9cd67b
      - https://yumarublog.com/python/threading/
    - これわかりやすそう
      - https://yassanabc.com/2021/04/23/%E3%80%90python%E3%80%91%E3%83%9E%E3%83%AB%E3%83%81%E3%82%B9%E3%83%AC%E3%83%83%E3%83%89%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9%E3%80%90thread%E3%80%91/

    - threading使って状態管理できればいいかも
      - 生成しているときと生成完了したときの状態を持つ
      - Main側はそれを見て，生成するか判断する
      - 生成しない時は待機状態
      - 状態管理するにはQueueを使えばいいらしい
        - https://note.com/amr1/n/ncd4d2bbb376c
    - 一応最適化は完了したので，新ゲーミングPC側の環境を整える