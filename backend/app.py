from flask import Flask
from flask_cors import CORS
import requests


app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False


def process_request(id):
    # 検索したいチャンネルのchannelId
    channelId = id
    key = "AIzaSyDzqOJPnXNXHYxsT_rBCvwJZbi4jVUxHcs"

    # SearchリソースのリクエストURL指定
    url = "https://www.googleapis.com/youtube/v3/"
    resource = "search"
    request_url = url + resource

    # 空のリストを準備
    videoIdList = []
    data = []

    # pageTokenの初期化
    # f
    pageToken = None

    while True:
        # パラメータ設定
        params = {
            "key": key,  # 1.で取得したAPIキーを入力
            "part": "id",  # videoIdを含むプロパティ
            "channelId": channelId,  # 検索したいチャンネルのchannelId
            "order": "viewCount",  # 検索結果を時系列順に表示
            "type": "video",  # 動画のみを検索（プレイリストなどを検索結果に含まない）
            "maxResults": 50,  # 1リクエストあたりの検索結果の動画数（デフォルトは5、最大で50まで設定可能）
            "pageToken": pageToken,  # リクエストのトークン
        }

        # リクエスト実行
        search_result = requests.get(request_url, params=params)

        # json形式の結果を格納
        search_result_json = search_result.json()

        # videoIdの抽出
        for item in search_result_json["items"]:
            videoIdList.append(item["id"]["videoId"])

        # 検索結果を全て表示できていない場合はpageTokenを更新
        if "nextPageToken" in search_result_json:
            pageToken = search_result_json["nextPageToken"]
        else:
            break

    videoIdList.reverse()

    videoIdList_splitted = []

    url = "https://www.googleapis.com/youtube/v3/"
    resource = "videos"
    request_url = url + resource

    for i in range(0, len(videoIdList), 50):
        videoIdList_splitted.append(videoIdList[i : i + 50])

    for videoId_grp in videoIdList_splitted:
        params = {"key": key, "part": "snippet,statistics", "id": ",".join(videoId_grp)}

        videos_result = requests.get(request_url, params=params)
        videos_result_json = videos_result.json()

    for item in videos_result_json["items"]:
        title = item["snippet"]["title"]
        viewCount = item["statistics"]["viewCount"]
        id = item["id"]

        data.append([title, viewCount, id])

    return data


@app.route("/<id>")
def index(id):
    return process_request(id)


app.run(port=8000, debug=True)
