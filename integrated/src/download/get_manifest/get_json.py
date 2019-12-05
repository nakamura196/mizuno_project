import urllib.request
import sys

def get_json(json_url, label):

    urllib.request.urlretrieve(json_url,"../../../input/manifest/{}.json".format(label))

    return "{}.json".format(label)


#print(get_json("https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/186421/manifest", "古今歴代十八史略 一 [A004313-01]"))
