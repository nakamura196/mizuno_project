import urllib.request, json

if __name__ == '__main__':
    url = "https://api.myjson.com/"
    method = "POST"
    headers = {"Content-Type" : "application/json"}

    # PythonオブジェクトをJSONに変換する
    sample_ = {"hoge":0, "fuga":"4"}
    json_data = json.dumps(sample_).encode("utf-8")

    # httpリクエストを準備してPOST
    req = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")

        print(response_body)
