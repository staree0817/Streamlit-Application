import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울시 공영주차장 정보",
    page_icon="🅿️",
    layout="wide"
)

st.title("🅿️ 서울시 공영주차장 정보 앱")

uploaded_file = st.file_uploader(
    "서울시 공영주차장 CSV 또는 Excel 파일 업로드",
    type=["csv","xlsx"]
)

if uploaded_file is not None:

    # 파일 읽기
    if uploaded_file.name.endswith(".csv"):
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        except:
            df = pd.read_csv(uploaded_file, encoding="cp949")
    else:
        df = pd.read_excel(uploaded_file)

    st.success("파일 업로드 완료!")

    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    st.write("---")

    ########################################
    # 컬럼 선택
    ########################################

    st.subheader("컬럼 설정")

    lat_col = st.selectbox("위도 컬럼", df.columns)
    lon_col = st.selectbox("경도 컬럼", df.columns)

    name_col = st.selectbox("주차장명 컬럼", df.columns)

    fee_col = st.selectbox("기본요금 컬럼", df.columns)

    address_col = st.selectbox("주소 컬럼", df.columns)

    ########################################
    # 지도
    ########################################

    map_df = df.copy()

    map_df[lat_col] = pd.to_numeric(map_df[lat_col], errors="coerce")
    map_df[lon_col] = pd.to_numeric(map_df[lon_col], errors="coerce")

    map_df = map_df.dropna(subset=[lat_col, lon_col])

    st.subheader("🗺️ 주차장 위치")

    fig = px.scatter_map(
        map_df,
        lat=lat_col,
        lon=lon_col,
        hover_name=name_col,
        hover_data=[address_col, fee_col],
        zoom=10,
        height=700
    )

    fig.update_layout(
        map_style="open-street-map",
        margin=dict(l=0,r=0,t=0,b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

    ########################################
    # 검색
    ########################################

    keyword = st.text_input("주차장 검색")

    result = map_df.copy()

    if keyword:
        result = result[
            result[name_col].astype(str).str.contains(keyword)
        ]

    ########################################
    # 요금 정렬
    ########################################

    result[fee_col] = (
        result[fee_col]
        .astype(str)
        .str.replace(",","")
        .str.extract(r'(\d+)')[0]
    )

    result[fee_col] = pd.to_numeric(result[fee_col], errors="coerce")

    result = result.sort_values(
        fee_col,
        ascending=True
    )

    st.subheader("💰 요금 순 정렬")

    st.dataframe(result)

    ########################################
    # 다운로드
    ########################################

    csv = result.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📥 요금순 CSV 다운로드",
        csv,
        "parking_fee_sorted.csv",
        "text/csv"
    )
