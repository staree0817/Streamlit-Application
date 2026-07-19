import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs

st.title("YouTube 댓글 분석기")

api_key = st.text_input("YouTube API Key", type="password")
url = st.text_input("영상 URL")

def get_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]

    query = parse_qs(urlparse(url).query)
    return query.get("v", [None])[0]


def get_comments(api_key, video_id):

    comments = []
    page_token = ""

    while True:

        res = requests.get(
            "https://www.googleapis.com/youtube/v3/commentThreads",
            params={
                "part":"snippet",
                "videoId":video_id,
                "maxResults":100,
                "pageToken":page_token,
                "textFormat":"plainText",
                "key":api_key
            }
        ).json()

        if "items" not in res:
            break

        for item in res["items"]:

            s = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({
                "작성자": s["authorDisplayName"],
                "댓글": s["textDisplay"],
                "좋아요": s["likeCount"]
            })

        page_token = res.get("nextPageToken")

        if not page_token:
            break

    return pd.DataFrame(comments)


if st.button("분석"):

    video_id = get_video_id(url)

    df = get_comments(api_key, video_id)

    st.write(f"댓글 {len(df)}개")

    st.dataframe(df)

    st.download_button(
        "CSV 다운로드",
        df.to_csv(index=False).encode("utf-8-sig"),
        "comments.csv",
        "text/csv"
    )
