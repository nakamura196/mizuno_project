from flask import Flask, request, jsonify, redirect
from modules import compare, curation, download, preprocess
from flask_cors import CORS
import os, json, hashlib

#インスタンス化
app = Flask(__name__)

CORS(app)

app.config["JSON_AS_ASCII"] = False  # 日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False  # ソートをそのまま

#法帖類似検索し、検索結果を保存する
def hojodetection(im_url):
    #既存の検索結果なら何もしない
    calculated_results = os.listdir("./results/")
    hashed_im_url = hashlib.sha1(im_url.encode()).hexdigest() + ".json"
    if hashed_im_url in calculated_results:
        return

    #新規検索なら以降の処理をやる
    im_url_resized = im_url.replace("full", "150,") #幅150より小さいクエリ画像についてはあとで検討する

    #クエリ画像をダウンロード
    download.download_image(im_url_resized)

    #クエリ画像を加工
    #preprocess.resize()
    preprocess.filter()
    preprocess.back_black()

    #検索して結果を格納
    ranking_top5_hojo = compare.compare_image()

    #キュレーションリストを作る
    curationlist = curation.generate_curationList(ranking_top5_hojo)

    #既存の検索結果として保存
    store_name = hashlib.sha1(im_url.encode()).hexdigest()
    curationlist_js = json.dumps(curationlist)
    with open("./results/{}.json".format(store_name), "w") as f:
        f.write(curationlist_js)

#アプリケーション用のルーティングを記述
@app.route("/")
def hello():
    return "hello"

@app.route("/hojodetection", methods=["GET"])
def curator():
    im_url = request.args.get("url", type=str)

    #結果を格納フォルダから持ってきてJSON化して返す
    hashed_im_url = hashlib.sha1(im_url.encode()).hexdigest()
    with open("./results/{}.json".format(hashed_im_url), "r") as f:
        output = json.load(f)

    return jsonify(output)

@app.route("/curation", methods=["GET"])
def _redirect():
    #画像URLをGET
    default_url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif-img/167904/4872,2848,568,1344/full/0/default.jpg"
    im_url = request.args.get("url", default=default_url, type=str)

    #hojodetectionの処理
    hojodetection(im_url)

    #リダイレクト
    return redirect("http://icc.jp-r.com/app/#/?curation=http://diyhistory.org:5001/hojodetection?url={}".format(im_url))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
