import urllib.request

def download_image(im_url):

    #画像ダウンロード
    urllib.request.urlretrieve(im_url, "./query/query.jpg")
