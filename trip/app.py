import random
import requests
import streamlit as st

st.set_page_config(
    page_title="🇰🇷 랜덤 국내여행",
    page_icon="✈️",
    layout="centered"
)

SERVICE_KEY = st.secrets["TOUR_API_KEY"]

URL = "https://apis.data.go.kr/B551011/KorService2/areaBasedList2"


AREA_CODES = {
    "전국": None,
    "서울": 1,
    "인천": 2,
    "대전": 3,
    "대구": 4,
    "광주": 5,
    "부산": 6,
    "울산": 7,
    "세종": 8,
    "경기": 31,
    "강원": 32,
    "충북": 33,
    "충남": 34,
    "경북": 35,
    "경남": 36,
    "전북": 37,
    "전남": 38,
    "제주": 39,
}


@st.cache_data(ttl=3600)
def get_places(area):

    params = {
        "serviceKey": SERVICE_KEY,
        "MobileOS": "ETC",
        "MobileApp": "TripPick",
        "_type": "json",
        "numOfRows": 100,
        "pageNo": 1,
        "contentTypeId": 12
    }

    if AREA_CODES[area] is not None:
        params["areaCode"] = AREA_CODES[area]

    response = requests.get(URL, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    items = (
        data["response"]["body"]
        .get("items", {})
        .get("item", [])
    )

    if isinstance(items, dict):
        items = [items]

    return items


st.title("🇰🇷 랜덤 국내여행 추천")

area = st.selectbox(
    "지역 선택",
    list(AREA_CODES.keys())
)

if st.button("🎲 랜덤 추천"):

    with st.spinner("여행지를 찾는 중..."):

        places = get_places(area)

        if not places:
            st.error("관광지를 찾지 못했습니다.")
            st.stop()

        place = random.choice(places)

        st.success("오늘의 여행지!")

        if place.get("firstimage"):
            st.image(place["firstimage"], use_container_width=True)

        st.subheader(place.get("title", "이름 없음"))

        st.write("📍", place.get("addr1", ""))

        overview = place.get("overview")
        if overview:
            st.write(overview)

        if place.get("mapy") and place.get("mapx"):
            st.map(
                [{
                    "lat": float(place["mapy"]),
                    "lon": float(place["mapx"])
                }]
            )
