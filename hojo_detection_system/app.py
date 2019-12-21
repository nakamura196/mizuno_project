from flask import Flask, render_template, request, redirect, url_for, jsonify
from modules import compare, curation, download, preprocess

#インスタンス化
app = Flask(__name__)

#アプリケーション用のルーティングを記述
@app.route('/')
def hello():
    return "hello"

@app.route('/hojodetection')
def curator():
    im_url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif-img/167904/4872,2848,568,1344/full/0/default.jpg"
    #im_url_resized = im_url.replace("full", "150,") #リサイズはあとで検討する、URLに埋め込むより普通にあとでリサイズした方がいい？

    #クエリ画像をダウンロード
    download.download_image(im_url)

    #クエリ画像を加工
    preprocess.resize()
    preprocess.filter()
    preprocess.back_black()

    #検索して結果を格納
    ranking_top5_hojo = compare.compare_image()

    #キュレーションリストを作る
    curationlist = curation.generate_curationList(ranking_top5_hojo)

    return jsonify(curationlist)

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
