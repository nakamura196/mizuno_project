from flask import Flask, render_template, request, redirect, url_for, jsonify
from modules import compare, curation, download, preprocess
from flask_cors import CORS

#インスタンス化
app = Flask(__name__)

CORS(app)

app.config['JSON_AS_ASCII'] = False  # 日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False  # ソートをそのまま

#アプリケーション用のルーティングを記述
@app.route('/')
def hello():
    return "hello"

@app.route('/hojodetection', methods=["GET", "POST"])
def curator():
    default_url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif-img/167904/4872,2848,568,1344/full/0/default.jpg"
    im_url = request.args.get("url", default=default_url, type=str)
    #im_url_resized = im_url.replace("full", "150,") #リサイズはあとで検討する、URLに埋め込むより普通にあとでリサイズした方がいい？

    #クエリ画像をダウンロード
    download.download_image(im_url)#_resized)

    #クエリ画像を加工
    preprocess.resize()
    preprocess.filter()
    preprocess.back_black()

    #検索して結果を格納
    ranking_top5_hojo = compare.compare_image()

    #キュレーションリストを作る
    curationlist = curation.generate_curationList(ranking_top5_hojo)

    return jsonify(curationlist)

    #myjsonにPOSTして帰ってきたURLをGET/POSTで受け取って、それをreturn

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
