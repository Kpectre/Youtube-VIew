from flask import Flask, jsonify
from flask_cors import CORS
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False


def process_request(id):
    channelId = id
    key = "YOUR_API_KEY"  # APIキーを適切なものに置き換えてください

    url = "https://www.googleapis.com/youtube/v3/"
    resource = "search"
    request_url = url + resource

    videoIdList = []
    data = []

    pageToken = None

    while True:
        params = {
            "key": key,
            "part": "id",
            "channelId": channelId,
            "order": "viewCount",
            "type": "video",
            "maxResults": 50,
            "pageToken": pageToken,
        }

        search_result = requests.get(request_url, params=params)
        search_result_json = search_result.json()

        for item in search_result_json["items"]:
            videoIdList.append(item["id"]["videoId"])

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
