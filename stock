import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Global Market Cap Top10 Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌍 Global Market Cap Top10 Stock Dashboard")
st.caption("최근 1년간 글로벌 시가총액 Top10 기업의 주가 변화")

companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Saudi Aramco": "2222.SR",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

@st.cache_data(ttl=3600)
def load_data():

    end = datetime.today()
    start = end - timedelta(days=365)

    df = pd.DataFrame()

    for name, ticker in companies.items():

        data = yf.download(
            ticker,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True
        )

        if len(data) > 0:
            df[name] = data["Close"]

    return df


prices = load_data()

selected = st.multiselect(
    "기업 선택",
    prices.columns,
    default=prices.columns
)

plot_df = prices[selected]

fig = go.Figure()

for col in plot_df.columns:

    fig.add_trace(
        go.Scatter(
            x=plot_df.index,
            y=plot_df[col],
            mode="lines",
            name=col
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=650,
    title="최근 1년 주가",
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    legend_title="Company"
)

st.plotly_chart(fig, use_container_width=True)

returns = (
    (plot_df.iloc[-1] / plot_df.iloc[0] - 1)
    * 100
).sort_values(ascending=False)

st.subheader("📊 최근 1년 수익률")

col1, col2, col3, col4, col5 = st.columns(5)

cols = [col1, col2, col3, col4, col5]

for i, (name, value) in enumerate(returns.items()):
    cols[i % 5].metric(
        label=name,
        value=f"{value:.2f}%"
    )

with st.expander("주가 데이터 보기"):
    st.dataframe(plot_df)
