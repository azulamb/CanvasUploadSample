# サンプル

HTML5のCanvasで描画した内容をサーバーにアップロードするサンプル。
あるプロジェクトで使ったのでエッセンスだけ抽出してすぐに使えるようにしておくためのメモ書き。
なお動作確認してないので動かなかったらごめん。

## 処理概要

JavaScriptでCanvasのオブジェクトを取得すると、　というメソッドでCanvasをPNGにした時のデータを文字列で取得できる。

文字列の内容は

    data:TYPE,DATA

で、TYPEがMIME-Typeでimage/pngがデフォルト。

DATAはBase64エンコードされたデータが入っている。
これをサーバーに送ってBase64デコードすればPNGバイナリを取得できる。

しかし、Base64はURLエンコードしないといけない文字が使われているので、送るときにはencodeURIComponent()を利用してエンコードする。

CGIではデータを受け取って加工すれば終了。

Canvasの一部を繰り抜いて使いたい場合は、送りたいサイズのCanvasを用意しておき、次のような手順でCanvasを用意する。

+ new Image()で画像を作り、srcに元CanvasのtoDataURL()を直接指定する。
+ onload時に送りたいサイズのCanvasのオブジェクトを取得し、そこにCanvasを画像化したこの画像を切り取って描画
+ 適切なサイズのCanvasでtoDataURL()をしてサーバーに送る。