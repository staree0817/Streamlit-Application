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
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import re

okt = Okt()

if st.button("분석"):

    video_id = get_video_id(url)
    df = get_comments(api_key, video_id)

    st.success(f"{len(df)}개의 댓글을 가져왔습니다.")

    st.dataframe(df)

    ###################################################
    # 좋아요 TOP10
    ###################################################

    st.subheader("❤️ 좋아요 TOP10 댓글")

    top10 = df.sort_values(
        "좋아요",
        ascending=False
    ).head(10)

    st.dataframe(top10)

    ###################################################
    # 댓글 길이
    ###################################################

    st.subheader("📏 댓글 길이")

    df["길이"] = df["댓글"].str.len()

    fig = px.histogram(
        df,
        x="길이",
        nbins=30
    )

    st.plotly_chart(fig)

    ###################################################
    # 명사 추출
    ###################################################

    nouns = []

    for text in df["댓글"]:

        try:

            nouns.extend(
                okt.nouns(text)
            )

        except:

            pass

    nouns = [

        n

        for n in nouns

        if len(n) >= 2

    ]

    stopwords = {

        "영상","진짜","정말","너무",
        "이번","그냥","감사","오늘",
        "제가","저는","이거","댓글",
        "사람","생각","하나","항상"
    }

    nouns = [

        n

        for n in nouns

        if n not in stopwords

    ]

    counter = Counter(nouns)

    keyword_df = pd.DataFrame(

        counter.most_common(20),

        columns=["키워드","빈도"]

    )

    ###################################################
    # TOP20 키워드
    ###################################################

    st.subheader("🔥 TOP20 키워드")

    st.dataframe(keyword_df)

    fig = px.bar(

        keyword_df,

        x="키워드",

        y="빈도",

        text="빈도"

    )

    st.plotly_chart(fig)

    ###################################################
    # 워드클라우드
    ###################################################

    st.subheader("☁️ 워드클라우드")

    text = " ".join(nouns)

    wc = WordCloud(

        font_path="NanumGothic.ttf",

        width=1200,

        height=700,

        background_color="white"

    ).generate(text)

    fig, ax = plt.subplots(figsize=(12,6))

    ax.imshow(wc)

    ax.axis("off")

    st.pyplot(fig)

    ###################################################
    # 많이 쓴 작성자
    ###################################################

    st.subheader("👤 댓글을 많이 작성한 사용자")

    user_df = (

        df["작성자"]

        .value_counts()

        .head(10)

        .reset_index()

    )

    user_df.columns = [

        "작성자",

        "댓글수"

    ]

    st.dataframe(user_df)

    ###################################################
    # 좋아요 분포
    ###################################################

    st.subheader("👍 좋아요 분포")

    fig = px.histogram(

        df,

        x="좋아요",

        nbins=20

    )

    st.plotly_chart(fig)

    ###################################################
    # CSV 다운로드
    ###################################################

    st.download_button(

        "CSV 다운로드",

        df.to_csv(index=False).encode("utf-8-sig"),

        "comments.csv",

        "text/csv"

    )
